/* eslint-disable react-hooks/exhaustive-deps */
/* eslint-disable jsx-a11y/label-has-associated-control */
import { ChangeEvent, FormEvent, useEffect, useState, MouseEvent } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Global from 'global/global';
import Token from 'utils/token';
import { PropsSongs } from 'components/Sidebar/types/propsSongs.module';
import { FastAverageColor } from 'fast-average-color';
import Modal from '@mui/material/Modal';
import Box from '@mui/material/Box';
import ContextMenuPlaylist from 'components/AdvancedUIComponents/ContextMenu/Playlist/ContextMenuPlaylist';
import Popover, { PopoverPosition } from '@mui/material/Popover/';
import { secondsToHoursAndMinutesFormatted } from 'utils/date';
import defaultThumbnailPlaylist from '../../assets/imgs/DefaultThumbnailPlaylist.jpg';
import Song from '../../components/Song/Song';
import styles from './playlist.module.css';

interface PropsPlaylist {
  changeSongName: Function;
  triggerReloadSidebar: Function;
}

export default function Playlist({
  changeSongName,
  triggerReloadSidebar,
}: PropsPlaylist) {
  const [mainColorThumbnail, setMainColorThumbnail] = useState('');

  /* Get current Playlist Name */
  const location = useLocation();
  const playlistName = decodeURIComponent(
    location.pathname.split('/').slice(-1)[0],
  );

  const navigate = useNavigate();

  const [thumbnail, setThumbnail] = useState<string>(defaultThumbnailPlaylist);
  const [numberSongs, setNumberSongs] = useState<number>(0);
  const [owner, setOwner] = useState<string>('');
  const [creationDate, setCreationDate] = useState<string>('');
  const [description, setDescription] = useState<string>('');
  const [displayPlay, setdisplayPlay] = useState('');
  const [displayPause, setdisplayPause] = useState(styles.displayNonePlay);
  const [displayDislike, setdisplayDislike] = useState('');
  const [displayLike, setdisplayLike] = useState(styles.displayNoneLike);
  const [playing, setPlaying] = useState(false);
  const [liked, setLiked] = useState(false);
  const [songs, setSongs] = useState<PropsSongs[]>();

  const handlePlay = (): void => {
    if (playing === false) {
      setdisplayPause('');
      setdisplayPlay(styles.displayNonePlay);
      setPlaying(true);
    } else {
      setdisplayPlay('');
      setdisplayPause(styles.displayNonePlay);
      setPlaying(false);
    }
  };

  /* Like Button */

  const setHearthLikedInterface = () => {
    setdisplayLike('');
    setdisplayDislike(styles.displayNoneLike);
    setLiked(true);
  };

  const setHearthUnLikedInterface = () => {
    setdisplayDislike('');
    setdisplayLike(styles.displayNoneLike);
    setLiked(false);
  };
  const loadPlaylistLikedStatus = async () => {
    const username = Token.getTokenUsername();

    let resFetchGetUserJson;

    try {
      const fetchGetUser = `${Global.backendBaseUrl}users/${username}`;

      const resFetchGetUser = await fetch(fetchGetUser, {
        credentials: 'include',
      });
      if (resFetchGetUser.status === 200)
        resFetchGetUserJson = await resFetchGetUser.json();

      if (
        resFetchGetUserJson &&
        resFetchGetUserJson.saved_playlists &&
        resFetchGetUserJson.saved_playlists.includes(playlistName)
      ) {
        setHearthLikedInterface();
      } else {
        setHearthUnLikedInterface();
      }
    } catch {
      console.log('Unable to load playlist status');
    }
  };

  const handleLike = (): void => {
    const username = Token.getTokenUsername();

    if (liked === false) {
      const fetchPatchSavedPlaylistUrl = `${Global.backendBaseUrl}users/${username}/saved_playlists?playlist_name=${playlistName}`;

      const requestOptionsPatchSavedPlaylistUr: RequestInit = {
        method: 'PATCH',
        credentials: 'include',
      };

      fetch(fetchPatchSavedPlaylistUrl, requestOptionsPatchSavedPlaylistUr)
        .then(() => {
          setHearthLikedInterface();
          triggerReloadSidebar();
          return null;
        })
        .catch(() => console.log('Unable to update saved playlists'));
    } else {
      const fetchDeleteSavedPlaylistUrl = `${Global.backendBaseUrl}users/${username}/saved_playlists?playlist_name=${playlistName}`;

      const requestOptionsDeleteSavedPlaylistUr: RequestInit = {
        method: 'DELETE',
        credentials: 'include',
      };

      fetch(fetchDeleteSavedPlaylistUrl, requestOptionsDeleteSavedPlaylistUr)
        .then(() => {
          setHearthUnLikedInterface();
          triggerReloadSidebar();
          return null;
        })
        .catch(() => console.log('Unable to update saved playlists'));
    }
  };

  const handleClickArtist = () => {
    navigate(`/user/${owner}`);
  };

  const getTotalDurationPlaylist = () => {
    let totalDuration = 0;

    if (songs) {
      songs.forEach((song) => {
        totalDuration += song.duration;
      });
    }
    return totalDuration;
  };

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

  const [openModalUpdatePlaylist, setopenModalUpdatePlaylist] = useState(false);
  const [thumbnailUpdatePlaylist, setThumbnailUpdatePlaylist] = useState('');

  const handleOpenUpdatePlaylistModal = () => {
    setopenModalUpdatePlaylist(true);
  };

  const [formData, setFormData] = useState({
    name: '',
    photo: '',
    description: '',
  });

  const handleChangeForm = (
    e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
  ) => {
    if (e.target.name === 'photo') {
      setThumbnailUpdatePlaylist(
        e.target.value.includes('http')
          ? e.target.value
          : defaultThumbnailPlaylist,
      );
    }

    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const loadPlaylistData = async () => {
    try {
      const resFetchGetPlaylistDTO = await fetch(
        encodeURI(`${Global.backendBaseUrl}playlists/${playlistName}`),
        {
          credentials: 'include',
        },
      );
      const resFetchGetPlaylistDTOJson = await resFetchGetPlaylistDTO.json();

      setOwner(resFetchGetPlaylistDTOJson.owner);
      setCreationDate(resFetchGetPlaylistDTOJson.upload_date.split('-')[0]);
      setDescription(resFetchGetPlaylistDTOJson.description);

      setThumbnail(
        resFetchGetPlaylistDTOJson.photo === ''
          ? defaultThumbnailPlaylist
          : resFetchGetPlaylistDTOJson.photo,
      );
      setThumbnailUpdatePlaylist(
        resFetchGetPlaylistDTOJson.photo === ''
          ? defaultThumbnailPlaylist
          : resFetchGetPlaylistDTOJson.photo,
      );

      if (resFetchGetPlaylistDTOJson.song_names) {
        setNumberSongs(resFetchGetPlaylistDTOJson.song_names.length);
        const songPromises: Promise<any>[] = [];

        resFetchGetPlaylistDTOJson.song_names
          .reverse()
          .forEach((songName: string) => {
            songPromises.push(
              new Promise((resolve) => {
                fetch(`${Global.backendBaseUrl}songs/metadata/${songName}`, {
                  credentials: 'include',
                })
                  .then((resFetchSongDTO) => {
                    return resFetchSongDTO.json();
                  })
                  .then((resFetchSongDTOJson) => {
                    const propsSong: PropsSongs = {
                      name: songName,
                      playlistName,
                      artistName: '',
                      streams: 0,
                      duration: 0,
                      index: 0,
                      handleSongCliked: changeSongName,
                      refreshPlaylistData: loadPlaylistData,
                      refreshSidebarData: triggerReloadSidebar,
                    };
                    propsSong.artistName = resFetchSongDTOJson.artist;
                    propsSong.duration = resFetchSongDTOJson.seconds_duration;
                    propsSong.streams = resFetchSongDTOJson.streams;

                    resolve(propsSong);
                    return propsSong;
                  })
                  .catch(() => {
                    console.log('Unable to get Song Data');
                  });
              }),
            );
          });

        Promise.all(songPromises)
          .then((resSongPromises) => {
            setSongs([...resSongPromises]);
            return null;
          })
          .catch(() => {
            console.log('Unable to get Songs Data');
          });
      }
    } catch {
      console.log('Unable to get playlist');
    }
  };

  const handleUpdatePlaylist = async (event: FormEvent<HTMLButtonElement>) => {
    event.preventDefault();

    try {
      const resGetPlaylistDTO = await fetch(
        `${Global.backendBaseUrl}playlists/${playlistName}`,
        {
          credentials: 'include',
        },
      );

      const resGetPlaylistDTOJson = await resGetPlaylistDTO.json();
      const newSongsPutPlaylist = [...resGetPlaylistDTOJson.song_names];

      const url = `${Global.backendBaseUrl}playlists/${playlistName}`;
      const photo =
        formData.photo && formData.photo.includes('http') ? formData.photo : '';

      let fetchUrlUpdateSong: string;

      if (formData.name !== playlistName && formData.name !== '') {
        fetchUrlUpdateSong = `${url}?photo=${photo}&description=${formData.description}&new_name=${formData.name}`;
      } else {
        fetchUrlUpdateSong = `${url}?photo=${photo}&description=${formData.description}`;
      }

      const requestOptions = {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          credentials: 'include',
        },
        body: JSON.stringify(newSongsPutPlaylist),
      };

      const resFetchUpdateSong = await fetch(
        fetchUrlUpdateSong,
        requestOptions,
      );

      if (resFetchUpdateSong.status !== 204) {
        console.log('Unable to update playlist');
      } else {
        setopenModalUpdatePlaylist(false);
        if (formData.name !== playlistName && formData.name !== '') {
          //* Al cargar inmediatamente con el useEffect de location produce que el contenido para la nueva url no esta disponible
          triggerReloadSidebar();
          navigate(`/playlist/${formData.name}`, { replace: true });
        } else {
          loadPlaylistData();
          triggerReloadSidebar();
        }
      }
    } catch {
      console.log('Unable to update playlist');
    }
  };

  /* Context Menu */

  const [isOpen, setIsOpen] = useState(false);

  const [anchorPosition, setAnchorPosition] = useState<{
    top: number;
    left: number;
  } | null>(null);

  const open = Boolean(anchorPosition);
  const id = open ? 'parent-popover' : undefined;

  const handleOpenContextMenu = (event: MouseEvent<HTMLButtonElement>) => {
    setIsOpen(!isOpen);
    setAnchorPosition({
      top: event.clientY,
      left: event.clientX,
    });
  };

  const handleCloseContextMenu = () => {
    setAnchorPosition(null);
    setIsOpen(false);
  };

  useEffect(() => {
    if (!isOpen) {
      handleCloseContextMenu();
    }
  }, [isOpen]);

  /*  */

  useEffect(() => {
    loadPlaylistData();

    if (localStorage.getItem('playlistEdit') === 'true') {
      setopenModalUpdatePlaylist(true);
      localStorage.setItem('playlistEdit', JSON.stringify(false));
    }

    loadPlaylistLikedStatus();
  }, [location]);

  /* Process photo color */
  useEffect(() => {
    const fac = new FastAverageColor();

    const options = {
      crossOrigin: '*',
    };

    fac
      .getColorAsync(thumbnail, options)
      .then((color) => {
        setMainColorThumbnail(color.hex);

        return null;
      })
      .catch(() => {
        // console.log(e);
      });

    fac.destroy();
  }, [thumbnail]);

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
            type="button"
            onClick={handleOpenUpdatePlaylistModal}
            className={`${styles.wrapperThumbnail}`}
          >
            <img
              className=""
              src={`${thumbnail}`}
              alt="thumbnail-playlist"
              onError={({ currentTarget }) => {
                currentTarget.onerror = null;
                currentTarget.src = defaultThumbnailPlaylist;
              }}
            />
          </button>

          <div
            className={`d-flex container-fluid flex-column ${styles.headerText}`}
          >
            <p>Álbum</p>
            <h1>{playlistName}</h1>
            <p className={`${styles.descriptionText}`}>{description}</p>
            <div className="d-flex flex-row">
              <button onClick={handleClickArtist} type="button">
                {owner}
              </button>
              <p className="me-2 ms-2">•</p>
              <p>{creationDate}</p>
              <p className="me-2 ms-2">•</p>
              <p>{numberSongs} canciones</p>
              <p className="me-2 ms-2">•</p>
              <p>
                {secondsToHoursAndMinutesFormatted(getTotalDurationPlaylist())}{' '}
                aproximadamente
              </p>
            </div>
          </div>
        </div>

        <div className={` ${styles.nonBlurred} ${styles.subhHeaderPlaylist}`}>
          <button
            type="button"
            className={`${styles.hoverablePlayButton} ${displayPlay}`}
            onClick={handlePlay}
          >
            <i
              className="fa-solid fa-circle-play"
              style={{ color: 'var(--primary-green)', fontSize: '3rem' }}
            />
          </button>
          <button
            type="button"
            className={`${styles.hoverablePlayButton} ${displayPause}`}
            onClick={handlePlay}
          >
            <i
              className="fa-solid fa-circle-pause"
              style={{ color: 'var(--primary-green)', fontSize: '3rem' }}
            />
          </button>
          <button
            type="button"
            className={`${styles.hoverableItemubheader} ${displayDislike}`}
            onClick={handleLike}
            id="playlist-like-button"
          >
            <i
              className="fa-regular fa-heart"
              style={{ color: 'var(--secondary-white)', fontSize: '1.75rem' }}
            />
          </button>
          <button
            type="button"
            className={`${displayLike}`}
            onClick={handleLike}
            id="playlist-unlike-button"
          >
            <i
              className="fa-solid fa-heart"
              style={{ color: 'var(--primary-green)', fontSize: '1.75rem' }}
            />
          </button>
          <button type="button" className={`${styles.hoverableItemubheader}`}>
            <i
              className="fa-regular fa-circle-down"
              style={{ color: 'var(--secondary-white)', fontSize: '1.75rem' }}
            />
          </button>
          <button
            type="button"
            className={`${styles.hoverableItemubheader}`}
            onClick={handleOpenContextMenu}
          >
            <i
              className="fa-solid fa-ellipsis"
              style={{ color: 'var(--secondary-white)' }}
            />
          </button>
        </div>
      </div>

      <div className={`d-flex container-fluid ${styles.wrapperSongTable}`}>
        <ul className="d-flex flex-column container-fluid">
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
            <span
              className={`d-flex justify-content-end ${styles.songTitleTable}`}
              style={{ color: 'var(--secondary-white)', whiteSpace: 'nowrap' }}
            >
              Número de reproducciones
            </span>
            <span className={` d-flex justify-content-end ${styles.gridItem}`}>
              <i className="fa-regular fa-clock" />
            </span>
          </li>

          {songs &&
            songs.map((song, index) => {
              return (
                <Song
                  key={song.name}
                  name={song.name}
                  playlistName={playlistName}
                  artistName={song.artistName}
                  streams={song.streams}
                  index={index + 1}
                  duration={song.duration}
                  handleSongCliked={changeSongName}
                  refreshPlaylistData={loadPlaylistData}
                  refreshSidebarData={triggerReloadSidebar}
                />
              );
            })}
        </ul>
      </div>

      <div>
        <Popover
          id={id}
          open={open}
          onClose={handleCloseContextMenu}
          anchorReference="anchorPosition"
          anchorPosition={anchorPosition as PopoverPosition}
          anchorOrigin={{
            vertical: 'top',
            horizontal: 'left',
          }}
          transformOrigin={{
            vertical: 'top',
            horizontal: 'left',
          }}
          sx={{
            '& .MuiPaper-root': {
              backgroundColor: 'var(--hover-white)',
            },
            '& . MuiPopover-root': {
              zIndex: '1000',
            },
          }}
        >
          <ContextMenuPlaylist
            playlistName={playlistName}
            owner={owner}
            handleCloseParent={handleCloseContextMenu}
            refreshPlaylistData={() => {}}
            refreshSidebarData={triggerReloadSidebar}
          />
        </Popover>
      </div>

      {owner === Token.getTokenUsername() && (
        <Modal
          className=""
          open={openModalUpdatePlaylist}
          onClose={() => {
            setopenModalUpdatePlaylist(false);
          }}
          aria-labelledby="modal-modal-confirmation"
          aria-describedby="modal-modal-confirmation-description"
        >
          <Box sx={style} className={`${styles.wrapperUpdatePlaylistModal}`}>
            <header className="d-flex flex-row justify-content-between align-items-center">
              <h1>Editar información</h1>
              <button
                type="button"
                onClick={() => {
                  setopenModalUpdatePlaylist(false);
                }}
              >
                <i className="fa-solid fa-xmark" />
              </button>
            </header>

            <form>
              <div className="d-flex flex-column p-0">
                <div className="d-flex flex-row container-fluid p-0">
                  <div className={` ${styles.wrapperUpdateThumbnail}`}>
                    <img src={`${thumbnailUpdatePlaylist}`} alt="" />
                  </div>

                  <div
                    className={`container-fluid pe-0 ${styles.wrapperUpdateTextData}`}
                  >
                    <div
                      className={`form-floating mb-3 ${styles.inputPlaylist}`}
                    >
                      <input
                        name="name"
                        type="text"
                        defaultValue={playlistName}
                        className="form-control"
                        id="name"
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
                          name="description"
                          className="form-control"
                          defaultValue={description}
                          placeholder="Añade una descripción"
                          id="description"
                          style={{ height: ' 100px' }}
                          onChange={handleChangeForm}
                        />
                        <label htmlFor="floatingTextarea2">Descripción</label>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div
                className={`container-fluid d-flex p-0 ${styles.wrapperUpdateTextData}`}
              >
                <div
                  className={`form-floating container-fluid p-0 ${styles.inputPlaylist}`}
                >
                  <input
                    name="photo"
                    type="text"
                    className="form-control"
                    id="photo"
                    defaultValue={
                      thumbnail === defaultThumbnailPlaylist ? '' : thumbnail
                    }
                    placeholder="Url de la nueva foto"
                    onChange={handleChangeForm}
                  />
                  <label htmlFor="photo">Url de la miniatura</label>
                </div>
              </div>

              <div
                className={`d-flex flex-row justify-content-end pt-2 ${styles.wrapperUpdateButton} ${styles.inputPlaylist}`}
              >
                <button type="button" onClick={handleUpdatePlaylist}>
                  Guardar
                </button>
              </div>
            </form>
          </Box>
        </Modal>
      )}
    </div>
  );
}
