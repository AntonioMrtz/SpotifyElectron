import { FormEvent, useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import Global from 'global/global';
import styles from './playlist.module.css';
import Song from './Song/Song';
import { PropsSongs } from 'componentes/Sidebar/types/propsSongs.module';
import { FastAverageColor } from 'fast-average-color';
import defaultThumbnailPlaylist from '../../assets/imgs/DefaultThumbnailPlaylist.jpg';
import Modal from '@mui/material/Modal';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';

interface PropsPlaylist {
  changeSongName: Function;
}

export default function Playlist(props: PropsPlaylist) {
  const [mainColorThumbnail, setMainColorThumbnail] = useState('');

  /* Get current Playlist Name */
  const location = useLocation();
  let playlistName = decodeURIComponent(
    location.pathname.split('/').slice(-1)[0]
  );

  const [thumbnail, setThumbnail] = useState<string>('');
  const [numberSongs, setNumberSongs] = useState<number>(0);
  const [songs, setSongs] = useState<PropsSongs[]>();

  const loadPlaylistData = async () => {
    fetch(encodeURI(Global.backendBaseUrl + 'playlists/dto/' + playlistName))
      .then((res) => res.json())
      .then(async (res) => {
        setThumbnail(
          res['photo'] === '' ? defaultThumbnailPlaylist : res['photo']
        );
        setThumbnailUpdatePlaylist(
          res['photo'] === '' ? defaultThumbnailPlaylist : res['photo']
        );
        if (res['song_names']) {
          setNumberSongs(res['song_names'].length);
          let propsSongs: PropsSongs[] = [];

          for (let obj of res['song_names'].reverse()) {
            let propsSong: PropsSongs = {
              name: obj,
              playlistName: playlistName,
              artistName: '',
              index: 0,
              handleSongCliked: props.changeSongName,
              refreshPlaylistData: loadPlaylistData,
            };

            let artistName = await fetch(
              Global.backendBaseUrl + 'canciones/dto/' + obj
            )
              .then((res) => res.json())
              .then((res) => res['artist']);

            propsSong['artistName'] = artistName;
            propsSongs.push(propsSong);
          }

          setSongs(propsSongs);
        }
      })
      .catch((error) => {
        console.log('No se puede obtener la playlist');
      });
  };

  useEffect(() => {
    loadPlaylistData();
  }, [location]);

  /* Process photo color */
  useEffect(() => {
    const fac = new FastAverageColor();

    let options = {
      crossOrigin: '*',
    };

    fac
      .getColorAsync(thumbnail, options)
      .then((color) => {
        setMainColorThumbnail(color.hex);
      })
      .catch((e) => {
        //console.log(e);
      });

    fac.destroy();
  }, [thumbnail]);

  /* Handle Update Playlist Data */

  const style = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: '524px',
    boxShadow: 24,
    p: 4,
  };

  const [open, setOpen] = useState(false);
  const [thumbnailUpdatePlaylist, setThumbnailUpdatePlaylist] = useState('');

  const handleOpenUpdatePlaylistModal = () => {
    setOpen(true);
  };

  const handleUpdatePlaylist = (event: FormEvent<HTMLButtonElement>) => {
    event.preventDefault();
  };

  return (
    <div
      className={`d-flex container-fluid flex-column ${styles.wrapperPlaylist}`}
    >
      <div
        className={`d-flex container-fluid flex-column ${styles.backgroundFilter} ${styles.header}`}
        style={{ backgroundColor: `${mainColorThumbnail}` }}
      >
        <div className={`d-flex flex-row container-fluid ${styles.nonBlurred}`}>
          <button
            onClick={handleOpenUpdatePlaylistModal}
            className={`${styles.wrapperThumbnail}`}
          >
            <img className="" src={`${thumbnail}`} alt="" />
          </button>

          <div
            className={`d-flex container-fluid flex-column ${styles.headerText}`}
          >
            <p>Álbum</p>
            <h1>{playlistName}</h1>
            <p>{numberSongs} canciones</p>
          </div>
        </div>

        <div className={` ${styles.nonBlurred} ${styles.subhHeaderPlaylist}`}>
          <button>
            <i
              className="fa-solid fa-ellipsis"
              style={{ color: '#ffffff' }}
            ></i>
          </button>
        </div>
      </div>

      <div className={`d-flex container-fluid ${styles.wrapperSongTable}`}>
        <ul className={`d-flex flex-column container-fluid`}>
          <li
            className={`container-fluid ${styles.gridContainer} ${styles.gridContainerFirstRow}`}
          >
            <span className={` ${styles.songNumberTable}`}>#</span>
            <span
              className={` ${styles.songTitleTable}`}
              style={{ color: 'var(--secondary-white)' }}
            >
              Título
            </span>
            <span className={` ${styles.gridItem}`}>
              <i className="fa-regular fa-clock"></i>
            </span>
          </li>

          {songs &&
            songs.map((song, index) => {
              return (
                <Song
                  key={index}
                  name={song.name}
                  playlistName={playlistName}
                  artistName={song.artistName}
                  index={index + 1}
                  handleSongCliked={props.changeSongName}
                  refreshPlaylistData={loadPlaylistData}
                />
              );
            })}
        </ul>
      </div>

      {/* Modal */}

      <Modal
        className={``}
        open={open}
        onClose={() => {
          setOpen(false);
        }}
        aria-labelledby="modal-modal-confirmation"
        aria-describedby="modal-modal-confirmation-description"
      >
        <Box sx={style} className={`${styles.wrapperUpdatePlaylistModal}`}>
          <header
            className={`d-flex flex-row justify-content-between align-items-center`}
          >
            <h1>Editar información</h1>
            <button
              onClick={() => {
                setOpen(false);
              }}
            >
              <i className="fa-solid fa-xmark"></i>
            </button>
          </header>

          <form>
            <div className={`d-flex flex-row`}>
              <div className={` ${styles.wrapperUpdateThumbnail}`}>
                <img src={`${thumbnailUpdatePlaylist}`} alt="" />
              </div>

              <div className={` ${styles.wrapperUpdateTextData}`}>
                <TextField
                  id="outlined-basic"
                  label={'Nombre'}
                  variant="filled"
                  defaultValue={playlistName}
                  style={{width:'100%'}}

/*                   style={{width:'100%',height:'100%'}}
 */                  sx={{
                    '& .MuiFormLabel-root': {
                      color: 'var(--primary-white)',
                    },
                  }}
                />
                <TextField
                  id="filled-basic"
                  label={'Añade una descripción original'}
                  variant="filled"
                  style={{width:'100%',height:'100%'}}
                  multiline
                  rows={4}
                  sx={{
                    '& .MuiFormLabel-root': {
                      color: 'var(--secondary-white)',
                    },
                    '& .MuiInputBase-root':{

                      padding:0,
                      height:'100%'

                    }
                  }}
                />
              </div>
            </div>

            <div
              className={`d-flex justify-content-end ${styles.wrapperUpdateButton}`}
            >
              <button onClick={handleUpdatePlaylist}>Guardar</button>
            </div>
          </form>
        </Box>
      </Modal>
    </div>
  );
}
