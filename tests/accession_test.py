import os
from mp3qa import init_db, batch_accession


if __name__ == '__main__':
    dbpath = os.path.expanduser('~/Desktop/music.sqlite3')
    musicpath = os.path.expanduser('~/Music')
    with init_db(dbpath) as con:
        batch_accession(basedir=musicpath, con=con, verbose=True)
