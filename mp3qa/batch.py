# Methods for scraping and editing metadata in batches

import os
import sqlite3
from typing import Tuple
from .init_db import init_db
from .accession import accession
from .scrub import scrub_metadata, scrub_albumart
from .spectrogram import spectrogram


__all__ = ['batch_accession', 'batch_scrub_metadata', 'batch_scrub_albumart', 'batch_spectrogram']


def batch_accession(basedir: str, con: sqlite3.Connection, verbose: bool = True):
    for root, dirs, files in os.walk(basedir):
        if verbose:
            print(root)
        for file in files:
            if os.path.splitext(file)[1].lower() in ['.mp3', '.flac']:
                accession(path=os.path.join(root, file), con=con, basedir=basedir, verbose=verbose)
        con.commit()


def batch_scrub_metadata(basedir: str, dryrun: bool = False, verbose: bool = True):
    for root, dirs, files in os.walk(basedir):
        if verbose:
            print(root)
        for file in files:
            if os.path.splitext(file)[1].lower() in ['.mp3', '.flac']:
                scrub_metadata(path=os.path.join(root, file), dryrun=dryrun, verbose=verbose)


def batch_scrub_albumart(basedir: str, dryrun: bool = False, verbose: bool = True):
    for root, dirs, files in os.walk(basedir):
        if verbose:
            print(root)
        for file in files:
            if os.path.splitext(file)[1].lower() in ['.mp3', '.flac']:
                scrub_albumart(path=os.path.join(root, file), dryrun=dryrun, verbose=verbose)


def batch_spectrogram(input_basedir: str, output_basedir: str, size: Tuple[int, int] = (512, 512),
                      read_flac: bool = True, read_mp3: bool = False, verbose: bool = True):

    # Input directory must exist
    if not os.path.isdir(input_basedir):
        raise FileNotFoundError(input_basedir)

    # Keep track of new directories created
    created_dirs = []

    # Create the output base directory if needed
    if not os.path.isdir(output_basedir):
        os.mkdir(output_basedir)
        created_dirs.append(output_basedir)

    # List the file extensions we're searching for
    extensions = []
    if read_flac:
        extensions.append('.flac')
    if read_mp3:
        extensions.append('.mp3')

    # Walk through the input directory
    for root, dirs, files in os.walk(input_basedir):
        # Get the path of the output directory, which we will create if needed
        output_root = os.path.join(output_basedir, os.path.relpath(root, input_basedir))
        if not os.path.isdir(output_root):
            os.mkdir(output_root)
            created_dirs.append(output_root)

        # Iterate through files in this directory
        for file in files:
            if os.path.splitext(file)[1].lower() in extensions:

                # Use FFMPEG to generate the spectrogram
                input_file = os.path.join(root, file)
                output_file = os.path.join(output_root, file) + '.png'
                spectrogram(input_file=input_file, output_file=output_file, size=size, verbose=verbose)

    # Clean up the created directories
    for dir in sorted(created_dirs, reverse=True):
        if not os.listdir(dir):
            if verbose:
                print(f'Deleting empty directory {dir}')
            os.rmdir(dir)
