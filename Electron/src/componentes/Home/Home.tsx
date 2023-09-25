import Global from 'global/global';
import { useEffect, useState } from 'react';
import LoadingCircle from 'componentes/AdvancedUIComponents/LoadingCircle/LoadingCircle';
import { useNavigate } from 'react-router-dom';
import styles from './homeCss.module.css';
import PlaylistCard from '../PlaylistCard/PlaylistCard';
import { PropsPlaylistCard } from '../PlaylistCard/types/propsPlaylistCard.module';
import defaultThumbnailPlaylist from '../../assets/imgs/DefaultThumbnailPlaylist.jpg';

interface PropsHome {
  refreshSidebarData: Function;
}

export default function Home({ refreshSidebarData }: PropsHome) {
  const navigate = useNavigate();

  const [playlists, setPlaylists] = useState<PropsPlaylistCard[]>();
  const [loading, setLoading] = useState(true);

  const handlePlaylists = () => {
    fetch(`${Global.backendBaseUrl}playlists/`, {
      headers: { 'Access-Control-Allow-Origin': '*' },
    })
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
              setLoading(false);
            });
        }
        return null;
      })
      .catch((error) => {
        console.log(error);
        console.log('No se pudieron obtener las playlists');
      });
  };

  useEffect(() => {
    handlePlaylists();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

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
                navigate(`/allPlaylists/Especialmente para ti`);
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
                navigate(`/allPlaylists/Especialmente para ti`);
              }}
            >
              Mostrar todos
            </button>
          </div>
        </header>

        <ul className={`container-fluid d-flex flex-row ${styles.row}`}>
          {loading && <LoadingCircle />}

          {!loading &&
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
                navigate(`/allPlaylists/Especialmente para ti`);
              }}
            >
              Escuchado recientemente
            </button>
          </div>
          <div
            className={`container-fluid d-flex ${styles.mostrarTodoContainer}`}
          >
            <button
              type="button"
              className={`${styles.mostrarTodo}`}
              onClick={() => {
                navigate(`/allPlaylists/Especialmente para ti`);
              }}
            >
              Mostrar todos
            </button>
          </div>
        </header>

        <section className={`container-fluid d-flex flex-row ${styles.row}`}>
          {loading && <LoadingCircle />}

          {!loading &&
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
        </section>
      </div>
    </div>
  );
}
