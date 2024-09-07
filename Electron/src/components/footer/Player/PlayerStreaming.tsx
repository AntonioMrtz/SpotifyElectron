import {
  useEffect,
  useState,
  useRef,
  MouseEventHandler,
  useCallback,
} from 'react';
import Global from 'global/global';
import { getTokenUsername } from 'utils/token';
import { SongsService } from 'swagger/api/services/SongsService';
import { UsersService } from 'swagger/api/services/UsersService';
import styles from './player.module.css';
import TimeSlider from './TimeSlider/TimeSlider';
import { PropsPlayer } from './types/propsPlayer';

export default function PlayerStreaming({
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
    styles.displayNonePlay,
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

  const setVolume = useCallback(() => {
    if (audio.current && audio.current.volume !== undefined) {
      audio.current.volume =
        volume === 0
          ? (audio.current.volume = 0)
          : (audio.current.volume = volume / 100);
    }
  }, [volume]);

  useEffect(() => {
    setVolume();
  }, [setVolume, volume]);

  const handleIncreaseSongStreams = async () => {
    try {
      await SongsService.increaseSongStreamsSongsNameStreamsPatch(songName);
    } catch (err) {
      console.log(`Unable to update number of streams of Song ${songName}`);
      console.log(err);
    }
  };

  const handleUpdatePlaybackHistory = async () => {
    const userName = getTokenUsername();

    try {
      await UsersService.patchPlaybackHistoryUsersNamePlaybackHistoryPatch(
        userName,
        songName,
      );
    } catch (err) {
      console.log(
        `Unable to update User ${userName} playback history with Son ${songName}`,
      );
      console.log(err);
    }
  };

  /* Loads the song and metadata to the Player */

  const handleSongInfo = async () => {
    try {
      if (audio.current) {
        audio.current.pause();
      }

      if (songName === Global.noSongPlaying) return;

      const songData = await SongsService.getSongSongsNameGet(songName);

      handleIncreaseSongStreams();
      handleUpdatePlaybackHistory();

      changeSongInfo({
        name: songData.name,
        thumbnail: songData.thumbnail,
        artist: songData.artist,
      });

      const audioStreamingURL = songData.url;

      if (audioStreamingURL !== undefined) {
        audio.current = new Audio(audioStreamingURL);
      }

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

            if (audio.current.currentTime === 0) {
              handleIncreaseSongStreams();
            }
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
    } catch {
      console.log('Unable to fetch the song');
    }
  };

  useEffect(() => {
    if (audio.current) {
      audio.current.pause();
      handlePause();
    }
    handleSongInfo();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [songName, changeSongInfo]);

  useEffect(() => {
    /* Pause audio if component unmount */
    return () => {
      if (audio.current) {
        audio.current.pause();
        handlePause();
      }
    };
  }, []);

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
        <button
          type="button"
          onClick={play}
          className={`${displayNonePlay}`}
          data-testid="player-play-button"
        >
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
