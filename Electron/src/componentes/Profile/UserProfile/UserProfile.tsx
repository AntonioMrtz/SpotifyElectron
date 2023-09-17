import { useEffect, useState } from 'react';
import { FastAverageColor } from 'fast-average-color';
import Global from 'global/global';
import { PropsPlaylistCard } from 'componentes/PlaylistCard/types/propsPlaylistCard.module';
import SongCard, { PropsSongCard } from 'componentes/SongCard/SongCard';
import PlaylistCard from 'componentes/PlaylistCard/PlaylistCard';
import { useParams } from 'react-router-dom';
import styles from './userProfile.module.css';
import defaultThumbnailPlaylist from '../../../assets/imgs/DefaultThumbnailPlaylist.jpg';

export enum UserType {
  USER = 'usuario',
  ARTIST = 'artista',
}

interface PropsUserProfile {
  userType: UserType;
  refreshSidebarData: Function;
  changeSongName: Function;
}

export default function UserProfile({
  userType,
  changeSongName,
  refreshSidebarData,
}: PropsUserProfile) {
  // Use the useParams hook to get the id parameter from the URL
  const { id } = useParams();

  const [thumbnail, setThumbnail] = useState<string>(defaultThumbnailPlaylist);
  const [mainColorThumbnail, setMainColorThumbnail] = useState('');
  const [playlists, setPlaylists] = useState<PropsPlaylistCard[]>([]);
  const [playbackHistory, setPlaybackHistory] = useState<PropsSongCard[]>([]);
  const [uploadedSongs, setUploadedSongs] = useState<PropsSongCard[]>([]);

  const loadPlaylists = async (resGetUserJson: any) => {
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
        setPlaylists([...resPlaylistPromises]);
        return null;
      })
      .catch(() => {
        console.log('Unable to get Playlists Data');
      });
  };

  const loadPlaybackHistory = (resGetUserJson: any) => {
    const songPromises: Promise<any>[] = [];
    resGetUserJson.playback_history.forEach((songName: string) => {
      songPromises.push(
        new Promise((resolve) => {
          fetch(`${Global.backendBaseUrl}canciones/dto/${songName}`)
            .then((resFetchSongDTO) => {
              return resFetchSongDTO.json();
            })
            .then((resFetchSongDTOJson) => {
              const propsSong: PropsSongCard = {
                name: resFetchSongDTOJson.name,
                photo: resFetchSongDTOJson.photo,
                artist: resFetchSongDTOJson.artist,
                changeSongName,
              };

              resolve(propsSong);
              return propsSong;
            })
            .catch(() => {
              console.log('Unable to get Songs Data');
            });
        })
      );
    });

    Promise.all(songPromises)
      .then((resSongPromises) => {
        setPlaybackHistory([...resSongPromises]);
        return null;
      })
      .catch(() => {
        console.log('Unable to get Songs Data');
      });
  };

  const loadSongsFromArtist = (resGetUserJson: any) => {
    const songPromises: Promise<any>[] = [];

    resGetUserJson.uploaded_songs.forEach((songName: string) => {
      songPromises.push(
        new Promise((resolve) => {
          fetch(`${Global.backendBaseUrl}canciones/dto/${songName}`)
            .then((resFetchSongDTO) => {
              return resFetchSongDTO.json();
            })
            .then((resFetchSongDTOJson) => {
              const propsSong: PropsSongCard = {
                name: resFetchSongDTOJson.name,
                photo: resFetchSongDTOJson.photo,
                artist: resFetchSongDTOJson.artist,
                changeSongName,
              };

              resolve(propsSong);
              return propsSong;
            })
            .catch(() => {
              console.log('Unable to get Songs Data from Artist');
            });
        })
      );
    });

    Promise.all(songPromises)
      .then((resSongPromises) => {
        setUploadedSongs([...resSongPromises]);
        return null;
      })
      .catch(() => {
        console.log('Unable to get Songs Data from Artist');
      });
  };

  const handleLoadProfile = async () => {
    const fetchUrlGetUser = `${Global.backendBaseUrl}${userType}s/${id}`;

    const resGetUser = await fetch(fetchUrlGetUser);

    if (resGetUser.status === 404) return;
    const resGetUserJson = await resGetUser.json();

    loadPlaylists(resGetUserJson);
    setThumbnail(resGetUserJson.photo);

    if (userType === UserType.USER) {
      loadPlaybackHistory(resGetUserJson);
    } else if (userType === UserType.ARTIST) {
      loadSongsFromArtist(resGetUserJson);
    }
  };

  useEffect(() => {
    handleLoadProfile();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

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
            alt="thumbnail user"
            className={`${styles.thumbnailUser}`}
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

              <p style={{ textTransform: 'capitalize' }}>
                {userType} {userType === UserType.ARTIST && 'verificado'}
              </p>
            </div>
            <h1>{id}</h1>
          </div>
        </div>
      </div>

      {userType === UserType.ARTIST && (
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
            Canciones más populares del artista
          </h2>
          <div className="d-flex flex-row flex-wrap " style={{ gap: '15px' }}>
            {uploadedSongs &&
              uploadedSongs.map((songItem, index) => {
                return (
                  <SongCard
                    // eslint-disable-next-line react/no-array-index-key
                    key={`${songItem.name}${index}`}
                    name={songItem.name}
                    photo={songItem.photo}
                    artist={songItem.artist}
                    changeSongName={songItem.changeSongName}
                  />
                );
              })}
          </div>
        </div>
      )}
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
          Playlists del {userType}
        </h2>
        <div className="d-flex flex-row flex-wrap " style={{ gap: '15px' }}>
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
            Historial de reproducción
          </h2>
          <div className="d-flex flex-row flex-wrap " style={{ gap: '15px' }}>
            {playbackHistory &&
              playbackHistory.map((songItem, index) => {
                return (
                  <SongCard
                    // eslint-disable-next-line react/no-array-index-key
                    key={`${songItem.name}${index}`}
                    name={songItem.name}
                    photo={songItem.photo}
                    artist={songItem.artist}
                    changeSongName={songItem.changeSongName}
                  />
                );
              })}
          </div>
        </div>
      )}
    </div>
  );
}
