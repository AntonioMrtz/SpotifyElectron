import styles from './contextMenuSong.module.css';
import Popover from '@mui/material/Popover';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import { MouseEventHandler, useEffect, useState } from 'react';
import Global from 'global/global';

interface PropsContextMenuSong {
  songName: string;
  handleClose: Function;
}

export default function ContextMenuSong(props: PropsContextMenuSong) {
  const [isOpen, setIsOpen] = useState(false);

  const [anchorEl, setAnchorEl] = useState(null);

  const handleClick = (event: any) => {
    setAnchorEl(event.currentTarget);
    setIsOpen(isOpen ? false : true);
  };

  const handleClose = () => {
    setAnchorEl(null);
    props.handleClose();
  };

  const open = Boolean(anchorEl);
  const id = open ? 'child-popover' : undefined;

  const [playlistNames, setPlaylistNames] = useState<String[]>();

  const handlePlaylists = () => {
    fetch(Global.backendBaseUrl + 'playlists/', {
      headers: { 'Access-Control-Allow-Origin': '*' },
    })
      .then((res) => res.json())
      .then((res) => {
        let playlistNames = [];

        if (res['playlists']) {
          for (let obj of res['playlists']) {
            obj = JSON.parse(obj);
            playlistNames.push(obj['name']);
          }
        }

        setPlaylistNames(playlistNames);
      })
      .catch((error) => {
        console.log(error);
        console.log('No se pudieron obtener las playlists');
      });
  };

  useEffect(() => {
    handlePlaylists();
  }, []);

  const handleAddToPlaylist = (
    event: React.MouseEvent<HTMLButtonElement>,
    playlistName: string,
    songName: string
  ) => {
    /* Add to playlist */

    fetch(Global.backendBaseUrl + 'playlists/dto/' + playlistName, {
      headers: { 'Access-Control-Allow-Origin': '*' },
    })
      .then((res) => res.json())
      .then((res) => {
        let url = Global.backendBaseUrl + 'playlists/' + playlistName; // Reemplaza con la URL de tu API y el nombre de la playlist

        let photo = res['photo'];

        const queryParams = new URLSearchParams({ photo });
        const fetchUrlUpdateSong = `${url}?${queryParams}`;

        let newSongsPutPlaylist = [];
        newSongsPutPlaylist.push(songName);

        for (let song_name of res['song_names']) {
          newSongsPutPlaylist.push(song_name);
        }

        const requestOptions = {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(newSongsPutPlaylist),
        };

        fetch(fetchUrlUpdateSong, requestOptions).then((response) => {
          if (response.status !== 204) {
            console.log('Unable to add then Song to Playlist');
          }
        });
      })
      .catch((error) => {
        console.log('Unable to update playlist');
      });

    handleClose();
  };

  return (
    <div className={` ${styles.wrapperContextMenu}`}>
      <ul>
        <li>
          <button>Añadir a la cola</button>
        </li>
        <li>
          <button>Ir a radio de la canción</button>
          <button>Ir al artista</button>
          <button>Ir al álbum</button>
          <button>Mostrar créditos</button>
        </li>
        <li>
          <button>Quitar de canciones que te gustan</button>
          <button>Quitar de esta lista</button>
          <button
            className="d-flex justify-content-between"
            onClick={handleClick}
          >
            Añadir a la playlist <i className="fa-solid fa-chevron-right"></i>
            <Popover
              id={id}
              open={open}
              anchorEl={anchorEl}
              onClose={handleClose}
              anchorOrigin={{
                vertical: 'center',
                horizontal: 'right',
              }}
              transformOrigin={{
                vertical: 'center',
                horizontal: 'left',
              }}
              sx={{
                '& .MuiPaper-root': {
                  backgroundColor: 'var(--hover-white)',
                },
              }}
            >
              <div
                className={` ${styles.wrapperContextMenu} ${styles.wrapperContextMenuAddToPlaylist}`}
              >
                <ul>
                  <li>
                    <button>Buscar una lista</button>
                  </li>
                  <li>
                    <button>Crear lista</button>
                  </li>

                  {/* Map */}

                  {playlistNames &&
                    playlistNames.map((playlistName, index) => {
                      return (
                        <li key={index}>
                          <button
                            onClick={(event) =>
                              handleAddToPlaylist(
                                event,
                                playlistName.toString(),
                                props.songName
                              )
                            }
                          >
                            {playlistName}
                          </button>
                        </li>
                      );
                    })}

                  <li>
                    <button>Playlist 1</button>
                  </li>
                </ul>
              </div>
            </Popover>
          </button>
        </li>
        <li>
          <button>Compartir</button>
        </li>
      </ul>
    </div>
  );
}
