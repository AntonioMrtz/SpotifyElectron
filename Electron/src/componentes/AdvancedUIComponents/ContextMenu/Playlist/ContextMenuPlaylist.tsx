import Popover from '@mui/material/Popover';
import { useCallback, useEffect, useReducer, useState } from 'react';
import Global from 'global/global';
import { useNavigate } from 'react-router-dom';
import LoadingCircle from 'componentes/AdvancedUIComponents/LoadingCircle/LoadingCircle';
import InfoPopover from 'componentes/AdvancedUIComponents/InfoPopOver/InfoPopover';
import { InfoPopoverType } from 'componentes/AdvancedUIComponents/InfoPopOver/types/InfoPopover';
import styles from '../contextMenu.module.css';
import { PropsContextMenuPlaylist } from '../types/PropsContextMenu';

interface ConfirmationMenuData {
  title: string;
  type: InfoPopoverType;
  description: string;
}

enum ConfirmationMenuActionKind {
  ADD_SUCCESS = 'ADD_SUCCESS',
  ADD_ERROR = 'ADD_ERROR',
  DELETE_SUCESS = 'DELETE_SUCCESS',
  DELETE_ERROR = 'DELETE_ERROR',
  CLIPBOARD = 'CLIPBOARD',
}

// An interface for our actions
interface ConfirmationMenuAction {
  type: ConfirmationMenuActionKind;
}

// An interface for our state
interface ConfirmationMenuState {
  payload: ConfirmationMenuData;
}

const reducerConfirmationMenu = (
  state: ConfirmationMenuState,
  action: ConfirmationMenuAction
): ConfirmationMenuState => {
  switch (action.type) {
    case ConfirmationMenuActionKind.ADD_SUCCESS:
      return {
        payload: {
          type: InfoPopoverType.SUCCESS,
          title: 'Canciones añadidas',
          description: 'Las canciones han sido añadidas correctamente',
        },
      };

    case ConfirmationMenuActionKind.ADD_ERROR:
      return {
        payload: {
          type: InfoPopoverType.ERROR,
          title: 'Canciones no añadidas',
          description: 'Las canciones  no han sido añadidas',
        },
      };

    case ConfirmationMenuActionKind.DELETE_SUCESS:
      return {
        payload: {
          type: InfoPopoverType.SUCCESS,
          title: 'Playlist eliminada',
          description: 'La playlist ha sido eliminada correctamente',
        },
      };
    case ConfirmationMenuActionKind.DELETE_ERROR: {
      return {
        payload: {
          type: InfoPopoverType.ERROR,
          title: 'Playlist no eliminada',
          description: 'La playlist no ha sido eliminada',
        },
      };
    }

    case ConfirmationMenuActionKind.CLIPBOARD:
      return {
        payload: {
          type: InfoPopoverType.CLIPBOARD,
          title: 'Enlace copiado al portapapeles',
          description:
            'El enlace del repositorio del proyecto ha sido copiado éxitosamente',
        },
      };

    default:
      return {
        payload: {
          type: InfoPopoverType.ERROR,
          title: 'Error',
          description: 'Ha ocurrido un error.',
        },
      };
  }
};

