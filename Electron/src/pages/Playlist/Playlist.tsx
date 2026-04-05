/* eslint-disable react-hooks/exhaustive-deps */
/* eslint-disable jsx-a11y/label-has-associated-control */
import { ChangeEvent, FormEvent, useEffect, useState, MouseEvent } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { getTokenUsername } from 'utils/token';
import { PropsSongs } from 'components/Sidebar/types/propsSongs';
import { FastAverageColor } from 'fast-average-color';
import Modal from '@mui/material/Modal';
import Box from '@mui/material/Box';
import ContextMenuPlaylist from 'components/AdvancedUIComponents/ContextMenu/Playlist/ContextMenuPlaylist';
import Popover, { PopoverPosition } from '@mui/material/Popover';
import { secondsToHoursAndMinutesFormatted } from 'utils/date';
import { TextField } from '@mui/material';
import { inputStyle } from 'styles/mui5/styles';
import { useNowPlayingContext } from 'hooks/useNowPlayingContext';
import { t } from 'i18next';
import { UserProps } from 'types/user';
import defaultThumbnailPlaylist from '../../assets/imgs/DefaultThumbnailPlaylist.jpg';
import Song from '../../components/Song/Song';
import styles from './playlist.module.css';
import { UsersService } from '../../swagger/api/services/UsersService';
import { PlaylistsService } from '../../swagger/api/services/PlaylistsService';
import { SongsService } from '../../swagger/api/services/SongsService';

interface PropsPlaylist {
  refreshSidebarData: () => void;
}

