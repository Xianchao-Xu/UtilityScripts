import wave

import numpy as np


def data2audio(filename):
    with open(filename, 'r') as fr:
        num_cols = len(fr.readline().split())

    num_channels = num_cols - 1  # 声道数
    time_data = np.loadtxt(filename, usecols=(0, ), delimiter=',')
    frame_rate = int(len(time_data) / time_data[-1])

    if num_channels == 1:
        wave_data = np.loadtxt(filename, usecols=(1,), delimiter=',', dtype=np.short)
    else:
        wave_data = np.loadtxt(filename, usecols=(1, 2), delimiter=',', dtype=np.short)

    out_file = filename.replace('.dat', '')
    out_file += '.wav'
    with wave.open(out_file, 'wb') as audio:
        audio.setnchannels(num_channels)
        audio.setsampwidth(2)
        audio.setframerate(frame_rate)
        audio.writeframes(wave_data.tobytes())


if __name__ == '__main__':
    data2audio('单通道测试数据.dat')
    data2audio('双通道测试数据.dat')
