import Popover from '@mui/material/Popover';
import { useEffect, useState } from 'react';
import Global from 'global/global';
import CircularProgress from '@mui/material/CircularProgress/CircularProgress';
import InfoPopover from '../../InfoPopover/InfoPopover';
import { InfoPopoverType } from '../../types/InfoPopover';
import styles from '../contextMenu.module.css';

interface PropsContextMenuSong {
  songName: string;
  playlistName: string;
  handleClose: Function;
  /* Refresh data on playlist menu after a modification */
  refreshPlaylistData: Function;
}

const MessagesInfoPopOver = {
  CLIPBOARD_TITLE: 'Enlace copiado al portapapeles',
  CLIPBOARD_DESCRIPTION:
    'El enlace del repositorio del proyecto ha sido copiado éxitosamente',
};

export default function ContextMenuSong(props: PropsContextMenuSong) {
  const [isOpen, setIsOpen] = useState(false);

  const [anchorEl, setAnchorEl] = useState(null);

  const handleClick = (event: any) => {
    setAnchorEl(event.currentTarget);
    setIsOpen(!isOpen);
  };

  const handleClose = () => {
    setAnchorEl(null);
    props.handleClose();
  };

  const open = Boolean(anchorEl);
  const id = open ? 'child-popover' : undefined;

  const [playlistNames, setPlaylistNames] = useState<String[]>();

  const [loading, setLoading] = useState(true);

  const handlePlaylists = () => {
    fetch(`${Global.backendBaseUrl}playlists/`, {
      headers: { 'Access-Control-Allow-Origin': '*' },
    })
      .then((res) => res.json())
      .then((res) => {
        const playlistNames = [];

        if (res.playlists) {
          for (let obj of res.playlists) {
            obj = JSON.parse(obj);
            playlistNames.push(obj.name);
          }
        }

        setPlaylistNames(playlistNames);
        setLoading(false);
      })
      .catch((error) => {
        console.log(error);
        console.log('No se pudieron obtener las playlists');
      });
  };

  useEffect(() => {
    handlePlaylists();
  }, []);

  /* Handle copy to clipboard on share button */

  // triggers Confirmation Modal
  const [triggerOpenConfirmationModal, setTriggerOpenConfirmationModal] =
    useState(false);

  const handleCopyToClipboard = (): void => {
    window.electron.copyToClipboard.sendMessage(
      'copy-to-clipboard',
      Global.repositoryUrl
    );
    setTriggerOpenConfirmationModal(true);
  };

  const handleAddToPlaylist = (
    event: React.MouseEvent<HTMLButtonElement>,
    playlistName: string,
    songName: string
  ) => {
    /* Add to playlist */

    fetch(`${Global.backendBaseUrl}playlists/dto/${playlistName}`, {
      headers: { 'Access-Control-Allow-Origin': '*' },
    })
      .then((res) => res.json())
      .then((res) => {
        const url = `${Global.backendBaseUrl}playlists/${playlistName}`; // Reemplaza con la URL de tu API y el nombre de la playlist

        const { photo } = res;

        const fetchUrlUpdateSong = `${url}?foto=${photo}&descripcion=${res.description}`;

        const newSongsPutPlaylist = [];
        newSongsPutPlaylist.push(songName);

        for (const song_name of res.song_names) {
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
            console.log('Unable to add the Song to Playlist');
          }
        });
      })
      .catch((error) => {
        console.log('Unable to update playlist');
      })
      .finally(() => {
        handleClose();
      });
  };

  const handleDeleteFromPlaylist = (
    event: React.MouseEvent<HTMLButtonElement>,
    playlistName: string,
    songName: string
  ) => {
    /* Add to playlist */

    fetch(`${Global.backendBaseUrl}playlists/dto/${playlistName}`, {
      headers: { 'Access-Control-Allow-Origin': '*' },
    })
      .then((res) => res.json())
      .then((res) => {
        const url = `${Global.backendBaseUrl}playlists/${playlistName}`; // Reemplaza con la URL de tu API y el nombre de la playlist

        const { photo } = res;

        const fetchUrlUpdateSong = `${url}?foto=${photo}`;

        const newSongsPutPlaylist = [];

        for (const song_name of res.song_names) {
          if (song_name !== songName) {
            newSongsPutPlaylist.push(song_name);
          }
        }

        const requestOptions = {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(newSongsPutPlaylist),
        };

        fetch(fetchUrlUpdateSong, requestOptions).then((response) => {
          if (response.status === 204) {
            props.refreshPlaylistData();
          } else {
            console.log('Unable to delete Song from Playlist');
          }
        });
      })
      .catch((error) => {
        console.log('Unable to update playlist');
      })
      .finally(() => {
        handleClose();
      });
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
          <button
            onClick={(event) =>
              handleDeleteFromPlaylist(
                event,
                props.playlistName,
                props.songName
              )
            }
          >
            Quitar de esta lista
          </button>
          <button
            className="d-flex justify-content-between align-items-center"
            onClick={handleClick}
          >
            Añadir a la playlist <i className="fa-solid fa-chevron-right" />
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
                  border: '1px solid var(--third-black)',
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

                  {loading && (
                    <div
                      className="container-fluid d-flex justify-content-center align-content-center"
                      style={{
                        height: '100%',
                        justifyContent: 'center',
                        alignItems: 'center',
                        padding: '5%',
                      }}
                    >
                      <CircularProgress
                        style={{ width: '2rem', height: 'auto' }}
                        sx={{
                          ' & .MuiCircularProgress-circle': {
                            color: 'var(--pure-white)',
                          },
                          '& .css-zk81sn-MuiCircularProgress-root': {
                            width: '3rem',
                          },
                        }}
                      />
                    </div>
                  )}

                  {!loading &&
                    playlistNames &&
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
                </ul>
              </div>
            </Popover>
          </button>
        </li>
        <li>
          <button onClick={handleCopyToClipboard}>Compartir</button>
        </li>
      </ul>

      <InfoPopover
        type={InfoPopoverType.CLIPBOARD}
        title={MessagesInfoPopOver.CLIPBOARD_TITLE}
        description={MessagesInfoPopOver.CLIPBOARD_DESCRIPTION}
        triggerOpenConfirmationModal={triggerOpenConfirmationModal}
        handleClose={handleClose}
      />
    </div>
  );
}
