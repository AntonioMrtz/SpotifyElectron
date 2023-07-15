import { ChangeEvent, FormEvent, useState, Fragment, useEffect } from 'react';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import LibraryMusicRoundedIcon from '@mui/icons-material/LibraryMusicRounded';
import AudiotrackIcon from '@mui/icons-material/Audiotrack';
import styles from './addSongPlayListAccordion.module.css';
import GenreOption from './GenreOption/GenreOption';
import Global from 'global/global';
import {
  ModalConfirmationResponse,
  ModalConfirmationTypes,
} from 'componentes/Sidebar/types/ModalConfirmationArgs';
('../../types/ModalConfirmationArgs');

interface PropsAddSongPlayListAccordion {
  handleClose: Function;
  reloadSidebar: Function;
  handleShowConfirmationModal: Function;
}

export default function AddSongPlayListAccordion(
  props: PropsAddSongPlayListAccordion
) {
  /* SONG */

  const [songFile, setSongFile] = useState<File>();
  const [thumbnailUploadSong, setThumbnailUploadSong] = useState<string>();

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
    let url = new URL(Global.backendBaseUrl + 'canciones/');

    event.preventDefault();

    if (formDataSong && songFile) {
      for (let [key, value] of Object.entries(formDataSong)) {
        if (key !== 'file' && typeof value === 'string') {
          url.searchParams.set(key, value);
        }
      }
      let formDataFile = new FormData();
      formDataFile.append('file', songFile);

      let requestOptions = {
        method: 'POST',
        body: formDataFile,
      };

      fetch(url, requestOptions)
        .then((response) => {
          if (response.status == 201) {
            console.log('Cancion creada');
            props.handleShowConfirmationModal(
              ModalConfirmationTypes.SONG,
              ModalConfirmationResponse.SUCCESS
            );
          } else {
            console.log('No se a creado la cancion');
            props.handleShowConfirmationModal(
              ModalConfirmationTypes.SONG,
              ModalConfirmationResponse.ERROR
            );
          }
        })
        .catch((error) => {
          console.error('Error:', error);
        })
        .finally(() => {
          props.handleClose();
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
    event: ChangeEvent<HTMLInputElement | HTMLSelectElement>
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
    let url = new URL(Global.backendBaseUrl + 'playlists/');

    event.preventDefault();

    if (formDataPlaylist) {
      for (let [key, value] of Object.entries(formDataPlaylist)) {
        if (typeof value === 'string') {
          url.searchParams.set(key, value);
        }
      }

      let requestOptions = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify([]),
      };

      fetch(url, requestOptions)
        .then((response) => {
          if (response.status == 201) {
            console.log('Playlist creada');

            props.handleShowConfirmationModal(
              ModalConfirmationTypes.PLAYLIST,
              ModalConfirmationResponse.SUCCESS
            );
            props.reloadSidebar();
          } else {
            console.log('No se a creado la playlist');

            props.handleShowConfirmationModal(
              ModalConfirmationTypes.PLAYLIST,
              ModalConfirmationResponse.ERROR
            );
          }
        })
        .catch((error) => {
          console.error('Error:', error);
        })
        .finally(() => {
          props.handleClose();
        });
    }
  };

  /* GENRES */

  const [genres, setGenres] = useState<{}>();

  const handleGenres = () => {
    fetch(Global.backendBaseUrl + 'generos/', {
      headers: { 'Access-Control-Allow-Origin': '*' },
    })
      .then((res) => res.json())
      .then((res) => {
        setGenres(res);
      })
      .catch((error) => {
        console.log('No se pudieron obtener los géneros');
      });
  };

  useEffect(() => {
    handleGenres();
  }, []);

  return (
    <Fragment>
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
            <div className={`container-fluid d-flex flex-row p-0`}>
              <div className="p-0 mb-3 me-3">
                <input
                  type="text"
                  id="nombre"
                  name="nombre"
                  placeholder="Nombre de la playlist"
                  className={` ${styles.input}`}
                  onChange={handleChangePlaylist}
                  required
                ></input>
              </div>
              <div className="mb-3">
                <input
                  type="text"
                  id="foto"
                  name="foto"
                  placeholder="URL de la miniatura"
                  className={` ${styles.input}`}
                  onChange={handleChangePlaylist}
                  required
                ></input>
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
            <div className={`container-fluid d-flex flex-row p-0`}>
              <div className="p-0 mb-3 me-3">
                <input
                  type="text"
                  id="nombre"
                  name="nombre"
                  placeholder="Nombre de la cancion"
                  className={` ${styles.input}`}
                  onChange={handleChangeSong}
                  required
                ></input>
              </div>
              <div className="mb-3">
                <input
                  type="text"
                  id="artista"
                  placeholder="Artista"
                  className={` ${styles.input}`}
                  onChange={handleChangeSong}
                  name="artista"
                  required
                ></input>
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
              ></input>
            </div>

            <div
              className={`d-flex flex-row overflow-hidden align-items-center ${styles.containerSelectAndFileSelector}`}
            >
              <div className={`me-5`}>
                <select
                  className="form-select-sm mb-3"
                  aria-label="Default select example"
                  onChange={handleChangeSong}
                  name="genero"
                  required
                  defaultValue={'Elige un género'}
                >
                  <option
                    className={` ${styles.option}`}
                    value={'Elige un género'}
                    disabled
                  >
                    ❗ Elige un género
                  </option>

                  {genres &&
                    Object.entries(genres).map(([key, value]) => {
                      return (
                        <GenreOption key={key} value={value} name={value} />
                      );
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
                ></input>
              </div>
            </div>

            <button
              type="button"
              onClick={handleSubmitSong}
              className={`btn btn-lg ${styles.btnSend}`}
            >
              Subir
            </button>
          </form>

          <div className={`${styles.containerThumbNailUpload}`}>
            <img className="img-fluid" src={thumbnailUploadSong} alt="" />
          </div>
        </AccordionDetails>
      </Accordion>
    </Fragment>
  );
}
