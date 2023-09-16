import { useEffect, useState } from 'react';
import { FastAverageColor } from 'fast-average-color';
import Global from 'global/global';
import { PropsPlaylistCard } from 'componentes/PlaylistCard/types/propsPlaylistCard.module';
import PlaylistCard from 'componentes/PlaylistCard/PlaylistCard';
import styles from './userProfile.module.css';
import defaultThumbnailPlaylist from '../../../assets/imgs/DefaultThumbnailPlaylist.jpg';

interface PropsUserProfile {
  refreshSidebarData: Function;
}

export default function UserProfile({ refreshSidebarData }: PropsUserProfile) {
  const userName = 'usuarioprovisionalcambiar';

  const [thumbnail, setThumbnail] = useState<string>(defaultThumbnailPlaylist);
  const [mainColorThumbnail, setMainColorThumbnail] = useState('');
  const [playbackHistory, setPlaybackHistory] = useState<PropsPlaylistCard[]>(
    []
  );

  const handleLoadProfile = async () => {
    const fetchUrlGetUser = `${Global.backendBaseUrl}usuarios/${userName}`;

    const resGetUser = await fetch(fetchUrlGetUser);
    const resGetUserJson = await resGetUser.json();

    setThumbnail(resGetUserJson.photo);

    const playlistPromises: Promise<any>[] = [];
    resGetUserJson.playlists.forEach((playlistName: string) => {
      playlistPromises.push(
        new Promise((resolve) => {
          fetch(`${Global.backendBaseUrl}playlists/dto/${playlistName}`)
            .then((resFetchPlaylistDTO) => {
              return resFetchPlaylistDTO.json();
            })
            .then((resFetchPlaylistDTOJson) => {
              const propsPlaylist: PropsPlaylistCard = {
                name: resFetchPlaylistDTOJson.name,
                description: resFetchPlaylistDTOJson.desdescription,
                owner: resFetchPlaylistDTOJson.owner,
                photo: resFetchPlaylistDTOJson.photo,
                refreshSidebarData,
              };

              resolve(propsPlaylist);
              return propsPlaylist;
            })
            .catch(() => {
              console.log('Unable to get Playlists Data');
            });
        })
      );
    });

    Promise.all(playlistPromises)
      .then((resPlaylistPromises) => {
        setPlaybackHistory([...resPlaylistPromises]);
        return null;
      })
      .catch(() => {
        console.log('Unable to get Playlists Data');
      });
  };

  useEffect(() => {
    handleLoadProfile();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

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
    <div className="d-flex flex-column container-fluid p-0">
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
            alt=""
          />
          <div className="d-flex flex-column">
            <p>Usuario</p>
            <h1>{userName}</h1>
          </div>
        </div>
      </div>
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
          Playlists del usuario
        </h2>
        <div className="d-flex flex-row flex-wrap " style={{ gap: '15px' }}>
          {playbackHistory &&
            playbackHistory.map((playlistItem) => {
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
    </div>
  );
}
