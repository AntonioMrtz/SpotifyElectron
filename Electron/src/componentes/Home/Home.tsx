import styles from './homeCss.module.css';
import Playlist from './Playlist/Playlist';
import Global from 'global/global';
import { PropsPlaylist } from './types/propsPlaylist.module';
import { useEffect, useState } from 'react';
import defaultThumbnailPlaylist from '../../assets/imgs/DefaultThumbnailPlaylist.jpg';



interface PropsHome {

  changeSongName: Function;

}

export default function Home(props: PropsHome) {

  const handleDoubleClick = () => {

    props.changeSongName("p3")

  }


  const [playlists, setPlaylists] = useState<PropsPlaylist[]>();

  const handlePlaylists = () => {

    fetch(Global.backendBaseUrl + 'playlists/', {
      headers: { 'Access-Control-Allow-Origin': '*' },
    })
      .then((res) => res.json())
      .then((res) => {
        if (res['playlists']) {
          let propsPlaylists: PropsPlaylist[] = [];

          for (let obj of res['playlists'].slice(0, 5)) {
            obj = JSON.parse(obj);

            let propsPlaylist: PropsPlaylist = {
              name: obj['name'],
              photo:
                obj['photo'] === '' ? defaultThumbnailPlaylist : obj['photo'],
              description: obj['description'],
              song_names: obj['song_names']
            };

            propsPlaylists.push(propsPlaylist);
          }
          setPlaylists(propsPlaylists);
        }
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

    <div className={`container-fluid d-flex flex-column ${styles.mainContentContainer}`}>
      <div
        className={`container-fluid d-flex flex-column ${styles.columnOfListas}`}
      >
        <header
          className={`container-fluid d-flex flex-row ${styles.columnHead}`}
        >
          <div className={`container-fluid d-flex ${styles.categoryTitleContainer}`}>
            <button className={`${styles.categoryTitle}`} onClick={handleDoubleClick}> Especialmente para ti </button>
          </div>
          <div className={`container-fluid d-flex ${styles.mostrarTodoContainer}`}>
            <button className={`${styles.mostrarTodo}`}>Mostrar todos</button>
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
                  song_names={playlist.song_names}
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
          <div className={`container-fluid d-flex ${styles.categoryTitleContainer}`}>
            <button className={`${styles.categoryTitle}`} onClick={handleDoubleClick}>Escuchado recientemente</button>
          </div>
          <div className={`container-fluid d-flex ${styles.mostrarTodoContainer}`}>
            <button className={`${styles.mostrarTodo}`}>Mostrar todos</button>
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
                  song_names={playlist.song_names}
                />
              );
            })}
        </section>
      </div>
    </div>
  );
}
