import { useEffect, useState } from 'react';
import styles from './footerCss.module.css';
import SongInfo from './SongInfo/SongInfo';
import SongConfig from './SongConfig/SongConfig';
import Player from './Player/Player';

interface PropsFooter{

  songName: string

}

export default function Footer(props:PropsFooter) {
  const [volume, setVolume] = useState(50);
  
  const changeVolumeParent = (volume:number) : void => {
    setVolume(volume);
  };


  return (
    <div
      className={`container-fluid d-flex flex-row space-evenly ${styles.wrapperFooter}`}
    >
      <SongInfo />

      <Player volume={volume} songName={props.songName}/>

      <SongConfig changeVolume={changeVolumeParent} />
    </div>
  );
}
