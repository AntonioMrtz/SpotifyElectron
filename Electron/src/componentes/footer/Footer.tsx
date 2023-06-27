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
  const [thumbnailUrl , setThumbnailUrl] = useState<string>('');
  
  const changeVolumeParent = (volume:number) : void => {
    setVolume(volume);
  };

  const changeThumbnail = (url:string) : void => {
    setThumbnailUrl(url);
  };


  return (
    <div
      className={`container-fluid d-flex flex-row space-evenly ${styles.wrapperFooter}`}
    >
      <SongInfo thumbnailUrl={thumbnailUrl}/>

      <Player volume={volume} songName={props.songName} changeThumbnail={changeThumbnail}/>

      <SongConfig changeVolume={changeVolumeParent} />
    </div>
  );
}
