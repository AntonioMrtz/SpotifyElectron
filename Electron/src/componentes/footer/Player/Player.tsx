import { useEffect, useState, useRef, MouseEventHandler } from 'react';
import styles from './player.module.css';
import TimeSlider from './TimeSlider/TimeSlider';


interface PropsPlayer {
  volume : number,
  songName : string
}


export default function Player(props : PropsPlayer) {
  //* PLAYER AUDIO DATA

  /* Global audio variable for the component, has the logic of playing the songs */
  let audio = useRef<HTMLAudioElement | null>(null);

  let songName = props.songName

  /* Loads the song */
  useEffect(() => {

    if(audio.current){

      audio.current.pause()
    }

    fetch('http://127.0.0.1:8000/canciones/'+songName,{"headers":{ 'Access-Control-Allow-Origin': '*' }})
      .then((res) => res.json())
      .then((res) => res['file'])
      .then((res) => {
        let audiobytes_string = res;

        if (audiobytes_string !== undefined) {
          audiobytes_string = audiobytes_string
            .replace('"', '')
            .replace('b', '')
            .replace("'", '')
            .slice(0, -1);
          let dataURI = 'data:audio/mp3;base64,' + audiobytes_string;
          audio.current = new Audio(dataURI);
        }
      })
      .then(() => {

        if(audio.current){

          // Listener that handles the time update of playbacktime
          audio.current.addEventListener('timeupdate', function () {
            
            if(audio.current && audio.current.currentTime && audio.current.duration){
              
              let time = audio.current.currentTime;
              setPlayBackTime(+time.toFixed(2));
    
              if (audio.current.currentTime === audio.current.duration) {
                handlePause();
              }

            }
          });

          // When metadata such as duration,etc is loaded
          audio.current.addEventListener('loadedmetadata', function () {

            if(audio.current){

              audio.current.play()
              handlePlay();
              setSongDuration(audio.current.duration); // not updating every 0.5s as playback time
              setVolume()
            }
            

          });


        }

        // set play and pause functions

        let playWhenFetched = () => {
          return function returns() {

            if(audio.current){
              audio.current.play();
              handlePlay();
              setSongDuration(audio.current.duration); // not updating every 0.5s as playback time

            }
          };
        };

        let pauseWhenFetched = () => {
          return function returns() {

            if(audio.current){

              audio.current.pause();
              handlePause();

            }

          };
        };

        setPlay(playWhenFetched);
        setPause(pauseWhenFetched);
        
      });
  }, [props.songName]);

  //* PLAYER BUTTON HANDLERS

  /* Methods are declared when song is fetched */
  const [play, setPlay] = useState<MouseEventHandler>();
  const [pause, setPause] = useState<MouseEventHandler>();

  /**
   * Modifies buttons and control variables when the play button is clicked
   */
  const handlePlay = () => {
    setDisplayNonePlay(styles.displayNonePlay);
    setDisplayNonePause('');
  };

  /**
   * Modifies buttons and control variables when the pause button is clicked
   */
  const handlePause = () => {
    setDisplayNonePlay('');
    setDisplayNonePause(styles.displayNonePause);
  };

  /* Play/Pause Button manager */
  const [displayNonePlay, setDisplayNonePlay] = useState('');
  const [displayNonePause, setDisplayNonePause] = useState(
    styles.displayNonePlay
  );

  //* PLAYBACK TIME MANAGING

  /* Hooks for updating the children Playbar */
  let [playBackTime, setPlayBackTime] = useState(0);
  let [songDuration, setSongDuration] = useState(0);

  /* Update playback time  */
  const changePlayBackTime = (value:number) => {
    if(audio.current && audio.current.currentTime){

      audio.current.currentTime = value;
    }
  };

  //* VOLUME

  /* Manages volume given from parent */
  useEffect(() => {
    setVolume();
  }, [props.volume]);

  const setVolume = () => {

    if (audio.current && audio.current.volume!==undefined) {
      props.volume == 0
        ? (audio.current.volume = 0)
        : (audio.current.volume = props.volume / 100);
    }
  };

  return (
    <div
      className={`d-flex container-fluid flex-column ${styles.playerBarContainer}`}
    >
      <div
        className={`d-flex container-fluid flex-row ${styles.buttonsPlayerContainer}`}
      >
        <span>
          <i className="fa-solid fa-shuffle fa-fw"></i>
        </span>
        <span>
          <i className="fa-solid fa-backward-step fa-fw"></i>
        </span>
        <span onClick={play} className={`${displayNonePlay}`}>
          <i className="fa-solid fa-circle-play fa-fw"></i>
        </span>
        <span onClick={pause} className={`${displayNonePause}`}>
          <i className="fa-solid fa-circle-pause fa-fw"></i>
        </span>
        <span>
          <i className="fa-solid fa-forward-step fa-fw"></i>
        </span>

        <span>
          <i className="fa-solid fa-repeat fa-fw"></i>
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
