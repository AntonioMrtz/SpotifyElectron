import { useEffect, useState } from 'react';
import styles from './footerCss.module.css';
import SongInfo from './SongInfo/SongInfo';
import SongConfig from './SongConfig/SongConfig';
import Player from './Player/Player';

interface PropsFooter{

  songName: string

}

export default function Footer(props:PropsFooter) {
  const [volume, setVolume] = useState<number>(50);
  const [songInfo , setSongInfo] = useState<JSON | undefined>();

  const changeVolumeParent = (volume:number) : void => {
    setVolume(volume);
  };

  const changeSongInfo = (data:JSON) : void => {
    setSongInfo(data);
  };


  return (
    <div
      className={`container-fluid d-flex flex-row space-evenly ${styles.wrapperFooter}`}
    >
      <SongInfo songInfo={songInfo}/>

      <Player volume={volume} songName={props.songName} changeSongInfo={changeSongInfo}/>

      <SongConfig changeVolume={changeVolumeParent} />
    </div>
  );
}
