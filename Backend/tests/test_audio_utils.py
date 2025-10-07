import sys, os


import io


import mutagen


from app.spotify_electron.utils.audio.audio_utils import check_file_size, check_file_type, strip_metadata, reencode_audio, sanitize_audio


file = open(r"C:\Users\admin\Desktop\all projects\SpotifyElectron\Backend\tests\assets\song_4_seconds.mp3", "rb")
fake = r"this is fake audio byte file" # fake byte file for testing
empty = r"" # empty file for testing

text = file.read()

"""
CHECK FILE SIZE

--- test1 ---
if check_file_size(text):
    print("file size is okay")
else:
    print("file size is too big")

--- test2 ---
if check_file_size(fake):
    print("file size is okay")
else:
    print("file size is too big")

"""


"""
CHECK FILE TYPE

--- test1 ---
if check_file_type(text):
    print("file type is audio, nothing malicious")
else:
    print("nope, file type is not audio")

--- test2 ---
if check_file_type(fake):
    print("file type is audio, nothing malicious")
else:
    print("nope, file type is not audio")

"""


"""
TEST strip_metadata()

--- test1 ---
original_audio = mutagen.File(io.BytesIO(text))
print("Original metadata:", original_audio.tags)

cleaned_bytes = strip_metadata(file)

cleaned_audio = mutagen.File(io.BytesIO(cleaned_bytes))
print("After stripping:", cleaned_audio.tags)

--- test2 ---
original_audio = mutagen.File(io.BytesIO(empty))
print("Original metadata:", original_audio.tags)

cleaned_bytes = strip_metadata(file)

cleaned_audio = mutagen.File(io.BytesIO(cleaned_bytes))
print("After stripping:", cleaned_audio.tags)


"""


"""
TEST reencode_audio()

--- test1 ---
reencoded_bytes = reencode_audio(text)

if puremagic.from_string(stripped_metadata_bytes).lower() != ".mp3":
    print("file reencoded")
else:
    print("nope, file could not reencode")

--- test1 ---
reencoded_bytes = reencode_audio(empty)

if puremagic.from_string(stripped_metadata_bytes).lower() != ".mp3":
    print("file reencoded")
else:
    print("nope, file could not reencode")

"""

