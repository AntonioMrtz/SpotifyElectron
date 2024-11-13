import { useEffect, useState } from 'react';
import { FastAverageColor } from 'fast-average-color';
import SongCard from 'components/Cards/SongCard/SongCard';
import PlaylistCard from 'components/Cards/PlaylistCard/PlaylistCard';
import { useParams, useNavigate } from 'react-router-dom';
import UserType from 'utils/role';
import { PropsSongCard } from 'types/song';
import { ArtistsService, UsersService } from 'swagger/api';
import useFetchGetUserPlaylists from 'hooks/useFetchGetUserPlaylists';
import styles from './userProfile.module.css';
import defaultThumbnailPlaylist from '../../assets/imgs/DefaultThumbnailPlaylist.jpg';

interface PropsUserProfile {
  userType: UserType;
  refreshSidebarData: () => void;
  changeSongName: (songName: string) => void;
}

// TODO refactor component?
export default function UserProfile({
  userType,
  changeSongName,
  refreshSidebarData,
}: PropsUserProfile) {
  const { id } = useParams();
  const navigate = useNavigate();

  const [thumbnail, setThumbnail] = useState<string>(defaultThumbnailPlaylist);
  const [mainColorThumbnail, setMainColorThumbnail] = useState('');
  const [streamHistory, setStreamHistory] = useState<PropsSongCard[]>([]);
  const [uploadedSongs, setUploadedSongs] = useState<PropsSongCard[]>([]);
  const [artistStreams, setArtistStreams] = useState(0);

  const { playlists } = useFetchGetUserPlaylists(id);

  useEffect(() => {
    const loadStreamHistory = async (userName: string) => {
      try {
        const streamHistoryData =
          await UsersService.getUserStreamHistoryUsersNameStreamHistoryGet(
            userName,
          );
        setStreamHistory(streamHistoryData);
      } catch (error) {
        setStreamHistory([]);
        console.log(`Unable to get stream history from user ${id}`);
      }
    };
    const loadSongsFromArtist = async (artistName: string) => {
      try {
        const artistSongsData =
          await ArtistsService.getArtistSongsArtistsNameSongsGet(artistName);

        setUploadedSongs(artistSongsData);
      } catch (error) {
        setStreamHistory([]);
        console.log(`Unable to get stream history from user ${id}`);
      }
    };
    const handleLoadProfile = async (userName: string) => {
      const userData = await UsersService.getUserUsersNameGet(userName);

      setThumbnail(userData.photo);

      if (userType === UserType.USER) {
        loadStreamHistory(userName);
      } else if (userType === UserType.ARTIST) {
        setArtistStreams(userData.total_streams);
        loadSongsFromArtist(userName);
      }
    };
    if (!id) return;
    handleLoadProfile(id);
  }, [id, userType]);

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

  /* Show all redirects */

  const handleShowAllUserPlaylists = (userTypeRedirect: UserType) => {
    navigate(
      `/showAllPlaylistFromUser/Playlists del usuario/${id}/${userTypeRedirect}`,
    );
  };

  const handleShowAllUserStreamHistory = (userTypeRedirect: UserType) => {
    navigate(
      `/showAllStreamHistoryFromUser/Historial de reproducción/${id}/${userTypeRedirect}`,
    );
  };

  const handleShowAllArtistSongs = () => {
    navigate(`/showAllSongsFromArtist/Canciones del artista/${id}}`);
  };

  return (
    <div
      className={`d-flex flex-column container-fluid p-0 ${styles.userProfileContainer}`}
    >
      <div
        className={`d-flex align-items-end container-fluid ${styles.headerUserProfile}`}
        style={{
          backgroundColor: `${mainColorThumbnail}`,
          paddingTop: 'var(--pading-top-sticky-header)',
        }}
      >
        <div
          className={`d-flex flex-row ms-3 align-items-center ${styles.wrapperHeaderData}`}
          style={{ zIndex: 2 }}
        >
          <img
            src={thumbnail === '' ? defaultThumbnailPlaylist : thumbnail}
            alt="thumbnail user"
            className={`${styles.thumbnailUser}`}
            onError={({ currentTarget }) => {
              currentTarget.onerror = null;
              currentTarget.src = defaultThumbnailPlaylist;
            }}
          />
          <div className="d-flex flex-column">
            <div className="d-flex flex-row align-items-center">
              {userType === UserType.ARTIST && (
                <img
                  style={{ width: '24px', height: '24px' }}
                  alt="verified icon"
                  src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAACXBIWXMAAAsTAAALEwEAmpwYAAADP0lEQVR4nO2az08TQRTHN+hR/QNM9ODVqAcvBk3ovBZ/HMATEcXon2CigvFUj+AN8aAJmEjnlYSTnk3UgzcjnozExKghUVQOwr63tQqseWyBWrtlpu2sVHnJO3R3uvP5zryZNzuznrdl/7ApTVdB+1e8VjSVD84qpCXQtJzO0UWvlUzlfVCavgNyGDn9SCGd8DaDZe4HexXSW0AaTqOf6XgSbi+/r5APA/LCOnzkCok7cnykvGw2G7ZJeYV8QyG/Oj4R7HEuADDo/R2MPwPyWErz6Yz2DyjNs5Xwa2U1z0oZKSv/UdF/y8oEvc4FKKTbcYCNutI04lwAIL90J4CnnMK3j37dqTQtOuyBxZO5uV3OBEDe73QFDyWXicFJy0fw9MC1AJA68n6n1Fk3cCbPuwG5SyEPAtIzpanoHpz/CCeZWgH5rkK6oPL+fmMBgDydNDBs5JpfGwtQyENJA55/WKjdI8iDxgJSOjiaJPzlR4Xw3bel8M5UMV7ARNBuLEBSPGj+lCT8zELk1URIxu6ZDLd5Niap3jV8/+NC+L4MXlx+91WEk0Ie9WxN5bg7yZafKcGLqCrlu6wFyKLLFfxATMv3V4cPhcWu9WWJW2NVmSQ8lFaxwmT+MoI8v1ngYW0cEIGmUzXh0+j32WTdjeZukwHbbwC/3hNUVNo/VxUekC+tvMMaPmzkedEYoJGWh0rXtAxI1xoSIPCmIE2FxxoCTENI5mhToGbDq1ohZDOIq83hH+aXwutPC+7g0WAQ20yjtUQ0v+XZfBq1SWRxM0u1awP1xjzWkcjESlsfGz68Wk80bcBiqQdy3G0tADTfM60gTkQz4CHyMSv4lR0zy6VEpYgmwofWy+kMBsfqqWhVRDPhoeTykmUTPjfrrUgGayMDFuJ7YailX+qVpjctva2SxsI+77/Z2Ioz2fZzLSCV89OeK+uYDHeApp8uw6bdRcuXm2yBOxOA/MIpfCSARpyFkKZbf+OIaQ6QxwGDHjVOh2puiGn+Ann/YDSWaBiQP5bfT+vgjHMBchAneUISi2RHWXaYHPLJtcolcTYbtskzSnux04kc8pkYaF9t2mNWm1Br2YPuVZPPDFr2U4Mt88zsF/L7hiBlV3/sAAAAAElFTkSuQmCC"
                  className="me-1"
                />
              )}

              <p style={{ textTransform: 'capitalize', marginTop: '4px' }}>
                {userType} {userType === UserType.ARTIST && 'verificado'}
              </p>
            </div>
            <h1>{id}</h1>
            <p
              style={{
                textTransform: 'capitalize',
                marginTop: '4px',
                fontSize: '0.75rem',
              }}
            >
              {userType === UserType.ARTIST &&
                `${artistStreams} reproducciones totales`}
            </p>
          </div>
        </div>
      </div>

      {userType === UserType.ARTIST && (
        <div className="p-4">
          <div className="d-flex">
            <div className={`w-100 d-flex ${styles.categoryTitleContainer}`}>
              <button
                type="button"
                className={`${styles.categoryTitle}`}
                style={{
                  border: 'none',
                  backgroundColor: 'transparent',
                  color: 'var(--pure-white)',
                  fontWeight: '700',
                  fontSize: '1.5rem',
                  marginTop: '1rem',
                  marginBottom: '1.5rem',
                }}
                onClick={handleShowAllArtistSongs}
              >
                Canciones del artista
              </button>
            </div>
            <div
              className={`container-fluid d-flex ${styles.mostrarTodoContainer}`}
            >
              <button
                type="button"
                className={`${styles.mostrarTodo}`}
                onClick={handleShowAllArtistSongs}
              >
                Mostrar todos
              </button>
            </div>
          </div>
          <div className="d-flex flex-row flex-wrap" style={{ gap: '14px' }}>
            {uploadedSongs &&
              uploadedSongs.map((songItem) => {
                return (
                  <SongCard
                    key={`${songItem.name}`}
                    name={songItem.name}
                    photo={songItem.photo}
                    artist={songItem.artist}
                    changeSongName={changeSongName}
                    refreshSidebarData={refreshSidebarData}
                  />
                );
              })}
          </div>
        </div>
      )}

      <div className="p-4">
        <div className="d-flex">
          <div className={`w-100 d-flex ${styles.categoryTitleContainer}`}>
            <button
              type="button"
              className={`${styles.categoryTitle}`}
              style={{
                border: 'none',
                backgroundColor: 'transparent',
                color: 'var(--pure-white)',
                fontWeight: '700',
                fontSize: '1.5rem',
                marginTop: '1rem',
                marginBottom: '1.5rem',
              }}
              onClick={() => {
                handleShowAllUserPlaylists(userType);
              }}
            >
              Playlists del usuario
            </button>
          </div>
          <div
            className={`container-fluid d-flex ${styles.mostrarTodoContainer}`}
          >
            <button
              type="button"
              className={`${styles.mostrarTodo}`}
              onClick={() => {
                handleShowAllUserPlaylists(userType);
              }}
            >
              Mostrar todos
            </button>
          </div>
        </div>
        <div className="d-flex flex-row flex-wrap " style={{ gap: '14px' }}>
          {playlists &&
            playlists.map((playlistItem) => {
              return (
                <PlaylistCard
                  key={playlistItem.name}
                  description={playlistItem.description}
                  name={playlistItem.name}
                  owner={playlistItem.owner}
                  photo={playlistItem.photo}
                  refreshSidebarData={refreshSidebarData}
                />
              );
            })}
        </div>
      </div>

      {userType === UserType.USER && (
        <div className="p-4">
          <div className="d-flex">
            <div className={`w-100 d-flex ${styles.categoryTitleContainer}`}>
              <button
                type="button"
                className={`${styles.categoryTitle}`}
                style={{
                  border: 'none',
                  backgroundColor: 'transparent',
                  color: 'var(--pure-white)',
                  fontWeight: '700',
                  fontSize: '1.5rem',
                  marginTop: '1rem',
                  marginBottom: '1.5rem',
                }}
                onClick={() => {
                  handleShowAllUserStreamHistory(userType);
                }}
              >
                Historial de reproducción
              </button>
            </div>
            <div
              className={`container-fluid d-flex ${styles.mostrarTodoContainer}`}
            >
              <button
                type="button"
                className={`${styles.mostrarTodo}`}
                onClick={() => {
                  handleShowAllUserStreamHistory(userType);
                }}
              >
                Mostrar todos
              </button>
            </div>
            <div className="d-flex flex-row flex-wrap " style={{ gap: '14px' }}>
              {streamHistory &&
                streamHistory.slice(0, 5).map((songItem) => {
                  return (
                    <SongCard
                      // eslint-disable-next-line react/no-array-index-key
                      key={songItem.name}
                      name={songItem.name}
                      photo={songItem.photo}
                      artist={songItem.artist}
                      changeSongName={changeSongName}
                      refreshSidebarData={refreshSidebarData}
                    />
                  );
                })}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
