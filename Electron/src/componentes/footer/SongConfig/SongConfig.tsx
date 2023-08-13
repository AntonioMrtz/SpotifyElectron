import styles from './songConfig.module.css';
import VolumeSlider from './VolumeSlider/VolumeSlider';

interface PropsSongConfig {
  changeVolume: (volume: number) => void;
}

export default function SongConfig({ changeVolume }: PropsSongConfig) {
  const handleFullScreen = (): void => {
    window.electron.toogleFullScreen.sendMessage('toogle-fullscreen');
  };

  return (
    <div
      className={`d-flex container-fluid justify-content-end ${styles.settingsContainer} `}
    >
      <button type="button" className="btn">
        <i className="fa-solid fa-microphone fa-fw" />
      </button>
      <button type="button" className="btn">
        <i className="fa-solid fa-bars fa-fw" />
      </button>
      <button type="button" className="btn">
        <i className="fa-solid fa-desktop fa-fw" />
      </button>
      <VolumeSlider changeVolume={changeVolume} />
      <button type="button" onClick={handleFullScreen} className="btn">
        <i className="fa-solid fa-up-right-and-down-left-from-center fa-fw" />
      </button>
    </div>
  );
}
