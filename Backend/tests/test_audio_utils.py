import io
import pytest
from app.spotify_electron.utils.audio.audio_utils import (
    check_file_size,
    check_file_type,
    strip_metadata,
    reencode_audio,
    sanitize_audio
)


with open(r"C:\Users\admin\Desktop\all projects\SpotifyElectron\Backend\tests\assets\song_4_seconds.mp3", "rb") as f:
    real_audio_bytes = f.read()

fake_bytes = b"this is not audio"
empty_bytes = b""

# ----------------- CHECK FILE SIZE -----------------
def test_check_file_size_real_audio():
    assert check_file_size(real_audio_bytes) is True

def test_check_file_size_empty_file():
    assert check_file_size(empty_bytes) is True

# ----------------- CHECK FILE TYPE -----------------
def test_check_file_type_real_audio():
    assert check_file_type(real_audio_bytes) is True

def test_check_file_type_fake_audio():
    assert check_file_type(fake_bytes) is False

# ----------------- STRIP METADATA -----------------
def test_strip_metadata_removes_tags():
    cleaned = strip_metadata(real_audio_bytes)
    # If metadata existed, the bytes should change
    assert isinstance(cleaned, bytes)
    assert cleaned != real_audio_bytes

def test_strip_metadata_empty_file():
    cleaned = strip_metadata(empty_bytes)
    assert cleaned == empty_bytes  # nothing to strip

# ----------------- REENCODE AUDIO -----------------
def test_reencode_audio_returns_bytes():
    reencoded = reencode_audio(real_audio_bytes)
    assert isinstance(reencoded, bytes)

# ----------------- SANITIZE AUDIO -----------------
def test_sanitize_audio_real_audio():
    sanitized = sanitize_audio(real_audio_bytes)
    assert isinstance(sanitized, bytes)

def test_sanitize_audio_fake_audio():
    with pytest.raises(ValueError, match="wrong file type"):
        sanitize_audio(fake_bytes)

def test_sanitize_audio_empty_file():
    sanitized = sanitize_audio(empty_bytes)
    assert isinstance(sanitized, bytes)