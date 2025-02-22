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
import LoadingCircleSmall from 'components/AdvancedUIComponents/LoadingCircle/LoadingCircleSmall';
import { getGenreFromString } from 'utils/genre';
import { t } from 'i18next';
import GenreOption from './GenreOption/GenreOption';
import styles from './uploadSongPlaylistAccordion.module.css';
import useFetchGetGenres from '../../../../hooks/useFetchGetGenres';
import { PlaylistsService } from '../../../../swagger/api/services/PlaylistsService';
import { SongsService } from '../../../../swagger/api/services/SongsService';

interface PropsuploadSongPlaylistAccordion {
  handleClose: Function;
  refreshSidebarData: () => void;
  setIsCloseAllowed: Function;
}

export default function UploadSongPlaylistAccordion({
  handleClose,
  refreshSidebarData,
  setIsCloseAllowed,
}: PropsuploadSongPlaylistAccordion) {
  /* Messages */

  const MessagesInfoPopOver = {
    PLAYLIST_ADDED_TITLE: t('uploadSongPlaylistAccordion.playlist-added-title'),
    PLAYLIST_ADDED_DESCRIPTION: t(
      'uploadSongPlaylistAccordion.playlist-added-description',
    ),
    PLAYLIST_NOT_ADDED_TITLE: t(
      'uploadSongPlaylistAccordion.playlist-not-added-title',
    ),
    PLAYLIST_NOT_ADDED_DESCRIPTION: t(
      'uploadSongPlaylistAccordion.playlist-not-added-description',
    ),

    SONG_ADDED_TITLE: t('uploadSongPlaylistAccordion.song-added-title'),
    SONG_ADDED_DESCRIPTION: t(
      'uploadSongPlaylistAccordion.song-added-description',
    ),
    SONG_NOT_ADDED_TITLE: t('uploadSongPlaylistAccordion.song-not-added-title'),
    SONG_NOT_ADDED_DESCRIPTION: t(
      'uploadSongPlaylistAccordion.song-not-added-description',
    ),
  };
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

    if (!songFile) {
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
            <LibraryMusicRoundedIcon />{' '}
            {t('uploadSongPlaylistAccordion.create-playlist')}
          </Typography>
        </AccordionSummary>
        <AccordionDetails
          className={`p-4 d-flex flex-row ${styles.accordionDetails}`}
        >
          <form
            className={`container-fluid d-flex flex-column p-0 ${styles.formAddSong}`}
          >
            <div className="container-fluid d-flex flex-column p-0 mb-3">
              <div className="d-flex flex-row">
                <div className="p-0 mb-3 me-3 container-fluid d-flex">
                  <p className="text-danger">*</p>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    placeholder={t('uploadSongPlaylistAccordion.playlist-name')}
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
                    placeholder={t(
                      'uploadSongPlaylistAccordion.playlist-thumbnail-url',
                    )}
                    className={` `}
                    onChange={handleChangePlaylist}
                    required
                  />
                </div>
              </div>
              <div className="container-fluid p-0 d-flex">
                <p className="invisible">*</p>
                <textarea
                  id="description"
                  name="description"
                  placeholder={t(
                    'uploadSongPlaylistAccordion.playlist-description',
                  )}
                  onChange={handleChangePlaylist}
                  style={{ height: ' 50px', width: '100%' }}
                  required
                />
              </div>
            </div>
            <div className="d-flex flex-row">
              <p className="invisible">*</p>
              <p className="text-danger">
                {t('uploadSongPlaylistAccordion.obligatory-fields')}
              </p>
            </div>

            <button
              type="button"
              onClick={handleSubmitPlaylist}
              className={`btn btn-lg ${styles.btnSend}`}
              data-testid="sidebar-submit-playlist"
              disabled={!formDataPlaylist.name}
            >
              {t('uploadSongPlaylistAccordion.upload')}
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
              <AudiotrackIcon /> {t('uploadSongPlaylistAccordion.create-song')}
            </Typography>
          </AccordionSummary>
          <AccordionDetails
            className={`p-4 d-flex flex-row ${styles.accordionDetails}`}
          >
            <form
              className={`container-fluid d-flex flex-column p-0 ${styles.formAddSong}`}
            >
              <div className="container-fluid d-flex flex-row p-0 mb-3 w-100">
                <p className="text-danger">*</p>
                <input
                  type="text"
                  id="name"
                  name="name"
                  placeholder={t('uploadSongPlaylistAccordion.song-name')}
                  className={` ${styles.input}`}
                  onChange={handleChangeSong}
                  required
                />
              </div>
              <div className="p-0 mb-3 me-2 d-flex flex-row w-100 ">
                <p className="invisible">*</p>
                <input
                  type="text"
                  id="photo"
                  placeholder={t(
                    'uploadSongPlaylistAccordion.song-thumbnail-url',
                  )}
                  onChange={handleChangeSong}
                  name="photo"
                  required
                />
              </div>

              <div
                className={`d-flex flex-row overflow-hidden align-items-center justify-content-between ${styles.containerSelectAndFileSelector}`}
              >
                <div className="me-5 d-flex">
                  <p className="text-danger me-2">*</p>
                  <select
                    className="form-select-sm mb-3"
                    aria-label="Default select example"
                    onChange={handleChangeSong}
                    name="genre"
                    id="genre"
                    data-testid="select-genre"
                    required
                    defaultValue={t('uploadSongPlaylistAccordion.choose-genre')}
                  >
                    <option
                      className={` ${styles.option}`}
                      value={t(
                        'uploadSongPlaylistAccordion.choose-genre-default',
                      )}
                      disabled
                    >
                      {t('uploadSongPlaylistAccordion.choose-genre-default')}
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
                <div className="mb-3 d-flex">
                  <p className="text-danger me-1">*</p>
                  <input
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
              <p className="text-danger mt-2">
                {t('uploadSongPlaylistAccordion.obligatory-fields')}
              </p>

              <button
                type="button"
                onClick={handleSubmitSong}
                className={`btn btn-lg ${styles.btnSend} d-flex flex-row justify-content-center`}
                data-testid="sidebar-submit-song"
                disabled={
                  !formDataSong.name ||
                  !formDataSong.genre ||
                  !songFile ||
                  loadingUploadSong
                }
              >
                {t('uploadSongPlaylistAccordion.upload')}{' '}
                {loadingUploadSong && <LoadingCircleSmall />}
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
