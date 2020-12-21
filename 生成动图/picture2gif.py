# coding: utf-8
# author: xuxc
from PIL import Image


def picture2gif_by_pillow(base_name, start, end, interval=1, output='out.gif'):
    frames = []
    images = [base_name.format(i) for i in range(start, end+1, interval)]
    for image in images:
        frame = Image.open(image)
        frames.append(frame)

    frames[0].save(output, format='GIF', append_images=frames[1:],
                   save_all=True, duration=300, loop=0)


if __name__ == '__main__':
    picture2gif_by_pillow('images/pressure_{:05d}.png', 5, 60, 5, 'images/out.gif')
