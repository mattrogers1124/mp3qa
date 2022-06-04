# Delete extraneous metadata from MP3 and FLAC files.
# CAUTION: The methods in this module DESTROY DATA. Use with caution!
import os
from mutagen.id3 import ID3
from mutagen.flac import FLAC


# Delete almost all metadata tags, keeping only basic identifying information
def scrub_metadata(path: str, dryrun: bool = False, verbose: bool = False):
    extension = os.path.splitext(path)[1].lower()

    # Save these tags
    safe_tags_mp3 = ['TALB', 'TDRC', 'TIT2', 'TPE1', 'TPE2', 'TPOS', 'TRCK', 'TSO2', 'TSOP']
    safe_tags_flac = ['album', 'albumartist', 'albumartistsort', 'artist', 'artistsort', 'date', 'discnumber',
                      'disctotal', 'title', 'totaldiscs', 'totaltracks', 'tracknumber', 'tracktotal']

    if extension == '.mp3':
        file = ID3(path)
        tags_to_delete = [tag for tag in file.keys() if tag not in safe_tags_mp3]
        if verbose:
            print(f'Found {len(tags_to_delete)} tag(s) to delete in file {path}')
        if tags_to_delete:
            for tag in tags_to_delete:
                file.delall(tag)
            if not dryrun:
                file.save()

    if extension == '.flac':
        file = FLAC(path)
        tags_to_delete = [tag for tag in file.keys() if tag not in safe_tags_flac]
        if verbose:
            print(f'Found {len(tags_to_delete)} tag(s) and {len(file.pictures)} pic(s) to delete in file {path}')
        if tags_to_delete or len(file.pictures):
            for tag in tags_to_delete:
                file.pop(tag)
            file.clear_pictures()
            if not dryrun:
                file.save()


# Delete just the album art
def scrub_albumart(path: str, dryrun: bool = False, verbose: bool = False):
    extension = os.path.splitext(path)[1].lower()
    if extension == '.mp3':
        file = ID3(path)
        apic_tags = [str(tag) for tag in file.keys() if str(tag).upper().startswith('APIC')]
        if verbose:
            print(f'Found {len(apic_tags)} APIC tag(s) in file {path}')
        if len(apic_tags) > 0:
            for tag in apic_tags:
                file.delall(tag)
            if not dryrun:
                file.save()

    if extension == '.flac':
        file = FLAC(path)
        if verbose:
            print(f'Found {len(file.pictures)} picture(s) in file {path}')
        if file.pictures:
            file.clear_pictures()
            if not dryrun:
                file.save()


if __name__ == '__main__':
    basedir = '/home/sutter/Music-Intake/'
    for root, dirs, files in os.walk(basedir):
        print(root)
        for file in files:
            if os.path.splitext(file)[1].lower() in ['.mp3', '.flac']:
                scrub_metadata(os.path.join(root, file), dryrun=True, verbose=True)
