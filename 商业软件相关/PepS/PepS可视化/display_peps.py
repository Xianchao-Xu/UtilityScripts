#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkUnstructuredGrid,
    VTK_LINE
)
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor
)

# noinspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2


class Node:
    def __init__(self, node_id: str, x: float = 0., y: float = 0., z: float = 0.) -> None:
        self.id: str = node_id
        self.x: float = x
        self.y: float = y
        self.z: float = z


class Element:
    def __init__(self, element_id: str, element_type: str, connection: list[str]) -> None:
        self.id: str = element_id
        self.type: str = element_type
        self.connection: list[str] = connection


class Card:
    def __init__(self, title: str):
        self.title = title
        self.properties: dict[str, str] = dict()

    def add_property(self, key: str, value: str):
        self.properties.setdefault(key, value)


class Model:
    def __init__(self) -> None:
        self.nodes: dict[str, Node] = dict()
        self.elements: dict[str, Element] = dict()

    def add_node(self, node: Node) -> None:
        self.nodes.setdefault(node.id, node)

    def add_element(self, element: Element) -> None:
        self.elements.setdefault(element.id, element)

    def get_node(self, node_id: str):
        return self.nodes.get(node_id)

    def get_element(self, element_id: str):
        return self.elements.get(element_id)


class PepsParser:
    def __init__(self, filename: str):
        self.file = filename
        self.card_lines: list[str] = list()
        self.cards: list[Card] = list()
        self.model = Model()
        self.node_mapping: dict[str, int] = dict()

    def clean_file(self, filename: str) -> None:
        """
        清理输入文件，删除空行、注释，拼接多行卡片
        :param filename: filename 文件名
        :return: None
        """
        with open(filename, 'r') as fr:
            line = fr.readline()
            while line:
                line = line.split('*')[0]  # 删除注释
                if line.strip():  # 只处理非空行
                    if not line.startswith(' '):
                        self.card_lines.append(line.rstrip().replace('  ', ' '))
                    else:
                        self.card_lines[-1] += ' ' + line.strip().replace('  ', ' ')
                line = fr.readline()

    def init_card(self, lines: list[str]):
        n_line = len(lines)
        for i in range(n_line):
            card_text = lines[i]
            card_title = card_text[:4]  # 卡片名
            card = Card(card_title)
            card_map = list()  # 卡片参数列表，由于卡片中的描述字符中存在空格，直接分割会出错，先处理字符串中的空格
            card_property = card_text[4:].strip()
            card_map_temp = card_property.split(' ')
            for value in card_map_temp:
                if '=' in value:
                    card_map.append(value)
                else:
                    if len(card_map):
                        card_map[-1] += ' ' + value
                    else:
                        card_map.append('')
            for param in card_map:
                if param:
                    key, value = param.split('=')
                    card.add_property(key, value)
                else:
                    card.add_property('', '')
            self.cards.append(card)

    def parse(self):
        self.clean_file(self.file)  # 清理输入卡
        self.init_card(self.card_lines)

        element_id = 1
        node1_id = ''
        n_card = len(self.cards)
        for i in range(n_card):
            card = self.cards[i]
            if card.title == 'ANCH':
                if node1_id == '':
                    node1_id = card.properties.get('PT')
                    self.model.add_node(Node(node1_id))
            elif card.title == 'JUNC':
                node1_id = card.properties.get('PT')
            elif card.title == 'TANG' or card.title == 'BRAN' or card.title == 'CRED':
                node1 = self.model.get_node(node1_id)
                x1 = node1.x
                y1 = node1.y
                z1 = node1.z
                node2_id = card.properties.get('PT')
                dx = float(card.properties.get('DX', '0'))
                dy = float(card.properties.get('DY', '0'))
                dz = float(card.properties.get('DZ', '0'))
                x2 = x1 + dx
                y2 = y1 + dy
                z2 = z1 + dz
                self.model.add_node(Node(node2_id, x2, y2, z2))
                self.model.add_element(Element(str(element_id), 'TANG', [node1_id, node2_id]))
                element_id += 1
                node1_id = node2_id
            elif card.title == 'BEND':
                node1 = self.model.get_node(node1_id)
                x1 = node1.x
                y1 = node1.y
                z1 = node1.z
                node2_id = card.properties.get('PT')
                dx1 = float(card.properties.get('X1', '0'))
                dy1 = float(card.properties.get('Y1', '0'))
                dz1 = float(card.properties.get('Z1', '0'))
                x_tangent = x1 + dx1
                y_tangent = y1 + dy1
                z_tangent = z1 + dz1
                dx2 = float(card.properties.get('X2', '0'))
                dy2 = float(card.properties.get('Y2', '0'))
                dz2 = float(card.properties.get('Z2', '0'))
                x2 = x_tangent + dx2
                y2 = y_tangent + dy2
                z2 = z_tangent + dz2
                self.model.add_node(Node(node2_id, x2, y2, z2))
                self.model.add_element(Element(str(element_id), 'BEND', [node1_id, node2_id]))
                element_id += 1
                node1_id = node2_id

    def show(self):
        # 添加节点
        points = vtkPoints()
        node_index = 0
        for node_id in self.model.nodes:
            node = self.model.nodes.get(node_id)
            x = node.x
            y = node.y
            z = node.z
            self.node_mapping[node_id] = node_index
            points.InsertPoint(node_index, x, y, z)
            node_index += 1

        grid = vtkUnstructuredGrid()
        for element_id in self.model.elements:
            element = self.model.elements.get(element_id)
            element_type = element.type
            elem_type = VTK_LINE
            if element_type in ['TANG', 'BEND', 'BRAN', 'CRED']:
                elem_type = VTK_LINE
            connection = element.connection
            connection_index = [self.node_mapping[node_id] for node_id in connection]
            grid.InsertNextCell(elem_type, len(connection_index), connection_index)
        grid.SetPoints(points)

        mapper = vtkDataSetMapper()
        mapper.SetInputData(grid)

        actor = vtkActor()
        actor.SetMapper(mapper)

        renderer = vtkRenderer()
        renderer.AddActor(actor)

        win = vtkRenderWindow()
        win.SetSize(640, 640)
        win.AddRenderer(renderer)
        win.Render()

        style = vtkInteractorStyleTrackballCamera()
        iren = vtkRenderWindowInteractor()
        iren.SetInteractorStyle(style)
        iren.SetRenderWindow(win)
        iren.Start()


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('filename')
    given_args = arg_parser.parse_args()
    peps_file = given_args.filename
    peps_parser = PepsParser(peps_file)
    peps_parser.parse()
    peps_parser.show()
