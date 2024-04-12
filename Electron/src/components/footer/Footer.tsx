import React, { useState } from 'react';
import SongArchitecture from 'global/SongArchitecture';
import Global from 'global/global';
import styles from './footer.module.css';
import SongInfo from './SongInfo/SongInfo';
import SongConfig from './SongConfig/SongConfig';
import PlayerStreaming from './Player/PlayerStreaming';
import PlayerFiles from './Player/PlayerFiles';

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

      {Global.songArchitecture === SongArchitecture.STREAMING_ARCHITECTURE ? (
        <PlayerStreaming
          volume={volume}
          songName={songName}
          changeSongInfo={setSongInfo}
        />
      ) : (
        <PlayerFiles
          volume={volume}
          songName={songName}
          changeSongInfo={setSongInfo}
        />
      )}

      <SongConfig changeVolume={setVolume} />
    </div>
  );
}
