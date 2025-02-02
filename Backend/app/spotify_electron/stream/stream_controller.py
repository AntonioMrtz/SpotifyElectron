"""
Stream controller for handling song audio streaming
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import StreamingResponse
from starlette.status import (
    HTTP_206_PARTIAL_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

import app.spotify_electron.stream.stream_service as stream_service
from app.auth.auth_schema import TokenData
from app.auth.JWTBearer import JWTBearer
from app.common.PropertiesMessagesManager import PropertiesMessagesManager
from app.spotify_electron.song.base_song_schema import (
    SongBadNameError,
    SongNotFoundError,
)
from app.spotify_electron.song.blob.song_schema import SongDataNotFoundError
from app.spotify_electron.stream.stream_schema import (
    InvalidContentRangeStreamError,
    StreamServiceError,
)

router = APIRouter(
    prefix="/stream",
    tags=["stream"],
)


@router.get("/{name}", response_model=None)
async def stream_song(
    name: str, request: Request, token: Annotated[TokenData, Depends(JWTBearer())]
) -> StreamingResponse | Response:
    """Streams song audio

    Args:
        name (str): song name
        request (Request): incoming request
        token (Annotated[TokenData, Depends): JWT info
    """
    try:
        range_header = request.headers.get("range")

        stream_audio_content = stream_service.get_stream_audio_data(range_header, name)

        return StreamingResponse(
            stream_service.stream_audio(
                song_data=stream_audio_content.song_data,
                start=stream_audio_content.start,
                end=stream_audio_content.end,
            ),
            headers=stream_audio_content.headers,
            status_code=HTTP_206_PARTIAL_CONTENT,
        )
    except SongBadNameError:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.songBadName,
        )
    except SongNotFoundError:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.songNotFound,
        )
    except SongDataNotFoundError:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.songDataNotFound,
        )
    except InvalidContentRangeStreamError:
        return Response(
            status_code=HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
            content=PropertiesMessagesManager.streamInvalidRangeHeader,
        )
    except (Exception, StreamServiceError):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )
