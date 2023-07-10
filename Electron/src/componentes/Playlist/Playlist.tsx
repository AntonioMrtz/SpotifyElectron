import { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import Global from 'global/global';
import styles from './playlist.module.css';

export default function Playlist() {
  /* Get current Playlist Name */
  const location = useLocation();
  let playlistName = decodeURIComponent(
    location.pathname.split('/').slice(-1)[0]
  );

  const [thumbnail, setThumbnail] = useState<string>('');
  const [numberSongs, setNumberSongs] = useState<number>(0);

  useEffect(() => {
    fetch(encodeURI(Global.backendBaseUrl + 'playlists/dto/' + playlistName))
      .then((res) => res.json())
      .then((res) => {
        console.log(res);
        setThumbnail(res['photo']);
        setNumberSongs(res['song_names'].length);
        console.log(res);
      })
      .catch((error) => {
        console.log(
          'URL ' +
            encodeURI(Global.backendBaseUrl + 'playlists/dto/' + playlistName)
        );
        console.log('No se puedo obtener la playlist');
      });
  }, []);

  return (
    <div
      className={`d-flex container-fluid flex-column ${styles.wrapperPlaylist}`}
    >
      <div
        className={`d-flex container-fluid flex-column ${styles.backgroundFilter} ${styles.header}`}
        style={{ backgroundImage: `url(${thumbnail})` }}
      >
        <div className={`d-flex flex-row container-fluid ${styles.nonBlurred}`}>
          <div className={``}>
            <img className="img-fluid" src={thumbnail} alt="" />
          </div>

          <div
            className={`d-flex container-fluid flex-column ${styles.headerText}`}
          >
            <p>Álbum</p>
            <h1>{playlistName}</h1>
            <p>{numberSongs} canciones</p>
          </div>
        </div>

        <div className={` ${styles.nonBlurred} ${styles.subhHeaderPlaylist}`}>
          Subheader
        </div>
      </div>

      <div className={`d-flex container-fluid ${styles.wrapperSongTable}`}>
        <ul className={`d-flex flex-column container-fluid`}>
          <li className={`container-fluid ${styles.gridContainer}`}>
            <span className={` ${styles.gridItem}`}>#</span>
            <span className={` ${styles.gridItem}`}>Título</span>
            <span className={` ${styles.gridItem}`}><i className="fa-regular fa-clock"></i></span>
          </li>

          <li className={`container-fluid ${styles.gridContainer}`}>
            <span className={` ${styles.gridItem}`}>1</span>
            <span className={` ${styles.gridItem} ${styles.songTitleTable}`}>La lucha por la vida</span>
            <span className={` ${styles.gridItem}`}>2:01</span>
          </li>
        </ul>
      </div>
    </div>
  );
}
