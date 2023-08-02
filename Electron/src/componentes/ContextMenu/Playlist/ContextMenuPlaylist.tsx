import styles from '../contextMenu.module.css';
import Popover from '@mui/material/Popover';
import { useEffect, useReducer, useState } from 'react';
import Global from 'global/global';
import InfoPopover from '../../InfoPopover/InfoPopover';
import { InfoPopoverType } from '../../types/InfoPopover';
import { useNavigate } from 'react-router-dom';
import CircularProgress from '@mui/material/CircularProgress/CircularProgress';

interface PropsContextMenuSong {
  playlistName: string;
  handleClose: Function;
  /* Refresh data on playlist menu after a modification */
  reloadSidebar: Function;
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

    case ConfirmationMenuActionKind.DELETE_ERROR:
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
          title: 'Playlist no eliminada',
          description: 'La playlist no ha sido eliminada',
        },
      };
  }
};

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

export default function ContextMenuSong(props: PropsContextMenuSong) {
  let navigate = useNavigate();

  const initialState: ConfirmationMenuState = {
    payload: {
      type: InfoPopoverType.ERROR,
      title: '',
      description: '',
    },
  };

  const displayConfirmationModal = (state: ConfirmationMenuActionKind) => {
    dispatch({ type: state });
    setTriggerOpenConfirmationModal(true);
  };

  const [state, dispatch] = useReducer(reducerConfirmationMenu, initialState);

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
  const [loading, setLoading] = useState(true);

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

  //triggers Confirmation Modal
  const [triggerOpenConfirmationModal, setTriggerOpenConfirmationModal] =
    useState(false);

  const handleCopyToClipboard = (): void => {
    window.electron.copyToClipboard.sendMessage(
      'copy-to-clipboard',
      Global.repositoryUrl
    );
    displayConfirmationModal(ConfirmationMenuActionKind.CLIPBOARD);
  };

  const handleAddPlaylitToPlaylist = (
    event: React.MouseEvent<HTMLButtonElement>,
    dstPlaylistName: string,
    srcPlaylistName: string
  ) => {
    /* Add to playlist */

    fetch(Global.backendBaseUrl + 'playlists/dto/' + dstPlaylistName, {
      headers: { 'Access-Control-Allow-Origin': '*' },
    })
      .then((res) => res.json())
      .then((res) => {
        let url = Global.backendBaseUrl + 'playlists/' + dstPlaylistName; // Reemplaza con la URL de tu API y el nombre de la playlist

        let photo = res['photo'];

        const fetchUrlUpdateSong = `${url}?foto=${photo}`;

        /* Current songs of the dstPlaylist */
        let newSongsPutPlaylist: string[] = [];
        for (let song_name of res['song_names']) {
          newSongsPutPlaylist.push(song_name);
        }

        fetch(Global.backendBaseUrl + 'playlists/dto/' + srcPlaylistName, {
          headers: { 'Access-Control-Allow-Origin': '*' },
        })
          .then((res) => res.json())
          .then((res) => {
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
                console.log(
                  `Unable to add songs from ${srcPlaylistName} to ${dstPlaylistName}`
                );
                displayConfirmationModal(ConfirmationMenuActionKind.ADD_ERROR);
              } else {
                displayConfirmationModal(
                  ConfirmationMenuActionKind.ADD_SUCCESS
                );
              }
            });
          });
      })
      .catch((error) => {
        console.log(
          `Unable to add songs from ${srcPlaylistName} to ${dstPlaylistName}`
        );
        displayConfirmationModal(ConfirmationMenuActionKind.ADD_ERROR);
      })
      .finally(() => {});
  };

  const handleDeletePlaylist = (
    event: React.MouseEvent<HTMLButtonElement>,
    playlistName: string
  ) => {
    /* Delete playlist */
    fetch(Global.backendBaseUrl + 'playlists/' + playlistName, {
      method: 'DELETE',
      headers: {
        'Access-Control-Allow-Origin': '*',
      },
    })
      .then((response) => {
        if (!response.ok) {
          displayConfirmationModal(ConfirmationMenuActionKind.DELETE_ERROR);

          throw new Error('Unable to delete playlist');
        } else if (response.status == 202) {
          navigate(`/home`, { replace: true });
          props.reloadSidebar();
          displayConfirmationModal(ConfirmationMenuActionKind.DELETE_SUCESS);
        }
      })
      .catch((error) => {
        console.error('Unable to delete playlist: ', error);
        displayConfirmationModal(ConfirmationMenuActionKind.DELETE_ERROR);
      });
  };

  return (
    <div className={` ${styles.wrapperContextMenu}`}>
      <ul>
        <li>
          <button>Añadir a la cola</button>
        </li>
        <li>
          <button>Editar datos</button>
          <button>Crear lista similar</button>
          <button
            onClick={(event) => handleDeletePlaylist(event, props.playlistName)}
          >
            Eliminar
          </button>
          <button>Descargar</button>
        </li>
        <li>
          <button
            className="d-flex justify-content-between"
            onClick={handleClick}
          >
            Añadir a otra lista<i className="fa-solid fa-chevron-right"></i>
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
                              handleAddPlaylitToPlaylist(
                                event,
                                playlistName.toString(),
                                props.playlistName
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
        type={state.payload.type}
        title={state.payload.title}
        description={state.payload.description}
        triggerOpenConfirmationModal={triggerOpenConfirmationModal}
        handleClose={handleClose}
      ></InfoPopover>
    </div>
  );
}
