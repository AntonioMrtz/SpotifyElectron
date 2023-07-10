import { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import Global from 'global/global';
import styles from './playlist.module.css';

export default function Playlist() {
  /* Get current Playlist Name */
  const location = useLocation();
  let playlistName = decodeURIComponent(location.pathname.split('/').slice(-1)[0]);

  const [thumbnail, setThumbnail] = useState<string>('');

  useEffect(() => {
    fetch(Global.backendBaseUrl + 'playlists/' + playlistName)
      .then((res) => res.json())
      .then((res) => {
        console.log(res);
        setThumbnail(res['photo']);
      })
      .catch((error) => {
        console.log('No se puedo obtener la playlist');
      });
  }, []);

  return (
    <div
      className={`d-flex container-fluid flex-column ${styles.wrapperPlaylist}`}
    >
      <div
        className={`container-fluid d-flex ${styles.backgroundFilter} ${styles.header}`}
        style={{ backgroundImage: `url(${thumbnail})` }}
      >
        <div className={`d-flex flex-row ${styles.nonBlurred}`}>
          <div className={``}>
            <img className="img-fluid" src={thumbnail} alt="" />
          </div>

          <div
            className={`d-flex container-fluid flex-column flex-grow-1 ${styles.headerText}`}
          >
            <h2>Álbum</h2>
            <h1>{playlistName}</h1>
            <p>Info de la canción</p>
          </div>
        </div>
      </div>


    </div>
  );
}
