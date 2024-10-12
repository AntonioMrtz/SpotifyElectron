import { ChangeEvent, FormEvent, useState, useEffect } from 'react';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import LibraryMusicRoundedIcon from '@mui/icons-material/LibraryMusicRounded';
import AudiotrackIcon from '@mui/icons-material/Audiotrack';
import { getTokenRole } from 'utils/token';
import { InfoPopoverType } from 'components/AdvancedUIComponents/InfoPopOver/types/InfoPopover';
import ConfirmationModal from 'components/AdvancedUIComponents/InfoPopOver/InfoPopover';
import UserType from 'utils/role';
import LoadingCircleSmall from 'components/AdvancedUIComponents/LoadingCircle/LoadingCircleSmallNoPadding';
import { getGenreFromString } from 'utils/genre';
import GenreOption from './GenreOption/GenreOption';
import styles from './addSongPlayListAccordion.module.css';
import useFetchGetGenres from '../../../../hooks/useFetchGetGenres';
import { PlaylistsService } from '../../../../swagger/api/services/PlaylistsService';
import { SongsService } from '../../../../swagger/api/services/SongsService';

interface PropsAddSongPlayListAccordion {
  handleClose: Function;
  refreshSidebarData: () => void;
  setIsCloseAllowed: Function;
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
  refreshSidebarData,
  setIsCloseAllowed,
}: PropsAddSongPlayListAccordion) {
  /* Check user type */

  const [isArtist, setIsArtist] = useState(false);

  const checkIsArtist = async () => {
    const role = getTokenRole();

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
    descriptionInput: string,
  ) => {
    setType(typeInput);
    setTitle(titleInput);
    setDescription(descriptionInput);
    setTriggerOpenConfirmationModal((state) => !state);
  };

  /* GENRE */

  const { genres } = useFetchGetGenres();

  /* SONG */

  const [songFile, setSongFile] = useState<File>();
  const [thumbnailUploadSong, setThumbnailUploadSong] = useState<string>();
  const [loadingUploadSong, setLoadingUploadSong] = useState(false);

  const [formDataSong, setFormDataSong] = useState({
    name: '',
    genre: '',
    photo: '',
  });

  const handleChangeSong = (
    event: ChangeEvent<HTMLInputElement | HTMLSelectElement>,
  ) => {
    if (event.target && event.target.name) {
      if (event.target.name === 'photo') {
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
      const file = event.target.files[0];

      if (file) {
        if (file.type.startsWith('audio/')) {
          setSongFile(file);
        } else {
          event.target.value = '';
        }
      } else {
        event.target.value = '';
      }
    }
  };

  const handleSubmitSong = async (event: FormEvent<HTMLButtonElement>) => {
    event.preventDefault();
    setLoadingUploadSong(true);
    setIsCloseAllowed(false);

    if (!formDataSong || !songFile) {
      return;
    }

    try {
      await SongsService.createSongSongsPost(
        formDataSong.name,
        getGenreFromString(formDataSong.genre),
        formDataSong.photo,
        { file: songFile },
      );
      console.log('Song created');
      handleShowConfirmationModal(
        InfoPopoverType.SUCCESS,
        MessagesInfoPopOver.SONG_ADDED_TITLE,
        MessagesInfoPopOver.SONG_ADDED_DESCRIPTION,
      );
    } catch (err) {
      console.log('Error creating song:', err);
      handleShowConfirmationModal(
        InfoPopoverType.ERROR,
        MessagesInfoPopOver.SONG_NOT_ADDED_TITLE,
        MessagesInfoPopOver.SONG_NOT_ADDED_DESCRIPTION,
      );
    } finally {
      setLoadingUploadSong(false);
      setIsCloseAllowed(true);
    }
  };

  /* PLAYLIST */

  const [thumbnailUploadPlaylist, setThumbnailUploadPlaylist] =
    useState<string>();

  const [formDataPlaylist, setFormDataPlaylist] = useState({
    name: '',
    photo: '',
    description: '',
  });

  const handleChangePlaylist = (
    event: ChangeEvent<
      HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement
    >,
  ) => {
    if (event.target && event.target.name) {
      if (event.target.name === 'photo') {
        setThumbnailUploadPlaylist(event.target.value);
      }

      setFormDataPlaylist({
        ...formDataPlaylist,
        [event.target.name]: event.target.value,
      });
    }
  };

  const handleSubmitPlaylist = async (event: FormEvent<HTMLButtonElement>) => {
    setIsCloseAllowed(false);

    event.preventDefault();

    if (!formDataPlaylist) {
      return;
    }

    try {
      await PlaylistsService.createPlaylistPlaylistsPost(
        formDataPlaylist.name,
        formDataPlaylist.photo,
        formDataPlaylist.description,
        [],
      );
      handleShowConfirmationModal(
        InfoPopoverType.SUCCESS,
        MessagesInfoPopOver.PLAYLIST_ADDED_TITLE,
        MessagesInfoPopOver.PLAYLIST_ADDED_DESCRIPTION,
      );
      refreshSidebarData();
    } catch (err) {
      console.log('Error creating playlist: ', err);
      handleShowConfirmationModal(
        InfoPopoverType.ERROR,
        MessagesInfoPopOver.PLAYLIST_NOT_ADDED_TITLE,
        MessagesInfoPopOver.PLAYLIST_NOT_ADDED_DESCRIPTION,
      );
    } finally {
      setIsCloseAllowed(true);
    }
  };

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
          data-testid="accordion-expand-submit-playlist"
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
                    id="name"
                    name="name"
                    placeholder="Nombre de la playlist"
                    className={` `}
                    onChange={handleChangePlaylist}
                    required
                  />
                </div>
                <div className="mb-3 container-fluid p-0">
                  <input
                    type="text"
                    id="photo"
                    name="photo"
                    placeholder="URL de la miniatura de la playlist"
                    className={` `}
                    onChange={handleChangePlaylist}
                    required
                  />
                </div>
              </div>
              <div className="container-fluid p-0">
                <textarea
                  id="description"
                  name="description"
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
              data-testid="sidebar-addsongplaylistaccordion-submit-playlist"
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
            data-testid="accordion-expand-submit-song"
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
                    id="name"
                    name="name"
                    placeholder="Nombre de la canción"
                    className={` ${styles.input}`}
                    onChange={handleChangeSong}
                    required
                  />
                </div>
              </div>
              <div className="p-0 mb-3 me-2">
                <input
                  type="text"
                  id="photo"
                  placeholder="URL de la miniatura de la canción"
                  className={` form-control ${styles.input}`}
                  onChange={handleChangeSong}
                  name="photo"
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
                    name="genre"
                    id="genre"
                    data-testid="select-genre"
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
                        if (typeof value === 'string') {
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
                    accept="audio/*"
                    required
                    data-testid="sidebar-file-input"
                  />
                </div>
              </div>

              <button
                type="button"
                onClick={handleSubmitSong}
                className={`btn btn-lg ${styles.btnSend} d-flex flex-row justify-content-center`}
                data-testid="sidebar-addsongplaylistaccordion-submit-song"
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
