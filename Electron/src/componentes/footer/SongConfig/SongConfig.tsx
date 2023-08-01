import { ClassNames } from '@emotion/react';
import styles from './songConfig.module.css';
import VolumeSlider from './VolumeSlider/VolumeSlider';

interface PropsSongConfig {
  changeVolume: (volume: number) => void;
}

export default function SongConfig(props: PropsSongConfig) {
  const handleFullScreen = (): void => {
    window.electron.toogleFullScreen.sendMessage('toogle-fullscreen');
  };

  return (
    <div
      className={`d-flex container-fluid justify-content-end ${styles.settingsContainer} `}
    >
      <button className="btn">
        <i className="fa-solid fa-microphone fa-fw"></i>
      </button>
      <button className="btn">
        <i className="fa-solid fa-bars fa-fw"></i>
      </button>
      <button className="btn">
        <i className="fa-solid fa-desktop fa-fw"></i>
      </button>
      <VolumeSlider changeVolume={props.changeVolume} />
      <button onClick={handleFullScreen} className="btn">
        <i className="fa-solid fa-up-right-and-down-left-from-center fa-fw"></i>
      </button>
    </div>
  );
}
