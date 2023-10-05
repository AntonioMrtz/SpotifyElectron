import Global from 'global/global';
import { useCallback, useEffect, useState } from 'react';
import LoadingCircle from 'componentes/AdvancedUIComponents/LoadingCircle/LoadingCircle';
import { useNavigate } from 'react-router-dom';
import ArtistCard from 'componentes/Cards/ArtistCard/ArtistCard';
import { PropsArtistCard } from 'componentes/Cards/ArtistCard/types/propsArtistCard';
import styles from './homeCss.module.css';
import PlaylistCard from '../Cards/PlaylistCard/PlaylistCard';
import { PropsPlaylistCard } from '../Cards/PlaylistCard/types/propsPlaylistCard';
import defaultThumbnailPlaylist from '../../assets/imgs/DefaultThumbnailPlaylist.jpg';

interface PropsHome {
  refreshSidebarData: Function;
}

export default function Home({ refreshSidebarData }: PropsHome) {
  const navigate = useNavigate();

  const [playlists, setPlaylists] = useState<PropsPlaylistCard[]>();
  const [loadingPlaylists, setLoadingPlaylists] = useState(true);

  const handlePlaylists = useCallback(() => {
    fetch(`${Global.backendBaseUrl}playlists/`, {})
      .then((resFetchPlaylists) => resFetchPlaylists.json())
      .then((resFetchPlaylistsJson) => {
        if (resFetchPlaylistsJson.playlists) {
          const propsPlaylists: PropsPlaylistCard[] = [];

          resFetchPlaylistsJson.playlists
            .slice(0, 5)
            .forEach((resPlaylistFetch: any) => {
              const resPlaylistFetchJson = JSON.parse(resPlaylistFetch);

              const propsPlaylist: PropsPlaylistCard = {
                name: resPlaylistFetchJson.name,
                photo:
                  resPlaylistFetchJson.photo === ''
                    ? defaultThumbnailPlaylist
                    : resPlaylistFetchJson.photo,
                description: resPlaylistFetchJson.description,
                refreshSidebarData,
                owner: resPlaylistFetchJson.owner,
              };

              propsPlaylists.push(propsPlaylist);

              setPlaylists(propsPlaylists);
            });
        }
        return null;
      })
      .then(() => {
        setLoadingPlaylists(false);
        return null;
      })
      .catch((error) => {
        console.log(error);
        console.log('No se pudieron obtener las playlists');
      });
  }, [refreshSidebarData]);

  const [artists, setArtists] = useState<PropsArtistCard[]>();
  const [loadingArtists, setLoadingArtists] = useState(true);

  const handleArtists = useCallback(() => {
    fetch(`${Global.backendBaseUrl}artistas/`, {
      headers: { 'Access-Control-Allow-Origin': '*' },
    })
      .then((resFetchArtistas) => resFetchArtistas.json())
      .then((resFetchArtistasJson) => {
        if (resFetchArtistasJson.artists) {
          const propsArtists: PropsArtistCard[] = [];

          resFetchArtistasJson.artists.forEach((resArtistFetch: any) => {
            const resArtistFetchJson = JSON.parse(resArtistFetch);

            const propsArtist: PropsArtistCard = {
              name: resArtistFetchJson.name,
              photo:
                resArtistFetchJson.photo === ''
                  ? defaultThumbnailPlaylist
                  : resArtistFetchJson.photo,
            };

            propsArtists.push(propsArtist);

            setArtists(propsArtists);
          });
        }
        return null;
      })
      .then(() => {
        setLoadingArtists(false);
        return null;
      })
      .catch(() => {
        console.log('Unable to get artists');
      });
  }, []);

  useEffect(() => {
    handleArtists();
    handlePlaylists();
  }, [handlePlaylists, handleArtists]);

  return (
    <div
      className={`container-fluid d-flex flex-column ${styles.mainContentContainer}`}
    >
      <div
        className={`container-fluid d-flex flex-column ${styles.columnOfListas}`}
      >
        <header
          className={`container-fluid d-flex flex-row ${styles.columnHead}`}
        >
          <div
            className={`container-fluid d-flex ${styles.categoryTitleContainer}`}
          >
            <button
              type="button"
              className={`${styles.categoryTitle}`}
              onClick={() => {
                navigate(`/showAllItemsPlaylist/Especialmente para ti`);
              }}
            >
              {' '}
              Especialmente para ti{' '}
            </button>
          </div>
          <div
            className={`container-fluid d-flex ${styles.mostrarTodoContainer}`}
          >
            <button
              type="button"
              className={`${styles.mostrarTodo}`}
              onClick={() => {
                navigate(`/showAllItemsPlaylist/Especialmente para ti`);
              }}
            >
              Mostrar todos
            </button>
          </div>
        </header>

        <ul className={`container-fluid d-flex flex-row ${styles.row}`}>
          {loadingPlaylists && <LoadingCircle />}

          {!loadingPlaylists &&
            playlists &&
            playlists.map((playlist) => {
              return (
                <PlaylistCard
                  name={playlist.name}
                  photo={playlist.photo}
                  description={playlist.description}
                  owner={playlist.owner}
                  key={playlist.name + playlist.description}
                  refreshSidebarData={refreshSidebarData}
                />
              );
            })}
        </ul>
      </div>

      <div
        className={`container-fluid d-flex flex-column ${styles.columnOfListas}`}
      >
        <header
          className={`container-fluid d-flex flex-row ${styles.columnHead}`}
        >
          <div
            className={`container-fluid d-flex ${styles.categoryTitleContainer}`}
          >
            <button
              type="button"
              className={`${styles.categoryTitle}`}
              onClick={() => {
                navigate(`/showAllItemsArtist/Artistas recomendados`);
              }}
            >
              Artistas destacados
            </button>
          </div>
          <div
            className={`container-fluid d-flex ${styles.mostrarTodoContainer}`}
          >
            <button
              type="button"
              className={`${styles.mostrarTodo}`}
              onClick={() => {
                navigate(`/showAllItemsArtist/Artistas recomendados`);
              }}
            >
              Mostrar todos
            </button>
          </div>
        </header>

        <section className={`container-fluid d-flex flex-row ${styles.row}`}>
          {loadingArtists && <LoadingCircle />}

          {!loadingArtists &&
            artists &&
            artists.map((artist) => {
              return (
                <ArtistCard
                  name={artist.name}
                  photo={artist.photo}
                  key={artist.name}
                />
              );
            })}
        </section>
      </div>
    </div>
  );
}
