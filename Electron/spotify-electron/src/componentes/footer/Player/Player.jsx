import { useEffect, useState ,useRef } from "react";
import styles from "./player.module.css";
import cancion from "./cancion.mp3";
import TimeSlider from "./TimeSlider/TimeSlider";


export default function Player(props) {

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

    const setVolume = () => {

        props.volume==0 ? audio.volume=0 : audio.volume=props.volume/100

    }

    const [isPlaying, setPlaying] = useState(false);

    /* Play button */

    const [displayNonePlay, setDisplayNonePlay] = useState("");
    const [displayNonePause, setDisplayNonePause] = useState(
        styles.displayNonePlay
    );


    /* Get current time */

    let [playTime,setPlayTime] = useState(0)

    const SECOND_MS = 500;

    useEffect(() => {
        const interval = setInterval(() => {
            //console.log("Logs every second");
            //console.log(audio.currentTime)
            
            if(audio.currentTime!=undefined){
                
                
                setPlayTime( audio.currentTime )

            }
        }, SECOND_MS);

        return () => clearInterval(interval); // This represents the unmount function, in which you need to clear your interval to prevent memory leaks.
    }, []);


    /* Manages volume given from parent */

    useEffect(() => {
      
        setVolume(props.volume)
        //console.log(props.volume)

    }, [props.volume])


    /* Manages playTime  */

    const changePlayTime = (value) => {

        //audio.pause()
        audio.currentTime=value;
        //audio.play()
        console.log("audio duration "+audio.duration)
    }
    


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

            <TimeSlider song={cancion} playTime={playTime} songDuration={audio.duration} changePlayTime={changePlayTime}/>
            
        </div>
    );
}
