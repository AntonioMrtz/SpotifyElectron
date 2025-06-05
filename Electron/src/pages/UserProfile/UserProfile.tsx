import { useEffect, useState } from 'react';
import { FastAverageColor } from 'fast-average-color';
import SongCard from 'components/Cards/SongCard/SongCard';
import PlaylistCard from 'components/Cards/PlaylistCard/PlaylistCard';
import { useParams, useNavigate } from 'react-router-dom';
import UserType from 'utils/role';
import { PropsSongCard } from 'types/song';
import { ArtistsService, UsersService } from 'swagger/api';
import useFetchGetUserPlaylists from 'hooks/useFetchGetUserPlaylists';
import { t } from 'i18next';
import { useSidebar } from 'providers/SidebarProvider';
import styles from './userProfile.module.css';
import defaultThumbnailPlaylist from '../../assets/imgs/DefaultThumbnailPlaylist.jpg';
import verifiedIcon from '../../assets/imgs/verified_icon.png';

interface PropsUserProfile {
  userType: UserType;
  // refreshSidebarData: () => void;
}

// TODO refactor component?
export default function UserProfile({
  userType, // refreshSidebarData,
}: PropsUserProfile) {
  const { id } = useParams();
  const navigate = useNavigate();
  const { refreshSidebarData } = useSidebar();

  const userPlaylistsTitle = t('userProfile.user-playlists');
  const artistSongsTitle = t('userProfile.artist-songs');

  const [thumbnail, setThumbnail] = useState<string>(defaultThumbnailPlaylist);
  const [mainColorThumbnail, setMainColorThumbnail] = useState('');
  const [playbackHistory, setPlaybackHistory] = useState<PropsSongCard[]>([]);
  const [uploadedSongs, setUploadedSongs] = useState<PropsSongCard[]>([]);
  const [artistStreams, setArtistStreams] = useState(0);

  const { playlists } = useFetchGetUserPlaylists(id);

  useEffect(() => {
    const loadPlaybackHistory = async (userName: string) => {
      try {
        const playbackHistoryData =
          await UsersService.getUserPlaybackHistoryUsersNamePlaybackHistoryGet(
            userName,
          );
        setPlaybackHistory(playbackHistoryData);
      } catch (error) {
        setPlaybackHistory([]);
        console.log(`Unable to get playback history from user ${id}`);
      }
    };
    const loadSongsFromArtist = async (artistName: string) => {
      try {
        const artistSongsData =
          await ArtistsService.getArtistSongsArtistsNameSongsGet(artistName);

        setUploadedSongs(artistSongsData);
      } catch (error) {
        setPlaybackHistory([]);
        console.log(`Unable to get playback history from user ${id}`);
      }
    };
    const handleLoadProfile = async (userName: string) => {
      const userData = await UsersService.getUserUsersNameGet(userName);

      setThumbnail(userData.photo);

      if (userType === UserType.USER) {
        loadPlaybackHistory(userName);
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
      `/showAllPlaylistFromUser/${userPlaylistsTitle}/${id}/${userTypeRedirect}`,
    );
  };

  const handleShowAllArtistSongs = () => {
    navigate(`/showAllSongsFromArtist/${artistSongsTitle}/${id}}`);
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
                  src={verifiedIcon}
                  alt="verified icon"
                  className="me-1"
                />
              )}
              <p style={{ textTransform: 'capitalize', marginTop: '4px' }}>
                {userType === UserType.ARTIST
                  ? t('userProfile.verified-artist')
                  : t('userProfile.profile')}
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
                `${artistStreams} ${t('userProfile.total-plays')}`}
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
                {t('userProfile.artist-songs')}
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
                {t('common.show-all')}
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
              {t('userProfile.user-playlists')}
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
              {t('common.show-all')}
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
          <h2
            style={{
              color: 'var(--pure-white)',
              fontWeight: '700',
              fontSize: '1.5rem',
              marginTop: '1rem',
              marginBottom: '1.5rem',
            }}
          >
            {t('userProfile.listening-history')}
          </h2>
          <div className="d-flex flex-row flex-wrap " style={{ gap: '14px' }}>
            {playbackHistory &&
              playbackHistory.map((songItem, index) => {
                return (
                  <SongCard
                    // eslint-disable-next-line react/no-array-index-key
                    key={`${songItem.name}-${index}`}
                    name={songItem.name}
                    photo={songItem.photo}
                    artist={songItem.artist}
                    refreshSidebarData={refreshSidebarData}
                  />
                );
              })}
          </div>
        </div>
      )}
    </div>
  );
}
