import { useEffect, useState ,useRef } from "react";
import styles from "./player.module.css";
import TimeSlider from "./TimeSlider/TimeSlider";

/**
 * 
 * @param {Number} volume
 *  
 */
export default function Player(props) {
    /*
     * PLAYER
     */

    /* Global audio variable for the component, has the logic of playing the songs */
    const [audio, setAudio] = useState(new Audio("assets/audio/cancion.mp3"));
    /** Control variable for knowing when music is being played or not*/
    const [isPlaying, setPlaying] = useState(false);

    /*
     * PLAYER BUTTON HANDLERS
     */

    const play = () => {
        if (!isPlaying) {
            audio.play();
            handlePlay();
            setSongDuration(audio.duration); // not updating every 0.5s as playback time
        }
    };

    const pause = () => {
        if (isPlaying) {
            audio.pause();
            handlePause();
        }
    };

    const setVolume = () => {
        props.volume == 0
            ? (audio.volume = 0)
            : (audio.volume = props.volume / 100);
    };

    /**
     * Modifies buttons and control variables when the play button is clicked
     */
    const handlePlay = () => {
        setPlaying(true);
        setDisplayNonePlay(styles.displayNonePlay);
        setDisplayNonePause("");
    };

    /**
     * Modifies buttons and control variables when the pause button is clicked
     */
    const handlePause = () => {
        setPlaying(false);
        setDisplayNonePlay("");
        setDisplayNonePause(styles.displayNonePause);
    };

    /* Play/Pause Button manager */
    const [displayNonePlay, setDisplayNonePlay] = useState("");
    const [displayNonePause, setDisplayNonePause] = useState(
        styles.displayNonePlay
    );

    
    /*
     * PLAYBACK TIME MANAGING
     */

    /* Hooks for updating the children Playbar */
    let [playBackTime, setPlayBackTime] = useState(0);
    let [songDuration, setSongDuration] = useState(0);
    
    /* Update playback time  */
    const changePlayBackTime = (value) => {
        audio.currentTime = value;
    };
    const SECOND_MS = 500;
    
    useEffect(() => {
        const interval = setInterval(() => {
            if (audio.currentTime != undefined) {
                setPlayBackTime(audio.currentTime);

                if (audio.currentTime === audio.duration) {
                    handlePause();
                }
            }
        }, SECOND_MS);

        return () => clearInterval(interval); // This represents the unmount function, in which you need to clear your interval to prevent memory leaks.
    }, []);


    /* Manages volume given from parent */
    useEffect(() => {
        setVolume(props.volume);
    }, [props.volume]);

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

            <TimeSlider
                playbacktime={playBackTime}
                songDuration={songDuration}
                changePlayBackTime={changePlayBackTime}
            />
        </div>
    );
}
