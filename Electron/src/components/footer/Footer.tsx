import { useState } from 'react';
import styles from './footer.module.css';
import SongInfo from './SongInfo/SongInfo';
import SongConfig from './SongConfig/SongConfig';
import PlayerStreaming from './Player/PlayerStreaming';

interface PropsFooter {
  songName: string;
}

export default function Footer({ songName }: PropsFooter) {
  const [volume, setVolume] = useState<number>(50);
  const [songInfo, setSongInfo] = useState<JSON | undefined>();

  return (
    <div
      className={`container-fluid d-flex flex-row space-evenly ${styles.wrapperFooter}`}
    >
      <SongInfo songInfo={songInfo} />

      <PlayerStreaming
        volume={volume}
        songName={songName}
        changeSongInfo={setSongInfo}
      />

      <SongConfig changeVolume={setVolume} />
    </div>
  );
}
