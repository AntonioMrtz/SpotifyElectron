import { useEffect, useState, useRef, MouseEventHandler } from 'react';
import Global from 'global/global';
import styles from './player.module.css';
import TimeSlider from './TimeSlider/TimeSlider';

interface PropsPlayer {
  volume: number;
  songName: string;
  changeSongInfo: (data: JSON) => void;
}

export default function Player({
  volume,
  songName,
  changeSongInfo,
}: PropsPlayer) {
  //* PLAYER AUDIO DATA

  /* Global audio variable for the component, has the logic of playing the songs */
  const audio = useRef<HTMLAudioElement | null>(null);

  //* PLAYER BUTTON HANDLERS

  /* Methods are declared when song is fetched */
  const [play, setPlay] = useState<MouseEventHandler>();
  const [pause, setPause] = useState<MouseEventHandler>();

  /* Play/Pause Button manager */
  const [displayNonePlay, setDisplayNonePlay] = useState('');
  const [displayNonePause, setDisplayNonePause] = useState(
    styles.displayNonePlay
  );

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

  //* PLAYBACK TIME MANAGING

  /* Hooks for updating the children Playbar */
  const [playBackTime, setPlayBackTime] = useState(0);
  const [songDuration, setSongDuration] = useState(0);

  /* Update playback time  */
  const changePlayBackTime = (value: number) => {
    if (audio.current && audio.current.currentTime) {
      audio.current.currentTime = value;
    }
  };

  //* VOLUME

  const setVolume = () => {
    if (audio.current && audio.current.volume !== undefined) {
      audio.current.volume =
        volume === 0
          ? (audio.current.volume = 0)
          : (audio.current.volume = volume / 100);
    }
  };
  /* Manages volume given from parent */
  useEffect(() => {
    setVolume();
  }, [volume]);

  /* Loads the song and metadata to the Player */
  useEffect(() => {
    if (audio.current) {
      audio.current.pause();
    }

    fetch(`${Global.backendBaseUrl}canciones/${songName}`, {
      headers: { 'Access-Control-Allow-Origin': '*' },
    })
      .then((resGetSong) => resGetSong.json())
      .then((resGetSongFetch) => {
        const requestOptions = {
          method: 'PUT',
        };
        const fetchUrlUpdateSong: string = `${Global.backendBaseUrl}canciones/${songName}?number_of_plays=True`;
        fetch(fetchUrlUpdateSong, requestOptions);
        fetch(
          `${Global.backendBaseUrl}canciones/dto/${songName}?number_of_plays=True`
        )
          .then((res) => res.json())
          .then((res) => {
            changeSongInfo(res);
            return null;
          })
          .catch(() => console.log('Unable to get Son Data'));

        return resGetSongFetch.file;
      })
      .then((res) => {
        let audioBytesString = res;

        if (audioBytesString !== undefined) {
          audioBytesString = audioBytesString
            .replace('"', '')
            .replace('b', '')
            .replace("'", '')
            .slice(0, -1);
          const dataURI = `data:audio/mp3;base64,${audioBytesString}`;
          audio.current = new Audio(dataURI);
        }

        return null;
      })
      .then(() => {
        if (audio.current) {
          // Listener that handles the time update of playbacktime
          audio.current.addEventListener('timeupdate', () => {
            if (
              audio.current &&
              audio.current.currentTime &&
              audio.current.duration
            ) {
              const time = audio.current.currentTime;
              setPlayBackTime(+time.toFixed(2));

              if (audio.current.currentTime === audio.current.duration) {
                handlePause();
              }
            }
          });

          // When metadata such as duration,etc is loaded
          audio.current.addEventListener('loadedmetadata', () => {
            if (audio.current) {
              audio.current.play();
              handlePlay();
              setSongDuration(audio.current.duration); // not updating every 0.5s as playback time
              setVolume();
            }
          });
        }

        // set play and pause functions

        const playWhenFetched = () => {
          return function returns() {
            if (audio.current) {
              audio.current.play();
              handlePlay();
              setSongDuration(audio.current.duration); // not updating every 0.5s as playback time
            }
          };
        };

        const pauseWhenFetched = () => {
          return function returns() {
            if (audio.current) {
              audio.current.pause();
              handlePause();
            }
          };
        };

        setPlay(playWhenFetched);
        setPause(pauseWhenFetched);

        return null;
      })
      .catch(() => {
        console.log('Unable to fetch the song');
      });
  }, [songName]);

  return (
    <div
      className={`d-flex container-fluid flex-column ${styles.playerBarContainer}`}
    >
      <div
        className={`d-flex container-fluid flex-row ${styles.buttonsPlayerContainer}`}
      >
        <button type="button">
          <i className="fa-solid fa-shuffle fa-fw" />
        </button>
        <button type="button">
          <i className="fa-solid fa-backward-step fa-fw" />
        </button>
        <button type="button" onClick={play} className={`${displayNonePlay}`}>
          <i className="fa-solid fa-circle-play fa-fw" />
        </button>
        <button type="button" onClick={pause} className={`${displayNonePause}`}>
          <i className="fa-solid fa-circle-pause fa-fw" />
        </button>
        <button type="button">
          <i className="fa-solid fa-forward-step fa-fw" />
        </button>

        <button type="button">
          <i className="fa-solid fa-repeat fa-fw" />
        </button>
      </div>

      <TimeSlider
        playBackTime={playBackTime}
        initialSongDuration={songDuration}
        changePlayBackTime={changePlayBackTime}
      />
    </div>
  );
}
