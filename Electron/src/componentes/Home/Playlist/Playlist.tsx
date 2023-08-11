import styles from './playlistCss.module.css';
import { PropsPlaylist } from '../types/propsPlaylist.module';
import { Link } from 'react-router-dom';
import { useState,MouseEvent } from 'react';

// ... (importaciones y definición de componente)

export default function Home(props: PropsPlaylist) {
  const [displayPlay, setdisplayPlay] = useState(styles.displayTruePlay);
  const [displayPause, setdisplayPause] = useState(styles.displayNonePlay);
  const [Playing, setPlaying] = useState(false);

  let urlPlaylist = '/playlist/' + props.name;

  const handlePlay = (): void => {
    if (Playing === false) {
      setdisplayPause(styles.displayTruePlay);
      setdisplayPlay(styles.displayNonePlay);
      setPlaying(true);
    } else {
      setdisplayPlay(styles.displayTruePlay);
      setdisplayPause(styles.displayNonePlay);
      setPlaying(false);
    }
  };

  const handleButtonClick = (e: MouseEvent<HTMLButtonElement>) => {
    e.stopPropagation(); // Detener la propagación del evento de clic
    e.preventDefault()
    handlePlay();
  };

  return (
    <span className={`rounded ${styles.card}`}>
      <Link to={urlPlaylist} key={props.name}>
        <div className={`${styles.imgContainer}`}>
          <img src={props.photo} className={`card-img-top rounded`} />
          <button
            className={`${styles.hoverablePlayButton} ${displayPlay}`}
            onClick={handleButtonClick}
          >
            <i className={`fa-solid fa-circle-play ${styles.playButton}`}></i>
          </button>
          <button
            className={`${styles.hoverablePlayButton} ${displayPause}`}
            onClick={handleButtonClick}
          >
            <i className={`fa-solid fa-circle-pause ${styles.playButton}`}></i>
          </button>
        </div>
        <div className={`${styles.cardBody}`}>
          <h5 className={`${styles.tituloLista}`}>{props.name}</h5>
          <p className={`${styles.autorLista}`}>{props.description}</p>
        </div>
      </Link>
    </span>
  );
}
