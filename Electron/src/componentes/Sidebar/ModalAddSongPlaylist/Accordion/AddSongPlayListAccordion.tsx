import { ChangeEvent, FormEvent, useState, useEffect } from 'react';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import LibraryMusicRoundedIcon from '@mui/icons-material/LibraryMusicRounded';
import AudiotrackIcon from '@mui/icons-material/Audiotrack';
import Global from 'global/global';
import Token from 'utils/token';
import { InfoPopoverType } from 'componentes/AdvancedUIComponents/InfoPopOver/types/InfoPopover';
import ConfirmationModal from 'componentes/AdvancedUIComponents/InfoPopOver/InfoPopover';
import { UserType } from 'utils/role';
import LoadingCircleSmall from 'componentes/AdvancedUIComponents/LoadingCircle/LoadingCircleSmallNoPadding';
import GenreOption from './GenreOption/GenreOption';
import styles from './addSongPlayListAccordion.module.css';

interface PropsAddSongPlayListAccordion {
  handleClose: Function;
  reloadSidebar: Function;
}

const MessagesInfoPopOver = {
  PLAYLIST_ADDED_TITLE: 'Playlist Añadida',
  PLAYLIST_ADDED_DESCRIPTION: 'La playlist se ha añadido correctamente',
  PLAYLIST_NOT_ADDED_TITLE: 'Playlist no Añadida',
  PLAYLIST_NOT_ADDED_DESCRIPTION: 'La playlist no se ha podido añadir',

  SONG_ADDED_TITLE: 'Canción Añadida',
  SONG_ADDED_DESCRIPTION: 'La canción se ha añadido correctamente',
  SONG_NOT_ADDED_TITLE: 'Canción no Añadida',
  SONG_NOT_ADDED_DESCRIPTION: 'La canción no se ha podido añadir',
};

