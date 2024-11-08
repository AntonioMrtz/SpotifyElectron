import { useEffect, useState } from 'react';
import SongArchitecture from 'global/SongArchitecture';
import Global from 'global/global';
import { useSongNameChangeContext } from 'hooks/useSongChangeContextApi';
import styles from './footer.module.css';
import SongInfo from './SongInfo/SongInfo';
import SongConfig from './SongConfig/SongConfig';
import PlayerServerless from './Player/PlayerServerless';
import PlayerBlob from './Player/PlayerBlob';
import { PropsSongInfo } from './SongInfo/types/propsSongInfo';

export default function Footer() {
  const { songName } = useSongNameChangeContext();

  const [volume, setVolume] = useState<number>(50);
  const [songInfo, setSongInfo] = useState<PropsSongInfo>({
    name: '',
    artist: '',
    thumbnail: '',
  });

  return (
    <div
      className={`container-fluid d-flex flex-row space-evenly ${styles.wrapperFooter}`}
    >
      <SongInfo
        name={songInfo.name}
        artist={songInfo.artist}
        thumbnail={songInfo.thumbnail}
      />

      {Global.songArchitecture === SongArchitecture.SERVERLESS_ARCHITECTURE ? (
        <PlayerServerless
          volume={volume}
          songName={songName}
          changeSongInfo={setSongInfo}
        />
      ) : (
        <PlayerBlob
          volume={volume}
          songName={songName}
          changeSongInfo={setSongInfo}
        />
      )}

      <SongConfig changeVolume={setVolume} />
    </div>
  );
}
