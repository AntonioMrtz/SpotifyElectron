import Global from 'global/global';
import { useEffect, useState } from 'react';
import styles from './homeCss.module.css';
import Playlist from './Playlist/Playlist';
import { PropsPlaylist } from './types/propsPlaylist.module';
import defaultThumbnailPlaylist from '../../assets/imgs/DefaultThumbnailPlaylist.jpg';

export default function Home() {
  const [playlists, setPlaylists] = useState<PropsPlaylist[]>();

  const handlePlaylists = () => {
    fetch(`${Global.backendBaseUrl}playlists/`, {
      headers: { 'Access-Control-Allow-Origin': '*' },
    })
      .then((resFetchPlaylists) => resFetchPlaylists.json())
      .then((resFetchPlaylistsJson) => {
        if (resFetchPlaylistsJson.playlists) {
          const propsPlaylists: PropsPlaylist[] = [];

          resFetchPlaylistsJson.playlists
            .slice(0, 5)
            .forEach((resPlaylistFetch: any) => {
              const resPlaylistFetchJson = JSON.parse(resPlaylistFetch);

              const propsPlaylist: PropsPlaylist = {
                name: resPlaylistFetchJson.name,
                photo:
                  resPlaylistFetchJson.photo === ''
                    ? defaultThumbnailPlaylist
                    : resPlaylistFetchJson.photo,
                description: resPlaylistFetchJson.description,
              };

              propsPlaylists.push(propsPlaylist);

              setPlaylists(propsPlaylists);
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
              /* onClick={} */
            >
              {' '}
              Especialmente para ti{' '}
            </button>
          </div>
          <div
            className={`container-fluid d-flex ${styles.mostrarTodoContainer}`}
          >
            <button type="button" className={`${styles.mostrarTodo}`}>
              Mostrar todos
            </button>
          </div>
        </header>

        <ul className={`container-fluid d-flex flex-row ${styles.row}`}>
          {playlists &&
            playlists.map((playlist) => {
              return (
                <Playlist
                  name={playlist.name}
                  photo={playlist.photo}
                  description={playlist.description}
                  key={playlist.name + playlist.description}
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
              /* onClick={} */
            >
              Escuchado recientemente
            </button>
          </div>
          <div
            className={`container-fluid d-flex ${styles.mostrarTodoContainer}`}
          >
            <button type="button" className={`${styles.mostrarTodo}`}>
              Mostrar todos
            </button>
          </div>
        </header>

        <section className={`container-fluid d-flex flex-row ${styles.row}`}>
          {playlists &&
            playlists.map((playlist) => {
              return (
                <Playlist
                  name={playlist.name}
                  photo={playlist.photo}
                  description={playlist.description}
                  key={playlist.name + playlist.description}
                />
              );
            })}
        </section>
      </div>
    </div>
  );
}
