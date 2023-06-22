import styles from "./songConfig.module.css";
import VolumeSlider from "./VolumeSlider/VolumeSlider";

export default function SongConfig(props) {
    return (
        <div
            className={`d-flex container-fluid justify-content-end ${styles.settingsContainer} `}
        >
            <a href="">
                <i class="fa-solid fa-microphone fa-fw"></i>
            </a>
            <a href="">
                <i class="fa-solid fa-bars fa-fw"></i>
            </a>
            <a href="">
                <i class="fa-solid fa-desktop fa-fw"></i>
            </a>
            <VolumeSlider changeVolume={props.changeVolume}/>

            <a href="">
                <i class="fa-solid fa-up-right-and-down-left-from-center fa-fw"></i>
            </a>
        </div>
    );
}