export default function AddSongPlayListAccordion({
  handleClose,
  reloadSidebar,
}: PropsAddSongPlayListAccordion) {
  /* Check user type */

  const [isArtist, setIsArtist] = useState(false);

  const checkIsArtist = async () => {
    const role = Token.getTokenRole();

    if (role === UserType.ARTIST) {
      setIsArtist(true);
    } else {
      setIsArtist(false);
    }
  };

  useEffect(() => {
    checkIsArtist();
  }, []);

  /* Confirmation Modal */

  const [type, setType] = useState<InfoPopoverType>();
  const [title, setTitle] = useState<string>();
  const [description, setDescription] = useState<String>();

  const [triggerOpenConfirmationModal, setTriggerOpenConfirmationModal] =
    useState(false);

  const handleShowConfirmationModal = (
    typeInput: InfoPopoverType,
    titleInput: string,
    descriptionInput: string
  ) => {
    setType(typeInput);
    setTitle(titleInput);
    setDescription(descriptionInput);
    setTriggerOpenConfirmationModal((state) => !state);
  };

  /* SONG */

  const [songFile, setSongFile] = useState<File>();
  const [thumbnailUploadSong, setThumbnailUploadSong] = useState<string>();
  const [loadingUploadSong, setLoadingUploadSong] = useState(false);

  const [formDataSong, setFormDataSong] = useState({
    nombre: '',
    artista: '',
    genero: '',
    foto: '',
  });

  const handleChangeSong = (
    event: ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    if (event.target && event.target.name) {
      if (event.target.name === 'foto') {
        setThumbnailUploadSong(event.target.value);
      }

      setFormDataSong({
        ...formDataSong,
        [event.target.name]: event.target.value,
      });
    }
  };

  const handleChangeFile = (event: ChangeEvent<HTMLInputElement>) => {
    if (event.target && event.target.files) {
      setSongFile(event.target.files[0]);
    }
  };

  const handleSubmitSong = (event: FormEvent<HTMLButtonElement>) => {
    event.preventDefault();
    setLoadingUploadSong(true);

    const userName = Token.getTokenUsername();

    const url = new URL(`${Global.backendBaseUrl}canciones/`);

    if (formDataSong && songFile) {
      Object.entries(formDataSong).forEach(([key, value]) => {
        if (key !== 'file' && typeof value === 'string') {
          url.searchParams.set(key, value);
        }
      });
      url.searchParams.set('artista', userName);

      const formDataFile = new FormData();
      formDataFile.append('file', songFile);

      const requestOptions = {
        method: 'POST',
        body: formDataFile,
      };

      fetch(url, requestOptions)
        .then((response) => {
          if (response.status === 201) {
            console.log('Cancion creada');
            handleShowConfirmationModal(
              InfoPopoverType.SUCCESS,
              MessagesInfoPopOver.SONG_ADDED_TITLE,
              MessagesInfoPopOver.SONG_ADDED_DESCRIPTION
            );
          } else {
            console.log('No se a creado la cancion');
            handleShowConfirmationModal(
              InfoPopoverType.ERROR,
              MessagesInfoPopOver.SONG_NOT_ADDED_TITLE,
              MessagesInfoPopOver.SONG_NOT_ADDED_DESCRIPTION
            );
          }
          setLoadingUploadSong(false);

          return null;
        })
        .finally(() => {
          // props.handleClose();
        })
        .catch((error) => {
          console.error('Error:', error);
          setLoadingUploadSong(false);
        });
    }
  };

  /* PLAYLIST */

  const [thumbnailUploadPlaylist, setThumbnailUploadPlaylist] =
    useState<string>();

  const [formDataPlaylist, setFormDataPlaylist] = useState({
    nombre: '',
    foto: '',
  });

  const handleChangePlaylist = (
    event: ChangeEvent<
      HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement
    >
  ) => {
    if (event.target && event.target.name) {
      if (event.target.name === 'foto') {
        setThumbnailUploadPlaylist(event.target.value);
      }

      setFormDataPlaylist({
        ...formDataPlaylist,
        [event.target.name]: event.target.value,
      });
    }
  };

  const handleSubmitPlaylist = (event: FormEvent<HTMLButtonElement>) => {
    const url = new URL(`${Global.backendBaseUrl}playlists/`);

    event.preventDefault();

    if (formDataPlaylist) {
      Object.entries(formDataPlaylist).forEach(([key, value]) => {
        if (typeof value === 'string') {
          url.searchParams.set(key, value);
        }
      });

      if (!url.searchParams.get('descripcion')) {
        url.searchParams.set('descripcion', '');
      }

      const requestOptions = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify([]),
      };

      fetch(url, requestOptions)
        .then((response) => {
          if (response.status === 201) {
            handleShowConfirmationModal(
              InfoPopoverType.SUCCESS,
              MessagesInfoPopOver.PLAYLIST_ADDED_TITLE,
              MessagesInfoPopOver.PLAYLIST_ADDED_DESCRIPTION
            );
            reloadSidebar();
          } else {
            console.log('No se a creado la playlist');

            handleShowConfirmationModal(
              InfoPopoverType.ERROR,
              MessagesInfoPopOver.PLAYLIST_NOT_ADDED_TITLE,
              MessagesInfoPopOver.PLAYLIST_NOT_ADDED_DESCRIPTION
            );
          }
          return null;
        })
        .finally(() => {
          // props.handleClose();
        })
        .catch((error) => {
          console.error('Error:', error);
        });
    }
  };

  /* GENRES */

  const [genres, setGenres] = useState<{}>();

  const handleGenres = () => {
    fetch(`${Global.backendBaseUrl}generos/`, {
      headers: { 'Access-Control-Allow-Origin': '*' },
    })
      .then((res) => res.json())
      .then((res) => {
        setGenres(res);
        return null;
      })
      .catch(() => {
        console.log('No se pudieron obtener los géneros');
      });
  };

  useEffect(() => {
    handleGenres();
  }, []);

  return (
    <>
      <Accordion
        style={{
          backgroundColor: 'var(--secondary-black)',
          borderColor: '#ffffff',
        }}
      >
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel1a-content"
          id="panel1a-header"
          style={{ border: '1px solid var(--primary-black)' }}
        >
          <Typography
            style={{
              color: 'var(--primary-green)',
              fontWeight: '700',
              textTransform: 'uppercase',
            }}
          >
            <LibraryMusicRoundedIcon /> Crear lista de reproducción
          </Typography>
        </AccordionSummary>
        <AccordionDetails
          className={`p-4 d-flex flex-row ${styles.accordionDetails}`}
        >
          <form
            className={`container-fluid d-flex flex-column p-0 ${styles.formAddSong}`}
          >
            <div className="container-fluid d-flex flex-column p-0">
              <div className="d-flex flex-row">
                <div className="p-0 mb-3 me-3 container-fluid">
                  <input
                    type="text"
                    id="nombre"
                    name="nombre"
                    placeholder="Nombre de la playlist"
                    className={` `}
                    onChange={handleChangePlaylist}
                    required
                  />
                </div>
                <div className="mb-3 container-fluid p-0">
                  <input
                    type="text"
                    id="foto"
                    name="foto"
                    placeholder="URL de la miniatura"
                    className={` `}
                    onChange={handleChangePlaylist}
                    required
                  />
                </div>
              </div>
              <div className="container-fluid p-0">
                <textarea
                  id="descripcion"
                  name="descripcion"
                  placeholder="Descripción de la playlist"
                  className={`${styles.input}`}
                  onChange={handleChangePlaylist}
                  style={{ height: ' 50px', width: '100%' }}
                  required
                />
              </div>
            </div>

            <button
              type="button"
              onClick={handleSubmitPlaylist}
              className={`btn btn-lg ${styles.btnSend}`}
            >
              Subir
            </button>
          </form>
          <div className={`${styles.containerThumbNailUpload}`}>
            <img className="img-fluid" src={thumbnailUploadPlaylist} alt="" />
          </div>
        </AccordionDetails>
      </Accordion>

      {isArtist && (
        <Accordion
          style={{
            backgroundColor: 'var(--secondary-black)',
            borderColor: '#ffffff',
          }}
        >
          <AccordionSummary
            expandIcon={<ExpandMoreIcon />}
            aria-controls="panel1a-content"
            id="panel1a-header"
            style={{ border: '1px solid var(--primary-black)' }}
          >
            <Typography
              style={{
                color: 'var(--primary-green)',
                fontWeight: '700',
                textTransform: 'uppercase',
              }}
            >
              <AudiotrackIcon /> Subir canción
            </Typography>
          </AccordionSummary>
          <AccordionDetails
            className={`p-4 d-flex flex-row ${styles.accordionDetails}`}
          >
            <form
              className={`container-fluid d-flex flex-column p-0 ${styles.formAddSong}`}
            >
              <div className="container-fluid d-flex flex-row p-0">
                <div className="p-0 mb-3 w-100">
                  <input
                    type="text"
                    id="nombre"
                    name="nombre"
                    placeholder="Nombre de la cancion"
                    className={` ${styles.input}`}
                    onChange={handleChangeSong}
                    required
                  />
                </div>
              </div>
              <div className="p-0 mb-3 me-2">
                <input
                  type="text"
                  id="foto"
                  placeholder="URL de la miniatura"
                  className={` form-control ${styles.input}`}
                  onChange={handleChangeSong}
                  name="foto"
                  required
                />
              </div>

              <div
                className={`d-flex flex-row overflow-hidden align-items-center ${styles.containerSelectAndFileSelector}`}
              >
                <div className="me-5">
                  <select
                    className="form-select-sm mb-3"
                    aria-label="Default select example"
                    onChange={handleChangeSong}
                    name="genero"
                    required
                    defaultValue="Elige un género"
                  >
                    <option
                      className={` ${styles.option}`}
                      value="Elige un género"
                      disabled
                    >
                      ❗ Elige un género
                    </option>

                    {genres &&
                      Object.entries(genres).map(([key, value]) => {
                        if (
                          typeof value === 'string' &&
                          typeof value === 'string'
                        ) {
                          return (
                            <GenreOption key={key} value={value} name={value} />
                          );
                        }

                        return null;
                      })}
                  </select>
                </div>
                <div className="mb-3">
                  <input
                    className={`form-control-md ${styles.input}`}
                    type="file"
                    id="file"
                    name="file"
                    onChange={handleChangeFile}
                    accept="audio/mp3"
                    required
                  />
                </div>
              </div>

              <button
                type="button"
                onClick={handleSubmitSong}
                className={`btn btn-lg ${styles.btnSend} d-flex flex-row justify-content-center`}
              >
                Subir {loadingUploadSong && <LoadingCircleSmall />}
              </button>
            </form>

            <div className={`${styles.containerThumbNailUpload}`}>
              <img className="img-fluid" src={thumbnailUploadSong} alt="" />
            </div>
          </AccordionDetails>
        </Accordion>
      )}

      <ConfirmationModal
        type={type}
        title={title}
        description={description}
        triggerOpenConfirmationModal={triggerOpenConfirmationModal}
        handleClose={handleClose}
      />
    </>
  );
}
