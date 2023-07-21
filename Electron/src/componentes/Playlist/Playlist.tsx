import { ChangeEvent, FormEvent, useEffect, useState } from 'react';
import { useLocation,useNavigate  } from 'react-router-dom';
import Global from 'global/global';
import styles from './playlist.module.css';
import Song from './Song/Song';
import { PropsSongs } from 'componentes/Sidebar/types/propsSongs.module';
import { FastAverageColor } from 'fast-average-color';
import defaultThumbnailPlaylist from '../../assets/imgs/DefaultThumbnailPlaylist.jpg';
import Modal from '@mui/material/Modal';
import Box from '@mui/material/Box';

interface PropsPlaylist {
  changeSongName: Function;
  triggerReloadSidebar:Function
}

export default function Playlist(props: PropsPlaylist) {
  const [mainColorThumbnail, setMainColorThumbnail] = useState('');

  /* Get current Playlist Name */
  const location = useLocation();
  let playlistName = decodeURIComponent(
    location.pathname.split('/').slice(-1)[0]
  );

  let navigate = useNavigate()


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

  const [updatingPlaylist,setUpdatingPlaylist] = useState(false)

  useEffect(() => {

    if(updatingPlaylist){

      let timeoutId = setTimeout(() => {
        loadPlaylistData();
        setUpdatingPlaylist(false)
        props.triggerReloadSidebar()

      }, 250);

      return () => clearTimeout(timeoutId);
    }else{

      loadPlaylistData();

    }
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


  const [formData, setFormData] = useState({
    nombre: '',
    foto: '',
    descripcion: '',
  });

  const handleChangeForm = (e:ChangeEvent<HTMLInputElement|HTMLTextAreaElement>) => {

    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    console.log(formData)
  };

  const handleUpdatePlaylist = (event: FormEvent<HTMLButtonElement>) => {
    event.preventDefault();


    fetch(Global.backendBaseUrl + 'playlists/dto/' + playlistName, {
      headers: { 'Access-Control-Allow-Origin': '*' },
    })
      .then((res) => res.json())
      .then((res) => {
        let url = Global.backendBaseUrl + 'playlists/' + playlistName; // Reemplaza con la URL de tu API y el nombre de la playlist

        //! cambiar si ponemos actualizar foto
        let photo = res['photo'];

        let fetchUrlUpdateSong;

        if (formData.nombre!==playlistName && formData.nombre!==''){

          fetchUrlUpdateSong = `${url}?foto=${photo}&nuevo_nombre=${formData.nombre}`;

        }else{

          fetchUrlUpdateSong = `${url}?foto=${photo}`

        }

        let newSongsPutPlaylist = [];
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
            console.log('Unable to update playlist');
          }
        });
      })
      .catch((error) => {
        console.log('Unable to update playlist');
      })
      .finally(() => {
        setOpen(false);
        if (formData.nombre!==playlistName && formData.nombre!==''){

          setUpdatingPlaylist(true)
          //* Al cargar inmediatamente con el useEffect de location produce que el contenido para la nueva url no esta disponible
          navigate(`/playlist/`+formData.nombre, { replace: true })
          loadPlaylistData()
        }
      });


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
            <div className={`d-flex flex-row container-fluid p-0`}>
              <div className={` ${styles.wrapperUpdateThumbnail}`}>
                <img src={`${thumbnailUpdatePlaylist}`} alt="" />
              </div>

              <div className={`container-fluid pe-0 ${styles.wrapperUpdateTextData}`}>
                <div
                  className={`form-floating mb-3 ${styles.inputPlaylist}`}
                >
                  <input
                    name='nombre'
                    type="text"
                    defaultValue={playlistName}
                    className={`form-control`}
                    id="nombre"
                    placeholder="Añade un nombre"
                    onChange={handleChangeForm}
                  />
                  <label htmlFor="floatingInput">Nombre</label>
                </div>

                <div
                  className={`form-floating mb-3 ${styles.inputPlaylist}`}
                >
                  <div className="form-floating">
                    <textarea
                      name='descripcion'
                      className="form-control"
                      placeholder="Añade una descripción"
                      id="descripcion"
                      style={{ height: ' 100px' }}
                      onChange={handleChangeForm}
                    ></textarea>
                    <label htmlFor="floatingTextarea2">Descripción</label>
                  </div>
                </div>
              </div>
            </div>

            <div
              className={`d-flex flex-row justify-content-end pt-2 ${styles.wrapperUpdateButton} ${styles.inputPlaylist}`}
            >
              <button onClick={handleUpdatePlaylist}>Guardar</button>
            </div>
          </form>
        </Box>
      </Modal>
    </div>
  );
}
