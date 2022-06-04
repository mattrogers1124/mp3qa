# Use FFMPEG to generate a spectrogram. Useful for checking quality of FLAC files.

import os


def spectrogram(input_file: str, output_file: str, size: tuple = (512, 512), verbose: bool = False):
    command = f'ffmpeg -hide_banner -loglevel error -i "{input_file}" -lavfi showspectrumpic=s={size[0]}x{size[1]} "{output_file}"'
    if verbose:
        print(command)
    os.system(command)