export default function Playlist({ refreshSidebarData }: PropsPlaylist) {
  const { changeSongName } = useNowPlayingContext();

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
    const username = getTokenUsername();

    try {
      // TODO simplify query to obtain the result directly

      const userData: UserProps =
        await UsersService.getUserUsersNameGet(username);

      if (
        userData &&
        userData.saved_playlists &&
        userData.saved_playlists.includes(playlistName)
      ) {
        setHearthLikedInterface();
      } else {
        setHearthUnLikedInterface();
      }
    } catch {
      console.log('Unable to load playlist status');
    }
  };

  const handleLike = async () => {
    const username = getTokenUsername();

    if (liked === false) {
      try {
        await UsersService.patchSavedPlaylistsUsersNameSavedPlaylistsPatch(
          username,
          playlistName,
        );
        setHearthLikedInterface();
        refreshSidebarData();
      } catch (err) {
        console.log(
          `Unable to add user ${username} saved playlists with ${playlistName}`,
        );
      }
    } else {
      try {
        await UsersService.deleteSavedPlaylistsUsersNameSavedPlaylistsDelete(
          username,
          playlistName,
        );
        setHearthUnLikedInterface();
        refreshSidebarData();
      } catch (err) {
        console.log(
          `Unable to delete user ${username} saved playlists with ${playlistName}`,
        );
      }
    }
  };

  const handleClickArtist = () => {
    navigate(`/user/${owner}`);
  };

  const getTotalDurationPlaylist = () => {
    let totalDuration = 0;

    if (songs) {
      songs.forEach((song) => {
        totalDuration += song.secondsDuration;
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
    event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
  ) => {
    if (event.target.name === 'photo') {
      setThumbnailUpdatePlaylist(
        event.target.value.includes('http')
          ? event.target.value
          : defaultThumbnailPlaylist,
      );
    }

    setFormData({
      ...formData,
      [event.target.name]: event.target.value,
    });
  };

  const loadPlaylistData = async () => {
    try {
      // TODO custom hook
      const playlistData =
        await PlaylistsService.getPlaylistPlaylistsNameGet(playlistName);
      setOwner(playlistData.owner);
      setCreationDate(playlistData.upload_date.split('-')[0]);
      setDescription(playlistData.description);

      setThumbnail(
        playlistData.photo === ''
          ? defaultThumbnailPlaylist
          : playlistData.photo,
      );
      setThumbnailUpdatePlaylist(
        playlistData.photo === ''
          ? defaultThumbnailPlaylist
          : playlistData.photo,
      );

      if (playlistData.song_names) {
        setNumberSongs(playlistData.song_names.length);
        const songPromises: Promise<any>[] = [];

        // TODO reduce complexity or refactor

        playlistData.song_names.reverse().forEach((songName: string) => {
          songPromises.push(
            new Promise((resolve) => {
              SongsService.getSongMetadataSongsMetadataNameGet(songName)
                .then((songData) => {
                  const propsSong: PropsSongs = {
                    name: songName,
                    playlistName,
                    artistName: '',
                    streams: 0,
                    secondsDuration: 0,
                    index: 0,
                    handleSongCliked: changeSongName,
                    refreshPlaylistData: loadPlaylistData,
                    refreshSidebarData,
                  };
                  propsSong.artistName = songData.artist;
                  propsSong.secondsDuration = songData.seconds_duration;
                  propsSong.streams = songData.streams;

                  resolve(propsSong);
                  return propsSong;
                })
                .catch((err) => {
                  console.log('Unable to get Song Data');
                  console.error(err);
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
    } catch (err) {
      console.log(`Unable to get playlist ${playlistName}`);
      console.log(err);
    }
  };

  const refreshPlaylistData = () => {
    // wait until backend has data updated, fast requests after update can trigger 404 on backend (Ej: playlist update - sidebar - playlist)
    setTimeout(() => {
      loadPlaylistData();
    }, 500);
  };

  const handleUpdatePlaylist = async (event: FormEvent<HTMLButtonElement>) => {
    event.preventDefault();

    try {
      // TODO add song to playlist instead of fetching already present songs
      const playlistData =
        await PlaylistsService.getPlaylistPlaylistsNameGet(playlistName);
      const newSongsPutPlaylist = [...playlistData.song_names];

      const formPhoto =
        formData.photo && formData.photo.includes('http') ? formData.photo : '';

      const formDescription = formData.description;

      if (formData.name !== playlistName && formData.name !== '') {
        PlaylistsService.updatePlaylistPlaylistsNamePut(
          playlistName,
          formPhoto,
          formDescription,
          newSongsPutPlaylist,
          formData.name,
        );
      } else {
        PlaylistsService.updatePlaylistPlaylistsNamePut(
          playlistName,
          formPhoto,
          formDescription,
          newSongsPutPlaylist,
        );
      }

      setopenModalUpdatePlaylist(false);

      if (formData.name !== playlistName && formData.name !== '') {
        // on name change
        setTimeout(() => {
          refreshSidebarData();
          navigate(`/playlist/${formData.name}`, { replace: true });
        }, 500);
        refreshPlaylistData();
        return;
      }

      refreshPlaylistData();
      refreshSidebarData();
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
            <p>{t('common.album')}</p>
            <h1>{playlistName}</h1>
            <p className={`${styles.descriptionText}`}>{description}</p>
            <div className="d-flex flex-row">
              <button onClick={handleClickArtist} type="button">
                {owner}
              </button>
              <p className="me-2 ms-2">•</p>
              <p>{creationDate}</p>
              <p className="me-2 ms-2">•</p>
              <p>
                {numberSongs} {t('playlist.songs')}
              </p>
              <p className="me-2 ms-2">•</p>
              <p>
                {secondsToHoursAndMinutesFormatted(getTotalDurationPlaylist())}
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
          {owner !== getTokenUsername() && (
            <>
              <button
                type="button"
                className={`${styles.hoverableItemubheader} ${displayDislike}`}
                onClick={handleLike}
                id="playlist-like-button"
              >
                <i
                  className="fa-regular fa-heart"
                  style={{
                    color: 'var(--secondary-white)',
                    fontSize: '1.75rem',
                  }}
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
            </>
          )}
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
              {t('playlist.title')}
            </span>
            <span
              className={`d-flex justify-content-end ${styles.songTitleTable}`}
              style={{ color: 'var(--secondary-white)', whiteSpace: 'nowrap' }}
            >
              {t('playlist.plays')}
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
                  secondsDuration={song.secondsDuration}
                  handleSongCliked={changeSongName}
                  refreshPlaylistData={refreshPlaylistData}
                  refreshSidebarData={refreshSidebarData}
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
            refreshPlaylistData={refreshPlaylistData}
            refreshSidebarData={refreshSidebarData}
          />
        </Popover>
      </div>

      {owner === getTokenUsername() && (
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
              <h1> {t('playlist.edit-details')}</h1>
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
              <div className="d-flex flex-column p-0 mb-3">
                <div className="d-flex flex-row container-fluid p-0">
                  <div className={` ${styles.wrapperUpdateThumbnail}`}>
                    <img src={`${thumbnailUpdatePlaylist}`} alt="" />
                  </div>

                  <div
                    className={`container-fluid pe-0 ${styles.wrapperUpdateTextData}`}
                  >
                    <div className={`mb-3 ${styles.inputPlaylist}`}>
                      <TextField
                        id="name-input"
                        label={t('playlist.name')}
                        name="name"
                        variant="outlined"
                        type="text"
                        placeholder={t('playlist.name-placeholder')}
                        defaultValue={playlistName}
                        onChange={handleChangeForm}
                        sx={inputStyle}
                      />
                    </div>

                    <div className={`${styles.inputPlaylist}`}>
                      <TextField
                        id="description-input"
                        label={t('playlist.description')}
                        variant="outlined"
                        type="text"
                        multiline // Enable multiline to create a textarea-like effect
                        minRows={3} // Minimum number of rows
                        maxRows={3} // Allow it to grow indefinitely
                        sx={{
                          ...inputStyle,
                          '& .MuiInputBase-input': {
                            height: '100px', // Set the height of the input
                            width: '100%',
                            boxSizing: 'border-box', // Ensure padding is included in the height
                            color: 'var(--primary-white)', // keep same color
                          },
                        }}
                        name="description"
                        defaultValue={description}
                        placeholder={t('playlist.description-placeholder')}
                        onChange={handleChangeForm}
                      />
                    </div>
                  </div>
                </div>
              </div>
              <div
                className={`container-fluid d-flex p-0 ${styles.wrapperUpdateTextData}`}
              >
                <div className={` container-fluid p-0 ${styles.inputPlaylist}`}>
                  <div className={`mb-3 ${styles.inputPlaylist}`}>
                    <TextField
                      id="photo-input"
                      label={t('playlist.thumbnail')}
                      name="name"
                      variant="outlined"
                      type="text"
                      placeholder={t('playlist.thumbnail-placeholder')}
                      defaultValue={
                        thumbnail === defaultThumbnailPlaylist ? '' : thumbnail
                      }
                      onChange={handleChangeForm}
                      sx={inputStyle}
                    />
                  </div>
                </div>
              </div>

              <div
                className={`d-flex flex-row justify-content-end pt-2 ${styles.wrapperUpdateButton} ${styles.inputPlaylist}`}
              >
                <button type="button" onClick={handleUpdatePlaylist}>
                  {t('playlist.save')}
                </button>
              </div>
            </form>
          </Box>
        </Modal>
      )}
    </div>
  );
}
