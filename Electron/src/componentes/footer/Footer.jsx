import { useEffect, useState } from 'react';
import styles from './footerCss.module.css';
import SongInfo from './SongInfo/SongInfo';
import SongConfig from './SongConfig/SongConfig';
import Player from './Player/Player';

export default function Footer() {
  const [volume, setVolume] = useState(50);

  const changeVolumeParent = (volume) => {
    setVolume(volume);
  };

  return (
    <div
      className={`container-fluid d-flex flex-row space-evenly ${styles.wrapperFooter}`}
    >
      <SongInfo />

      <Player volume={volume} />

      <SongConfig changeVolume={changeVolumeParent} />
    </div>
  );
}
