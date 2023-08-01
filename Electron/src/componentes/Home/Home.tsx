import styles from './homeCss.module.css';

import Song from './Song/Song';
import Global from 'global/global';
import { PropsPlaylist } from './types/propsPlaylist.module';
import { useEffect, useState } from 'react';
import defaultThumbnailPlaylist from '../../assets/imgs/DefaultThumbnailPlaylist.jpg';
import { Link } from 'react-router-dom';


interface PropsHome {
  changeSongName : Function;
}

export default function Home(props : PropsHome) {

  const handleDoubleClick = () =>{

    props.changeSongName("p3")

  }


  const [playlists, setPlaylists] = useState<PropsPlaylist[]>();

  const handlePlaylists = () => {

    fetch(Global.backendBaseUrl + 'playlists/', {
      headers: { 'Access-Control-Allow-Origin': '*' },
    })
      .then((res) => res.json())
      .then((res) => {
        if(res['playlists']){
          let propsPlaylists: PropsPlaylist[] = [];

          for (let obj of res['playlists']) {
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
    <div className={`container-fluid d-flex flex-column ${styles.principal}`}>
      <div
        className={`container-fluid d-flex flex-column ${styles.columnOfListas}`}
      >
        <header
          className={`container-fluid d-flex flex-row ${styles.columnHead}`}
        >
          <div className={`container-fluid d-flex ${styles.columnTitle}`}>
            <h4 className={`${styles.tituloSeccion}`} onClick={handleDoubleClick}>Especialmente para ti</h4>
          </div>
          <div className={`container-fluid d-flex ${styles.mostrarT}`}>
            <p>Mostrar todos</p>
          </div>
        </header>


        <ul className={`container-fluid d-flex flex-row ${styles.row}`}>
        {playlists &&
              playlists.map((playlist) => {
                let urlPlaylist = '/playlist/' + playlist.name;
                return (
                  <Link to={urlPlaylist} key={playlist.name} className={`${styles.playlistLink}`}>
                    <Song
                      name={playlist.name}
                      photo={playlist.photo}
                      description={playlist.description}
                      song_names={playlist.song_names}
                    />
                  </Link>
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
            <div className={`container-fluid d-flex ${styles.columnTitle}`}>
              <h4 className={`${styles.tituloSeccion}`} onClick={handleDoubleClick}>Escuchado recientemente</h4>
            </div>
            <div className={`container-fluid d-flex ${styles.mostrarT}`}>
              <p>Mostrar todos</p>
            </div>
          </header>

          <section className={`container-fluid d-flex flex-row ${styles.row}`}>
          {playlists &&
              playlists.map((playlist) => {
                let urlPlaylist = '/playlist/' + playlist.name;
                return (
                  <Link to={urlPlaylist} key={playlist.name} className={`${styles.playlistLink}`}>
                    <Song
                      name={playlist.name}
                      photo={playlist.photo}
                      description={playlist.description}
                      song_names={playlist.song_names}
                    />
                  </Link>
                );
              })}


          </section>
        </div>
    </div>
  );
}
