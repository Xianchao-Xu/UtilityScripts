#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio

import edge_tts

TEXT = "大家好，我是悬臂梁!"
VOICE = "zh-CN-YunxiaNeural"
# VOICE2 = "zh-CN-YunyangNeural"
OUTPUT_FILE = "test.mp3"


async def _main() -> None:
    communicate = edge_tts.Communicate(TEXT, VOICE)
    await communicate.save(OUTPUT_FILE)


if __name__ == "__main__":
    asyncio.new_event_loop().run_until_complete(_main())
