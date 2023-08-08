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
  handleCloseParent: Function;
  /* Refresh data on playlist menu after a modification */
  refreshPlaylistData: Function;
}

const MessagesInfoPopOver = {
  CLIPBOARD_TITLE: 'Enlace copiado al portapapeles',
  CLIPBOARD_DESCRIPTION:
    'El enlace del repositorio del proyecto ha sido copiado éxitosamente',
};

export default function ContextMenuSong({
  songName,
  playlistName,
  handleCloseParent,
  refreshPlaylistData,
}: PropsContextMenuSong) {
  const [isOpen, setIsOpen] = useState(false);

  const [anchorEl, setAnchorEl] = useState(null);

  const handleClick = (event: any) => {
    setAnchorEl(event.currentTarget);
    setIsOpen(!isOpen);
  };

  const handleClose = () => {
    setAnchorEl(null);
    handleCloseParent();
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
        const playlistNamesFromFetch: string[] = [];

        if (res.playlists) {
          res.playlists.forEach((obj: any) => {
            const playlistObject = JSON.parse(obj);
            playlistNamesFromFetch.push(playlistObject.name);
          });
        }

        setPlaylistNames(playlistNamesFromFetch);
        setLoading(false);

        return null;
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

  const handleAddToPlaylist = () => {
    /* Add to playlist */

    fetch(`${Global.backendBaseUrl}playlists/dto/${playlistName}`, {
      headers: { 'Access-Control-Allow-Origin': '*' },
    })
      .then((res) => res.json())
      .then((res) => {
        const url = `${Global.backendBaseUrl}playlists/${playlistName}`;

        const { photo } = res;

        const fetchUrlUpdateSong = `${url}?foto=${photo}&descripcion=${res.description}`;

        const newSongsPutPlaylist: string[] = [];
        newSongsPutPlaylist.push(songName);

        res.song_names.forEach((songNameFetch: any) => {
          newSongsPutPlaylist.push(songNameFetch);
        });

        const requestOptions = {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(newSongsPutPlaylist),
        };

        fetch(fetchUrlUpdateSong, requestOptions)
          .then((response) => {
            if (response.status !== 204) {
              console.log('Unable to add the Song to Playlist');
            }
            return null;
          })
          .finally(() => {
            handleClose();
          })
          .catch(() => {
            console.log('Unable to update playlist');
          });

        return null;
      })
      .catch(() => {
        console.log('Unable to update playlist');
      });
  };

  const handleDeleteFromPlaylist = () => {
    /* Add to playlist */

    fetch(`${Global.backendBaseUrl}playlists/dto/${playlistName}`, {
      headers: { 'Access-Control-Allow-Origin': '*' },
    })
      .then((res) => res.json())
      .then((res) => {
        const url = `${Global.backendBaseUrl}playlists/${playlistName}`; // Reemplaza con la URL de tu API y el nombre de la playlist

        const { photo } = res;

        const fetchUrlUpdateSong = `${url}?foto=${photo}`;

        const newSongsPutPlaylist: string[] = [];

        res.song_names.forEach((songNameFetch: any) => {
          if (songNameFetch !== songName) {
            newSongsPutPlaylist.push(songNameFetch);
          }
        });

        const requestOptions = {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(newSongsPutPlaylist),
        };

        fetch(fetchUrlUpdateSong, requestOptions)
          .then((response) => {
            if (response.status === 204) {
              refreshPlaylistData();
            } else {
              console.log('Unable to delete Song from Playlist');
            }
            return null;
          })
          .catch(() => {
            console.log('Unable to update playlist');
          });

        return null;
      })
      .finally(() => {
        handleClose();
      })
      .catch(() => {
        console.log('Unable to update playlist');
      });
  };

  return (
    <div className={` ${styles.wrapperContextMenu}`}>
      <ul>
        <li>
          <button type="button">Añadir a la cola</button>
        </li>
        <li>
          <button type="button">Ir a radio de la canción</button>
          <button type="button">Ir al artista</button>
          <button type="button">Ir al álbum</button>
          <button type="button">Mostrar créditos</button>
        </li>
        <li>
          <button type="button">Quitar de canciones que te gustan</button>
          <button type="button" onClick={() => handleDeleteFromPlaylist()}>
            Quitar de esta lista
          </button>
          <button
            type="button"
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
                    <button type="button">Buscar una lista</button>
                  </li>
                  <li>
                    <button type="button">Crear lista</button>
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
                    playlistNames.map((playlistNameItem) => {
                      return (
                        <li key={songName}>
                          <button
                            type="button"
                            onClick={() => handleAddToPlaylist()}
                          >
                            {playlistNameItem}
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
          <button type="button" onClick={handleCopyToClipboard}>
            Compartir
          </button>
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
