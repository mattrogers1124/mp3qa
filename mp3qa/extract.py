import os
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from .data import FileData, MP3HeaderData, FLACHeaderData, TagData


# Given a path to an MP3 or FLAC file, returns three data objects
#   1. FileData: Filesystem information about the file
#   2. MP3HeaderData or FLACHeaderData: Information about how the audio in the file is encoded
#   3. List[TagData]: Descriptive metadata tags about the audio

def extract(path: str, basedir: str = None):
    # Verify the path exists
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    # Verify the path is a file
    if not os.path.isfile(path):
        raise RuntimeError(f'{path} is not a file')

    # Verify the file extension is .mp3 or .flac
    extension = os.path.splitext(path)[1].lower()
    if extension not in ['.mp3', '.flac']:
        raise RuntimeError(f'{path} is not an MP3 or FLAC file')

    # Create a FileData object
    file_data = FileData(
        path=os.path.relpath(path, basedir),
        format=extension[1:],
        size=os.path.getsize(path)
    )
    
    # Create defaults for header and tag data objects
    header_data, tag_data = None, []

    if extension == '.mp3':
        header_data, tag_data = mp3_data(path, basedir)

    if extension == '.flac':
        header_data, tag_data = flac_data(path, basedir)

    return file_data, header_data, tag_data


# Returns two dicts with (1) header data and (2) metadata tags for MP3 files
def mp3_data(path: str, basedir: str = None):
    with open(path, 'br') as file:
        f = MP3(file)
        header_data = MP3HeaderData(
            path=os.path.relpath(path, basedir),
            album_gain=f.info.album_gain,
            album_peak=f.info.album_peak,
            bitrate=f.info.bitrate,
            bitrate_mode=str(f.info.bitrate_mode).replace('BitrateMode.', ''),
            channels=f.info.channels,
            encoder_info=f.info.encoder_info,
            encoder_settings=f.info.encoder_settings,
            frame_offset=f.info.frame_offset,
            layer=f.info.layer,
            length=f.info.length,
            mode=f.info.mode,
            padding=f.info.padding,
            protected=f.info.protected,
            sample_rate=f.info.sample_rate,
            sketchy=f.info.sketchy,
            track_gain=f.info.track_gain,
            track_peak=f.info.track_peak,
            version=f.info.version
        )
        
        tag_data = [
            TagData(
                path=header_data.path,
                tag=tag,
                value=str(f[tag]))
            for tag in f.keys() if not tag.startswith('APIC')
        ]
        
    return header_data, tag_data


# Returns two dicts with (1) header data and (2) metadata tags for FLAC files
def flac_data(path: str, basedir: str = None):
    with open(path, 'br') as file:
        f = FLAC(file)
        header_data = FLACHeaderData(
            path=os.path.relpath(path, basedir),
            bitrate=f.info.bitrate,
            bits_per_sample=f.info.bits_per_sample,
            channels=f.info.channels,
            code=f.info.code,
            length=f.info.length,
            max_blocksize=f.info.max_blocksize,
            max_framesize=f.info.max_framesize,
            md5_signature=str(f.info.md5_signature),
            min_blocksize=f.info.min_blocksize,
            min_framesize=f.info.min_framesize,
            sample_rate=f.info.sample_rate,
            total_samples=f.info.total_samples
        )
        tag_data = [TagData(path=header_data.path, tag=tag, value=str(f[tag][0])) for tag in f.keys()]

    return header_data, tag_data
