import Popover from '@mui/material/Popover';
import { useState } from 'react';
import LoadingCircle from 'components/AdvancedUIComponents/LoadingCircle/LoadingCircle';
import InfoPopover from 'components/AdvancedUIComponents/InfoPopOver/InfoPopover';
import { InfoPopoverType } from 'components/AdvancedUIComponents/InfoPopOver/types/InfoPopover';
import Global from 'global/global';
import Token from 'utils/token';
import { useNavigate } from 'react-router-dom';
import useFetchGetUserPlaylistNames from 'hooks/useFetchGetUserPlaylistNames';
import styles from '../contextMenu.module.css';
import { PropsContextMenuSong } from '../types/PropsContextMenu';

const MessagesInfoPopOver = {
  CLIPBOARD_TITLE: 'Enlace copiado al portapapeles',
  CLIPBOARD_DESCRIPTION:
    'El enlace del repositorio del proyecto ha sido copiado éxitosamente',
};

export default function ContextMenuSong({
  songName,
  artistName,
  playlistName,
  handleCloseParent,
  refreshPlaylistData,
  refreshSidebarData,
}: PropsContextMenuSong) {
  const navigate = useNavigate();

  const urlArtist = `/artist/${artistName}`;

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

  const handleClickGoToArtist = (event: any) => {
    event.preventDefault();
    event.stopPropagation();
    navigate(urlArtist);
  };

  const open = Boolean(anchorEl);
  const id = open ? 'child-popover' : undefined;

  const username = Token.getTokenUsername();

  const { playlistNames, loading } = useFetchGetUserPlaylistNames(username);

  // triggers Confirmation Modal
  const [triggerOpenConfirmationModal, setTriggerOpenConfirmationModal] =
    useState(false);

  const handleCopyToClipboard = (): void => {
    window.electron.copyToClipboard.sendMessage(
      'copy-to-clipboard',
      Global.repositoryUrl,
    );
    setTriggerOpenConfirmationModal(true);
  };

  const handleAddToPlaylist = async (selectedPlaylistName: string) => {
    try {
      const playlistResponse = await fetch(
        `${Global.backendBaseUrl}playlists/${selectedPlaylistName}`,
        {
          credentials: 'include',
        },
      );
      const playlistData = await playlistResponse.json();

      const url = `${Global.backendBaseUrl}playlists/${selectedPlaylistName}`;
      const { photo } = playlistData;

      const fetchUrlUpdateSong = `${url}?photo=${photo}&description=${playlistData.description}`;

      const newSongsPutPlaylist: string[] = [
        songName,
        ...playlistData.song_names,
      ];
      const requestOptions: RequestInit = {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
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
        `${Global.backendBaseUrl}playlists/${playlistName}`,
        {
          credentials: 'include',
        },
      );
      const playlistData = await playlistResponse.json();

      const url = `${Global.backendBaseUrl}playlists/${playlistName}`;
      const { photo, description } = playlistData;

      const fetchUrlUpdateSong = `${url}?photo=${photo}&description=${description}`;

      const newSongsPutPlaylist = playlistData.song_names.filter(
        (songNameFetch: any) => songNameFetch !== songName,
      );

      const requestOptions: RequestInit = {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
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
        Math.floor(Math.random() * 1000),
      ).toString()}`;

      const fetchPostPlaylistWithSongUrl = `${Global.backendBaseUrl}playlists/?name=${newPlaylistName}&photo=foto&description=Insertar+descripcion`;

      const requestOptions: RequestInit = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify([songName]),
      };

      const postResponse = await fetch(
        fetchPostPlaylistWithSongUrl,
        requestOptions,
      );

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
          <button type="button" onClick={(e) => handleClickGoToArtist(e)}>
            Ir al artista
          </button>
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
