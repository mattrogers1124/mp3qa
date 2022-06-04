--
-- File generated with SQLiteStudio v3.3.3 on Sat Jun 4 16:11:35 2022
--
-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: Files
DROP TABLE IF EXISTS Files;

CREATE TABLE Files (
    path   TEXT    PRIMARY KEY,
    format TEXT,
    size   INTEGER
);


-- Table: Headers_FLAC
DROP TABLE IF EXISTS Headers_FLAC;

CREATE TABLE Headers_FLAC (
    path            TEXT    REFERENCES Files (path) ON DELETE CASCADE
                                                    ON UPDATE CASCADE
                            PRIMARY KEY,
    bitrate         INTEGER,
    bits_per_sample INTEGER,
    channels        INTEGER,
    code            INTEGER,
    length          REAL,
    max_blocksize   INTEGER,
    max_framesize   INTEGER,
    md5_signature   TEXT,
    min_blocksize   INTEGER,
    min_framesize   INTEGER,
    sample_rate     INTEGER,
    total_samples   INTEGER
);


-- Table: Headers_MP3
DROP TABLE IF EXISTS Headers_MP3;

CREATE TABLE Headers_MP3 (
    path             TEXT    REFERENCES Files (path) ON DELETE CASCADE
                                                     ON UPDATE CASCADE
                             PRIMARY KEY,
    album_gain       REAL,
    album_peak       REAL,
    bitrate          INTEGER,
    bitrate_mode     TEXT,
    channels         INTEGER,
    encoder_info     TEXT,
    encoder_settings TEXT,
    frame_offset     INTEGER,
    layer            INTEGER,
    length           REAL,
    mode             INTEGER,
    padding          INTEGER,
    protected        INTEGER,
    sample_rate      INTEGER,
    sketchy          INTEGER,
    track_gain       REAL,
    track_peak       REAL,
    version          INT
);


-- Table: Tags
DROP TABLE IF EXISTS Tags;

CREATE TABLE Tags (
    path       REFERENCES Files (path),
    tag   TEXT,
    value TEXT
);


-- View: AlbumInfo
DROP VIEW IF EXISTS AlbumInfo;
CREATE VIEW AlbumInfo AS
    SELECT albumartist,
           album,
           COUNT( * ) AS tracks,
           time(sum(length), 'unixepoch') AS total_length,
           GROUP_CONCAT(DISTINCT format) AS format,
           sum(size) AS total_size,
           GROUP_CONCAT(DISTINCT sample_rate) AS sample_rate,
           GROUP_CONCAT(DISTINCT bitrate_mode) AS bitrate_mode,
           MIN(bitrate) AS bitrate_min,
           MAX(bitrate) AS bitrate_max
      FROM FileInfo
     WHERE albumartist IS NOT NULL AND
           album IS NOT NULL
     GROUP BY albumartist,
              album;


-- View: FileInfo
DROP VIEW IF EXISTS FileInfo;
CREATE VIEW FileInfo AS
    SELECT f.path,
           t.artist,
           t.albumartist,
           t.album,
           t.disc,
           t.track,
           t.title,
           f.format,
           f.size,
           CASE WHEN f.format = 'mp3' THEN em.length WHEN f.format = 'flac' THEN ef.length ELSE NULL END AS length,
           CASE WHEN f.format = 'mp3' THEN em.bitrate_mode ELSE NULL END AS bitrate_mode,
           CASE WHEN f.format = 'mp3' THEN em.bitrate WHEN f.format = 'flac' THEN ef.bitrate ELSE NULL END AS bitrate,
           CASE WHEN f.format = 'mp3' THEN em.sample_rate WHEN f.format = 'flac' THEN ef.sample_rate ELSE NULL END AS sample_rate
      FROM Files f
           LEFT JOIN
           Headers_FLAC ef ON f.path = ef.path
           LEFT JOIN
           Headers_MP3 em ON f.path = em.path
           LEFT JOIN
           (
               SELECT path,
                      IFNULL(MAX(IIF(tag IN ('TSOP', 'artistsort'), value, NULL) ), MAX(IIF(tag IN ('TPE1', 'artist'), value, NULL) ) ) AS artist,
                      IFNULL(MAX(IIF(tag IN ('TSO2', 'albumartistsort'), value, NULL) ), MAX(IIF(tag IN ('TPE2', 'albumartist'), value, NULL) ) ) AS albumartist,
                      MAX(IIF(tag IN ('TALB', 'album'), value, NULL) ) AS album,
                      MAX(IIF(tag IN ('TPOS', 'discnumber'), value, NULL) ) AS disc,
                      MAX(IIF(tag IN ('TRCK', 'tracknumber'), value, NULL) ) AS track,
                      MAX(IIF(tag IN ('TIT2', 'title'), value, NULL) ) AS title
                 FROM Tags
                GROUP BY path
           )
           t ON f.path = t.path;


-- View: TagCounts
DROP VIEW IF EXISTS TagCounts;
CREATE VIEW TagCounts AS
    SELECT f.format,
           t.tag,
           count( * ) AS count
      FROM Tags t
           LEFT JOIN
           Files f ON t.path = f.path
     GROUP BY f.format,
              t.tag;


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
