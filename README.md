# mp3qa

`mp3qa` is a Python package for extraction and analysis of data
from a personal music library.


## Dependencies

`mp3qa` requires the `mutagen` package
to read and write MP3 and FLAC file metadata.


## Background

I wrote this package to help with upkeep of my aging MP3 collection.
My music files came from many sources over a period of about 20 years.
The level of quality varied wildly due to extreme compression,
artifacts accumulated from transcoding, and so on.

I wanted to weed out or replace files of poor quality.
I also wanted to set up a quality control process for newly-acquired files.
The `mp3qa` package provides methods to automate some tedious processes:

* Extract data from MP3 file headers and ID3 tags, and load into a SQLite3 database
* Delete cover art and other extraneous data from ID3 tags

Since I started this project, I added support for FLAC files:

* As above, extract headers and metadata and delete extraneous metadata
* Create spectrograms using `ffmpeg`


## Usage

### Set up a database for extraction
Use the `init_db()` method to initialize a SQLite3 database
containing the necessary tables and some useful views.
The method returns a `sqlite3.Connection` object,
which connects to a database specified in the argument.

It's recommended to use a new database here,
as data in an existing database **will be dropped**.

```python
import os
from mp3qa import init_db
dbpath = os.path.expanduser('~/Desktop/music.sqlite3')
with init_db(dbpath) as con:
    ...
```

### Extract data into the database
Use the `batch_accession()` method to scrape data from your music files.
This method takes the following arguments:

* `basedir: str` The base directory of your music library.
  The method walks through this directory recursively, scraping MP3 and FLAC files.

* `con: sqlite3.Connection` Connection to a SQLite3 database.
  Use the one you get from the `init_db()` method above.

* `verbose: bool` Whether to print progress to `sys.stdout`.
  Defaults to `True`.

```python
import os
from mp3qa import init_db, batch_accession
dbpath = os.path.expanduser('~/Desktop/music.sqlite3')
musicpath = os.path.expanduser('~/Music')
with init_db(dbpath) as con:
    batch_accession(basedir=musicpath, con=con, verbose=True)
```

Once you've done this, you can interact with the database however you'd like.
The database comes with some useful views:

* `FileInfo` Compiles data from the headers and metadata tags for each file.
* `AlbumInfo` Takes the data from `FileInfo` and summarizes it by album.
* `TagCount` Counts how many files each metadata tag appears in.

For example, to identify which of my MP3 albums are most in need of replacing,
I might run a query like the following:

```sqlite-sql
SELECT *
  FROM AlbumInfo
 WHERE format = 'mp3' AND 
       bitrate_max <= 192000
 ORDER BY bitrate_max;
```

### Scrub extraneous metadata
Use the `batch_scrub_albumart()` method to delete attached pictures
in the metadata of your music library.
Use the `batch_scrub_metadata()` method to delete all metadata
except for basic info (artist, album name, track title, etc.)

These methods **destroy data** in your music files, so use with caution.
Each method comes with a `dryrun` option.
If `dryrun=True` is passed in, the method will not save changes to the files.

```python
import os
from mp3qa import batch_scrub_metadata
musicdir = os.path.expanduser('~/Music-Intake')
batch_scrub_metadata(basedir=musicdir, dryrun=False, verbose=True)
```

### Create spectrograms
Use the `batch_spectrogram()` method to create spectrograms using `ffmpeg`
for all of your music files.
This method takes the following arguments:

* `input_basedir: str` The base directory of your music library.
  The method walks through this directory recursively, scraping MP3 and FLAC files.

* `output_basedir: str` The directory where you want the spectrograms saved.

* `size: Tuple[int, int]` Size of the spectrogram in pixels.  Defaults to `(256, 256)`.

* `read_flac: bool` Whether to read FLAC files. Defaults to `True`.

* `read_mp3: bool` Whether to read MP3 files. Defaults to `False`.

* `verbose: bool` Whether to print progress to `sys.stdout`.

```python
import os
from mp3qa import batch_spectrogram
musicdir = os.path.expanduser('~/Music')
specdir = os.path.expanduser('~/Desktop/spectrograms')
batch_spectrogram(input_basedir=musicdir, output_basedir=specdir,
                  size=(256, 256), read_flac=True, read_mp3=False, verbose=True)
```

The method recursively recreates the directory structure below `input_basedir`.
So if your input directory contains these music files:
```
input_basedir/artist/album/track_01.flac
input_basedir/artist/album/track_02.flac
input_basedir/artist/album/track_03.flac
...
```

Then the method will save these image files:
```
output_basedir/artist/album/track_01.flac.png
output_basedir/artist/album/track_02.flac.png
output_basedir/artist/album/track_03.flac.png
...
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
