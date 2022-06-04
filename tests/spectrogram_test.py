import os
from mp3qa import batch_spectrogram


if __name__ == '__main__':
    batch_spectrogram(
        input_basedir=os.path.expanduser('~/Music'),
        output_basedir=os.path.expanduser('~/Desktop/spectrograms')
    )
