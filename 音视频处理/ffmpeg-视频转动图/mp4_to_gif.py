#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ffmpeg

out, _ = (ffmpeg
          .input('video.mp4')
          .output('video.gif')
          .overwrite_output()
          .run()
          )
