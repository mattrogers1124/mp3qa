# Provides dataclasses used in the mp3qa.extract and mp3qa.load modules

from dataclasses import dataclass


@dataclass
class FileData:
    path: str
    format: str
    size: int


@dataclass
class HeaderData:
    path: str
    bitrate: int
    channels: int
    sample_rate: int
    length: float


@dataclass
class MP3HeaderData(HeaderData):
    album_gain: float
    album_peak: float
    bitrate_mode: str
    encoder_info: str
    encoder_settings: str
    frame_offset: int
    layer: int
    mode: int
    padding: int
    protected: int
    sketchy: int
    track_gain: float
    track_peak: float
    version: int


@dataclass
class FLACHeaderData(HeaderData):
    bits_per_sample: int
    code: int
    max_blocksize: int
    max_framesize: int
    md5_signature: str
    min_blocksize: int
    min_framesize: int
    total_samples: int


@dataclass
class TagData:
    path: str
    tag: str
    value: str
