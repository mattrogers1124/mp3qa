import os
from mp3qa import batch_scrub_metadata


if __name__ == '__main__':
    musicdir = os.path.expanduser('~/Music-Intake')
    batch_scrub_metadata(basedir=musicdir, dryrun=True, verbose=True)
