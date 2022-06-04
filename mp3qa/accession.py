import sqlite3
from .extract import extract
from .load import load


# Given an MP3/FLAC file and database connection, extract the file's metadata and load it into the database.
# This is basically just a pipeline that connects the .extract and .load methods

def accession(path: str, con: sqlite3.Connection, basedir: str = None, verbose: bool = True):
    if verbose:
        print(f'Accessioning: {path}')
    file_data, header_data, tag_data = extract(path, basedir)
    load(file_data, header_data, tag_data, con)
