import styles from './songConfig.module.css';
import VolumeSlider from './VolumeSlider/VolumeSlider';

interface PropsSongConfig{

  changeVolume : (volume:number) => void 
}

export default function SongConfig(props:PropsSongConfig) {
  return (
    <div
      className={`d-flex container-fluid justify-content-end ${styles.settingsContainer} `}
    >
      <a href="">
        <i className="fa-solid fa-microphone fa-fw"></i>
      </a>
      <a href="">
        <i className="fa-solid fa-bars fa-fw"></i>
      </a>
      <a href="">
        <i className="fa-solid fa-desktop fa-fw"></i>
      </a>
      <VolumeSlider changeVolume={props.changeVolume} />

      <a href="">
        <i className="fa-solid fa-up-right-and-down-left-from-center fa-fw"></i>
      </a>
    </div>
  );
}
