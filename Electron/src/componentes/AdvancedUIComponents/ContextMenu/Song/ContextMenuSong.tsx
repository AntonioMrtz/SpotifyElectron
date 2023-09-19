import Popover from '@mui/material/Popover';
import { useEffect, useState } from 'react';
import Global from 'global/global';
import LoadingCircle from 'componentes/AdvancedUIComponents/LoadingCircle/LoadingCircle';
import InfoPopover from 'componentes/AdvancedUIComponents/InfoPopOver/InfoPopover';
import { InfoPopoverType } from 'componentes/AdvancedUIComponents/InfoPopOver/types/InfoPopover';
import styles from '../contextMenu.module.css';
import { PropsContextMenuSong } from '../types/PropsContextMenu';

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
  refreshSidebarData,
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

  const handleAddToPlaylist = async (selectedPlaylistName: string) => {
    try {
      const playlistResponse = await fetch(
        `${Global.backendBaseUrl}playlists/dto/${selectedPlaylistName}`,
        {
          headers: { 'Access-Control-Allow-Origin': '*' },
        }
      );
      const playlistData = await playlistResponse.json();

      const url = `${Global.backendBaseUrl}playlists/${selectedPlaylistName}`;
      const { photo } = playlistData;

      const fetchUrlUpdateSong = `${url}?foto=${photo}&descripcion=${playlistData.description}`;

      const newSongsPutPlaylist: string[] = [
        songName,
        ...playlistData.song_names,
      ];
      const requestOptions = {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newSongsPutPlaylist),
      };

      const updateResponse = await fetch(fetchUrlUpdateSong, requestOptions);
      if (updateResponse.status !== 204) {
        console.log('Unable to add the Song to Playlist');
      }

      handleClose();
    } catch (error) {
      console.log('Unable to update playlist', error);
    }
  };

  const handleDeleteFromPlaylist = async () => {
    try {
      const playlistResponse = await fetch(
        `${Global.backendBaseUrl}playlists/dto/${playlistName}`,
        {
          headers: { 'Access-Control-Allow-Origin': '*' },
        }
      );
      const playlistData = await playlistResponse.json();

      const url = `${Global.backendBaseUrl}playlists/${playlistName}`;
      const { photo, description } = playlistData;

      const fetchUrlUpdateSong = `${url}?foto=${photo}&descripcion=${description}`;

      const newSongsPutPlaylist = playlistData.song_names.filter(
        (songNameFetch: any) => songNameFetch !== songName
      );

      const requestOptions = {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newSongsPutPlaylist),
      };

      const updateResponse = await fetch(fetchUrlUpdateSong, requestOptions);
      if (updateResponse.status === 204) {
        refreshPlaylistData();
      } else {
        console.log('Unable to delete Song from Playlist');
      }

      handleClose();
    } catch (error) {
      console.log('Unable to update playlist', error);
    }
  };

  /* Handle crear lista */

  const handleCrearLista = async () => {
    try {
      const newPlaylistName = `Playlist${Math.trunc(
        Math.floor(Math.random() * 1000)
      ).toString()}`;

      const fetchPostSongUrl = `${Global.backendBaseUrl}playlists/?nombre=${newPlaylistName}&foto=foto&descripcion=Insertar+descripcion&creador=usuarioprovisionalcambiar`;

      const requestOptions = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify([songName]),
      };

      const postResponse = await fetch(fetchPostSongUrl, requestOptions);

      if (postResponse.status === 201) {
        refreshSidebarData();
      } else {
        console.log('Unable to create playlist with this Song');
      }

      handleClose();
    } catch {
      console.log(console.log('Unable to create playlist with this Song'));
    }
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
        </li>
        <li>
          <button type="button">Quitar de canciones que te gustan</button>
          {playlistName !== '' && (
            <button type="button" onClick={() => handleDeleteFromPlaylist()}>
              Quitar de esta lista
            </button>
          )}
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
                <ul style={{ height: '100%' }}>
                  <li>
                    <button type="button">Buscar una lista</button>
                  </li>
                  <li>
                    <button type="button" onClick={handleCrearLista}>
                      Crear lista
                    </button>
                  </li>

                  {loading && <LoadingCircle />}

                  {!loading &&
                    playlistNames &&
                    playlistNames.map((playlistNameItem) => {
                      return (
                        <li key={playlistNameItem + songName}>
                          <button
                            type="button"
                            onClick={() =>
                              handleAddToPlaylist(playlistNameItem.toString())
                            }
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
