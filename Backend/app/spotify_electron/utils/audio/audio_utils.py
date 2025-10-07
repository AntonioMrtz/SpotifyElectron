import sys


import puremagic
import mutagen
import subprocess
from io import BytesIO


# ------------------------------- HELPER FUNCTIONS -------------------------------

# checking file type - using magic numbers
def check_file_type(file: bytes) -> bool:
    all_ext = [".mp3", ".wav", ".flac", ".ogg", ".m4a", ".aac", ".wma", ".aiff"]

    file_ext = puremagic.from_string(file)

    if type(file_ext) != str: # when not string -> List
        file_ext = [e.lower() for e in file_ext] # convert to lowercase if uppercase (for weird cases)
        for ext in file_ext:
            if ext in all_ext:
                return True # all good
    
    else: # when string
        if file_ext.lower() in all_ext: 
                return True # all good

    return False # raise error

# checking file size
def check_file_size(file: bytes) -> bool:
    max_size = 10 * pow(2,20) # 10MB

    if len(file) > max_size:
        return False # raise error
    
    return True

# stripping the metadata
def strip_metadata(file: bytes, output_format: str = "mp3") -> bytes:
    if not file or len(file) == 0:
        raise ValueError("File is empty. cannot strip metadata")
    
    input_bytes = BytesIO(file) # file buffer

    command  = [
        "ffmpeg",
        "-y", # overwrite output if needed
        "-i", "pipe:0", # read from stdin
        "-map_metadata", "-1", # remove all metadata
        "-c:a", "copy", # copy the stream as it is into a container (.mp3 in this case)
        "-f", output_format, # output, output format
        "pipe:1" # write to stdout
        ]
    
    try: 
        file_input_bytes = mutagen.File(input_bytes)
        
        if not file_input_bytes or not file_input_bytes.tags: # no metadata
            return file # return file as it is
    
    except Exception:
        pass 
        
    # cursor to start
    input_bytes.seek(0)
    # run ffmpeg with subprocess
    result = subprocess.run(
        command,
        input=input_bytes.read(),   # send input bytes
        stdout=subprocess.PIPE,     # capture output bytes
        stderr=subprocess.PIPE      # capture errors for debugging
    )

    if result.returncode != 0:
        # ffmpeg failed
        raise RuntimeError(f"FFmpeg failed: {result.stderr.decode()}")

    # return the cleaned audio bytes
    return result.stdout


# re-encoding bytes to mp3 from any other extension
def reencode_audio(file: bytes, output_format: str = "mp3") -> bytes:
    if not file or len(file) == 0:
        raise ValueError("File is empty. Cannot reencode")
    
    input_bytes = BytesIO(file)

    command = [
        "ffmpeg",
        "-i", "pipe:0",
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        "-ar", "44100",
        "-ac", "2",
        "-f" , output_format,
        "pipe:1"
        ]

    result = subprocess.run(
        command,
        input = input_bytes.read(),
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
        
    )

    if result.returncode != 0:
        # ffmpeg failed
        raise RuntimeError(f"FFmpeg failed: {result.stderr.decode()}")

    # return the cleaned audio bytes
    return result.stdout

# ---------------------------- END OF HELPER FUNCTIONS ------------------------------

# song sanitizer func
def sanitize_audio(file: bytes) -> bytes:

    if not file or len(file) == 0:
        raise ValueError("File is empty")

    if not check_file_type(file):
        raise ValueError("Wrong file type")

    if not check_file_size(file):
        raise ValueError("File size is too large. max 10MB allowed")

    stripped_metadata_bytes = strip_metadata(file)

    if puremagic.from_string(stripped_metadata_bytes).lower() != ".mp3": # if extension is not .mp3
        return reencode_audio(stripped_metadata_bytes) # re-encoded bytes to (dot)mp3
    
    return stripped_metadata_bytes # when extension is .mp3







