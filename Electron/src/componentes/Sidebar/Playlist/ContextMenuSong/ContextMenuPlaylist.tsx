import styles from './contextMenuPlaylist.module.css';
import Popover from '@mui/material/Popover';
import { useEffect, useState } from 'react';
import Global from 'global/global';
import InfoPopover from '../../../InfoPopover/InfoPopover'
import {InfoPopoverType} from '../../../types/InfoPopover'
import { useNavigate } from 'react-router-dom';

interface PropsContextMenuSong {
  songName: string;
  playlistName: string;
  handleClose: Function;
  /* Refresh data on playlist menu after a modification */
  reloadSidebar: Function;
}

const MessagesInfoPopOver = {

  CLIPBOARD_TITLE : 'Enlace copiado al portapapeles',
  CLIPBOARD_DESCRIPTION : 'El enlace del repositorio del proyecto ha sido copiado éxitosamente',

}


export default function ContextMenuSong(props: PropsContextMenuSong) {

  let navigate = useNavigate()


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

  /* Handle copy to clipboard on share button */

  //triggers Confirmation Modal
  const [triggerOpenConfirmationModal, setTriggerOpenConfirmationModal] = useState(false);

  const handleCopyToClipboard = (): void => {
    window.electron.copyToClipboard.sendMessage(
      'copy-to-clipboard',
      Global.repositoryUrl
    );
    setTriggerOpenConfirmationModal(true);

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
          .then(res =>{

            for(let song_name of res["song_names"]){

              newSongsPutPlaylist.push(song_name)
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
                console.log(`Unable to add songs from ${srcPlaylistName} to ${dstPlaylistName}` );
              }
            });

          })


      })
      .catch((error) => {
        console.log(`Unable to add songs from ${srcPlaylistName} to ${dstPlaylistName}` );
      })
      .finally(() => {
        handleClose();
      });
  };

  const handleDeletePlaylist = (
    event: React.MouseEvent<HTMLButtonElement>,
    playlistName: string,
  ) => {

    /* Delete playlist */
    fetch(Global.backendBaseUrl + 'playlists/' + playlistName, {
      method: 'DELETE',
      headers: {
        'Access-Control-Allow-Origin': '*'
      }
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Unable to delete playlist');
        }else{ if(response.status == 202)
          navigate(`/home`, { replace: true })
          props.reloadSidebar()
          handleClose()

        }
      })
      .catch(error => {
        console.error('Unable to delete playlist: ', error);
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
          <button onClick={(event) =>
              handleDeletePlaylist(
                event,
                props.playlistName,
              )
            }
          >Eliminar</button>
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

                  {/* Map */}

                  {playlistNames &&
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
        type={InfoPopoverType.CLIPBOARD}
        title={MessagesInfoPopOver.CLIPBOARD_TITLE}
        description={MessagesInfoPopOver.CLIPBOARD_DESCRIPTION}
        triggerOpenConfirmationModal={triggerOpenConfirmationModal}
        handleClose={handleClose}
      ></InfoPopover>
    </div>
  );
}