export default function ContextMenuPlaylist({
  playlistName,
  owner,
  handleCloseParent,
  refreshSidebarData,
}: PropsContextMenuPlaylist) {
  const navigate = useNavigate();

  const initialState: ConfirmationMenuState = {
    payload: {
      type: InfoPopoverType.ERROR,
      title: '',
      description: '',
    },
  };
  const [state, dispatch] = useReducer(reducerConfirmationMenu, initialState);

  // triggers Confirmation Modal
  const [triggerOpenConfirmationModal, setTriggerOpenConfirmationModal] =
    useState(false);

  /* Handle copy to clipboard on share button */

  const displayConfirmationModal = (newState: ConfirmationMenuActionKind) => {
    dispatch({ type: newState });
    setTriggerOpenConfirmationModal(true);
  };

  const handleCopyToClipboard = (): void => {
    window.electron.copyToClipboard.sendMessage(
      'copy-to-clipboard',
      Global.repositoryUrl
    );
    displayConfirmationModal(ConfirmationMenuActionKind.CLIPBOARD);
  };

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

  const [playlistNames, setPlaylistNames] = useState<string[]>();
  const [loading, setLoading] = useState(true);

  const handlePlaylists = async () => {
    const resFetchWhoAmIUser = await fetch(
      `${Global.backendBaseUrl}usuarios/whoami`,
      {
        headers: { Authorization: Global.getToken() },
      }
    );

    const resFetchWhoAmIJson = await resFetchWhoAmIUser.json();

    const { username } = resFetchWhoAmIJson;

    const fetchUrlGetUser = `${Global.backendBaseUrl}usuarios/${username}`;

    fetch(fetchUrlGetUser)
      .then((resFetchUrlGetUser) => resFetchUrlGetUser.json())
      .then((resFetchUrlGetUserJson) => {
        return resFetchUrlGetUserJson.playlists.join(',');
      })
      .then((sidebarPlaylistNames) => {
        return fetch(
          `${Global.backendBaseUrl}playlists/multiple/${sidebarPlaylistNames}`,
          {
            headers: { 'Access-Control-Allow-Origin': '*' },
          }
        );
      })
      .then((resFetchPlaylists) => {
        return resFetchPlaylists.json();
      })
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

    /* fetch(`${Global.backendBaseUrl}playlists/`, {
      headers: { 'Access-Control-Allow-Origin': '*' },
    })
      .then((res) => res.json())
      .then((res) => {
        const playlistNamesFromFetch: string[] = [];

        res.playlists.forEach((playlistObj: any) => {
          playlistNamesFromFetch.push(JSON.parse(playlistObj).name);
        });

        setPlaylistNames(playlistNamesFromFetch);
        setLoading(false);

        return null;
      })
      .catch((error) => {
        console.log(error);
        console.log('No se pudieron obtener las playlists');
      }); */
  };

  const [isOwnerPlaylist, setIsOwnerPlaylist] = useState<boolean>();

  const disabledButton = {
    color: isOwnerPlaylist ? 'var(--pure-white)' : 'var(--grey)',
  };

  const handleOwner = useCallback(async () => {
    const resFetchWhoAmIUser = await fetch(
      `${Global.backendBaseUrl}usuarios/whoami`,
      {
        headers: { Authorization: Global.getToken() },
      }
    );

    const resFetchWhoAmIJson = await resFetchWhoAmIUser.json();

    if (owner === resFetchWhoAmIJson.username) {
      setIsOwnerPlaylist(true);
    } else {
      setIsOwnerPlaylist(false);
    }
  }, [owner]);

  useEffect(() => {
    handlePlaylists();
    handleOwner();
  }, [handleOwner]);

  const handleAddPlaylistToPlaylist = async (
    dstPlaylistName: string,
    srcPlaylistName: string
  ) => {
    try {
      const url = `${Global.backendBaseUrl}playlists/${dstPlaylistName}`; // Reemplaza con la URL de tu API y el nombre de la playlist

      const dstResponse = await fetch(
        `${Global.backendBaseUrl}playlists/dto/${dstPlaylistName}`,
        {
          headers: { 'Access-Control-Allow-Origin': '*' },
        }
      );

      const dstPlaylistData = await dstResponse.json();
      // eslint-disable-next-line camelcase
      const { photo, description, song_names } = dstPlaylistData;

      const putUrl = `${url}?foto=${photo}&descripcion=${description}`;

      const srcResponse = await fetch(
        `${Global.backendBaseUrl}playlists/dto/${srcPlaylistName}`,
        {
          headers: { 'Access-Control-Allow-Origin': '*' },
        }
      );

      const srcPlaylistData = await srcResponse.json();
      const newSongsPutPlaylist = [
        // eslint-disable-next-line camelcase
        ...song_names,
        ...srcPlaylistData.song_names,
      ];

      const requestOptions = {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newSongsPutPlaylist),
      };

      const updateResponse = await fetch(putUrl, requestOptions);

      if (updateResponse.status !== 204) {
        console.log(
          `Unable to add songs from ${srcPlaylistName} to ${dstPlaylistName}`
        );
        displayConfirmationModal(ConfirmationMenuActionKind.ADD_ERROR);
      } else {
        displayConfirmationModal(ConfirmationMenuActionKind.ADD_SUCCESS);
      }
    } catch (error) {
      console.log(
        `Unable to add songs from ${srcPlaylistName} to ${dstPlaylistName}`
      );
      displayConfirmationModal(ConfirmationMenuActionKind.ADD_ERROR);
    }
  };

  const handleDeletePlaylist = (playlistNameToDelete: string) => {
    /* Delete playlist */
    fetch(`${Global.backendBaseUrl}playlists/${playlistNameToDelete}`, {
      method: 'DELETE',
      headers: {
        'Access-Control-Allow-Origin': '*',
      },
    })
      .then((response) => {
        if (!response.ok) {
          displayConfirmationModal(ConfirmationMenuActionKind.DELETE_ERROR);

          throw new Error('Unable to delete playlist');
        } else if (response.status === 202) {
          refreshSidebarData();
          navigate(`/home`);
        }
        handleClose();
        return null;
      })
      .catch((error) => {
        console.error('Unable to delete playlist: ', error);
        displayConfirmationModal(ConfirmationMenuActionKind.DELETE_ERROR);
      });
  };

  const handleEditPlaylistData = () => {
    navigate(`/playlists/${playlistName}?edit=true`, { replace: true });

    localStorage.setItem('playlistEdit', JSON.stringify(true));

    handleClose();
  };

  return (
    <div className={` ${styles.wrapperContextMenu}`}>
      <ul>
        <li>
          <button type="button">Añadir a la cola</button>
        </li>
        <li>
          <button type="button" onClick={handleEditPlaylistData}>
            Editar datos
          </button>
          <button type="button">Crear lista similar</button>
          <button
            type="button"
            disabled={!isOwnerPlaylist}
            style={disabledButton}
            onClick={() => handleDeletePlaylist(playlistName)}
          >
            Eliminar
          </button>
          <button type="button">Descargar</button>
        </li>
        <li>
          <button
            type="button"
            className="d-flex justify-content-between align-items-center"
            onClick={handleClick}
          >
            Añadir a otra lista
            <i className="fa-solid fa-chevron-right" />
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
                <ul style={{ height: '100%' }}>
                  <li>
                    <button type="button">Buscar una lista</button>
                  </li>
                  <li>
                    <button type="button">Crear lista</button>
                  </li>

                  {loading && <LoadingCircle />}

                  {!loading &&
                    playlistNames &&
                    playlistNames.map((playlistNameItem) => {
                      return (
                        <li key={playlistNameItem}>
                          <button
                            type="button"
                            onClick={() =>
                              handleAddPlaylistToPlaylist(
                                playlistNameItem.toString(),
                                playlistName
                              )
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
        type={state.payload.type}
        title={state.payload.title}
        description={state.payload.description}
        triggerOpenConfirmationModal={triggerOpenConfirmationModal}
        handleClose={handleClose}
      />
    </div>
  );
}
