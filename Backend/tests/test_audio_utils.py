import sys, os


import io


import mutagen


from app.spotify_electron.utils.audio.audio_utils import check_file_size, check_file_type, strip_metadata, reencode_audio, sanitize_audio


file = open(r"C:\Users\admin\Desktop\all projects\SpotifyElectron\Backend\tests\assets\song_4_seconds.mp3", "rb")
fake = r"this is fake audio byte file"

text = file.read()

"""
CHECK FILE SIZE

if check_file_size(text):
    print("file size is okay")
else:
    print("file size is too big")

"""


"""
CHECK FILE TYPE

if check_file_type(text):
    print("file type is audio, nothing malicious")
else:
    print("nope, file type is not audio")

"""


"""
TEST strip_metadata()

original_audio = mutagen.File(io.BytesIO(text))
print("Original metadata:", original_audio.tags)

cleaned_bytes = strip_metadata(file)

cleaned_audio = mutagen.File(io.BytesIO(cleaned_bytes))
print("After stripping:", cleaned_audio.tags)

"""


"""
TEST reencode_audio()

reencoded_bytes = reencode_audio(text)

if check_file_type(reencoded_bytes):
    print("file type is audio, nothing malicious")
else:
    print("nope, file type is not audio")

"""

