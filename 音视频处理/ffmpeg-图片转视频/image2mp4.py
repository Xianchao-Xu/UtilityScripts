#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ffmpeg

jpeg_files = [
    'images/网格场景_1_mesh_00005.png',
    'images/网格场景_1_mesh_00010.png',
    'images/网格场景_1_mesh_00015.png',
    'images/网格场景_1_mesh_00020.png',
    'images/网格场景_1_mesh_00025.png',
    'images/网格场景_1_mesh_00030.png',
    'images/网格场景_1_mesh_00035.png',
    'images/网格场景_1_mesh_00040.png',
    'images/网格场景_1_mesh_00045.png',
    'images/网格场景_1_mesh_00050.png',
    'images/网格场景_1_mesh_00055.png',
    'images/网格场景_1_mesh_00060.png',
    'images/网格场景_1_mesh_00065.png',
    'images/网格场景_1_mesh_00070.png',
    'images/网格场景_1_mesh_00075.png',
    'images/网格场景_1_mesh_00080.png',
    'images/网格场景_1_mesh_00085.png',
    'images/网格场景_1_mesh_00090.png',
    'images/网格场景_1_mesh_00095.png',
    'images/网格场景_1_mesh_00100.png',
    'images/网格场景_1_mesh_00105.png',
    'images/网格场景_1_mesh_00110.png',
    'images/网格场景_1_mesh_00115.png',
    'images/网格场景_1_mesh_00120.png',
    'images/网格场景_1_mesh_00125.png',
    'images/网格场景_1_mesh_00130.png',
    'images/网格场景_1_mesh_00135.png',
    'images/网格场景_1_mesh_00140.png',
    'images/网格场景_1_mesh_00145.png',
    'images/网格场景_1_mesh_00150.png',
    'images/网格场景_1_mesh_00155.png',
    'images/网格场景_1_mesh_00160.png',
    'images/网格场景_1_mesh_00165.png',
    'images/网格场景_1_mesh_00170.png',
    'images/网格场景_1_mesh_00175.png',
    'images/网格场景_1_mesh_00180.png',
    'images/网格场景_1_mesh_00185.png',
    'images/网格场景_1_mesh_00190.png',
    'images/网格场景_1_mesh_00195.png',
    'images/网格场景_1_mesh_00200.png',
    'images/网格场景_1_mesh_00205.png',
    'images/网格场景_1_mesh_00210.png',
    'images/网格场景_1_mesh_00215.png',
    'images/网格场景_1_mesh_00220.png',
    'images/网格场景_1_mesh_00225.png',
    'images/网格场景_1_mesh_00230.png',
    'images/网格场景_1_mesh_00235.png',
    'images/网格场景_1_mesh_00240.png',
    'images/网格场景_1_mesh_00245.png',
    'images/网格场景_1_mesh_00250.png',
]

process = (ffmpeg
           .input('pipe:', r='20', f='image2pipe')
           .output('videos/video.mp4', vcodec='libx264')
           .overwrite_output()
           .run_async(pipe_stdin=True)
           )

for in_file in jpeg_files:
    with open(in_file, 'rb') as f:
        jpeg_data = f.read()
        process.stdin.write(jpeg_data)

process.stdin.close()
process.wait()
