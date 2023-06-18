import { useEffect, useState } from "react";
import styles from "./player.module.css";
import cancion from "./cancion.mp3";

export default function Player() {

    /* Player */

    const [audio, setAudio] = useState( new Audio(cancion) )

    const play = () => {
        if (!isPlaying) {
            audio.play();
            setPlaying(true);
            setDisplayNonePlay(styles.displayNonePlay);
            setDisplayNonePause("");
        }
    };

    const pause = () => {
        if (isPlaying) {
            audio.pause();
            setPlaying(false);
            setDisplayNonePlay("");
            setDisplayNonePause(styles.displayNonePause);
            
        }
    };

    const [isPlaying, setPlaying] = useState(false);

    /* Play button */

    const [displayNonePlay, setDisplayNonePlay] = useState("");
    const [displayNonePause, setDisplayNonePause] = useState(
        styles.displayNonePlay
    );

    return (
        <div
            className={`d-flex container-fluid flex-column ${styles.playerBarContainer}`}
        >
            <div
                className={`d-flex container-fluid flex-row ${styles.buttonsPlayerContainer}`}
            >
                <span>
                    <i class="fa-solid fa-shuffle fa-fw"></i>
                </span>
                <span>
                    <i class="fa-solid fa-backward-step fa-fw"></i>
                </span>
                <span onClick={play} className={`${displayNonePlay}`}>
                    <i class="fa-solid fa-circle-play fa-fw"></i>
                </span>
                <span onClick={pause} className={`${displayNonePause}`}>
                    <i class="fa-solid fa-circle-pause fa-fw"></i>
                </span>
                <span>
                    <i class="fa-solid fa-forward-step fa-fw"></i>
                </span>

                <span>
                    <i class="fa-solid fa-repeat fa-fw"></i>
                </span>
            </div>

            <div
                className={`d-flex container-fluid flex-row ${styles.barPlayerContainer}`}
            >
                <p>1:26</p>

                <div
                    className={`d-flex container-fluid ${styles.playerContainer}`}
                >
                    --------------------------------------------------------------------------------------------
                </div>

                <p>3:46</p>
            </div>
        </div>
    );
}
