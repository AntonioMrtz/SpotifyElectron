import { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import Global from 'global/global';
import styles from './playlist.module.css';
import Song from './Song/Song';
import { PropsSongs } from 'componentes/Sidebar/types/propsSongs.module';
import { FastAverageColor } from 'fast-average-color';
import defaultThumbnailPlaylist from '../../assets/imgs/DefaultThumbnailPlaylist.jpg';

interface PropsPlaylist {
  changeSongName: Function;
}

export default function Playlist(props: PropsPlaylist) {
  const [mainColorThumbnail, setMainColorThumbnail] = useState('');

  /* Get current Playlist Name */
  const location = useLocation();
  let playlistName = decodeURIComponent(
    location.pathname.split('/').slice(-1)[0]
  );


  const [thumbnail, setThumbnail] = useState<string>('');
  const [numberSongs, setNumberSongs] = useState<number>(0);
  const [description, setDescription] = useState<string>('');
  const [displayPlay, setdisplayPlay] = useState('');
  const [displayPause, setdisplayPause] = useState(styles.displayNonePlay);
  const [displayDislike, setdisplayDislike] = useState('');
  const [displayLike, setdisplayLike] = useState(styles.displayNoneLike);
  const [Playing, setPlaying] = useState(false);
  const [Liked, setLiked] = useState(false);
  const [songs, setSongs] = useState<PropsSongs[]>();



  const handlePlay = ():void=>{
    if(Playing == false){
      setdisplayPause('');
      setdisplayPlay(styles.displayNonePlay);
      setPlaying(true);
    }else{
      setdisplayPlay('');
      setdisplayPause(styles.displayNonePlay);
      setPlaying(false);
    }
  }

  const handleLike = () : void=>{
    if(Liked == false){
      setdisplayLike('');
      setdisplayDislike(styles.displayNoneLike);
      setLiked(true);
    }else{
      setdisplayDislike('');
      setdisplayLike(styles.displayNoneLike);
      setLiked(false);
    }
  }

  let getTotalDurationPlaylist = () => {
    let totalDuration = 0;

    if (songs) {
      for (let song of songs) {
        totalDuration += song.duration;
      }
    }
    return totalDuration;
  };

  const loadPlaylistData = async () => {
    fetch(encodeURI(Global.backendBaseUrl + 'playlists/dto/' + playlistName))
      .then((res) => res.json())
      .then(async (res) => {
        setDescription(res['description'])
        setThumbnail(res['photo'] === '' ? defaultThumbnailPlaylist : res['photo']);
        if (res['song_names']) {
          setNumberSongs(res['song_names'].length);
          let propsSongs: PropsSongs[] = [];

          for (let obj of res['song_names'].reverse()) {
            let propsSong: PropsSongs = {
              name: obj,
              playlistName: playlistName,
              artistName: '',
              duration:0,
              index: 0,

              handleSongCliked: props.changeSongName,
              refreshPlaylistData: loadPlaylistData,
            };

            let artistNameAndDuration;
            try {
              const response = await fetch(
                Global.backendBaseUrl + 'canciones/dto/' + obj
              );
              const data = await response.json();
              artistNameAndDuration = {
                artist: data['artist'],
                duration: data['duration'],
              };
            } catch (error) {
              console.log('Unable to get Song: ' + error);
              artistNameAndDuration = { artist: null, duration: null };
            }

            propsSong['artistName'] = artistNameAndDuration.artist;
            propsSong['duration'] = artistNameAndDuration.duration;

            propsSongs.push(propsSong);
          }

          setSongs(propsSongs);
        }
      })
      .catch((error) => {
        console.log('No se puede obtener la playlist');
      });
  };

  useEffect(() => {
    loadPlaylistData();
  }, [location]);

  /* Process photo color */
  useEffect(() => {
    const fac = new FastAverageColor();

    let options = {
      crossOrigin: '*',
    };

    fac
      .getColorAsync(thumbnail, options)
      .then((color) => {
        setMainColorThumbnail(color.hex);
      })
      .catch((e) => {
        //console.log(e);
      });

    fac.destroy();
  }, [thumbnail]);


  /*  */

  return (
    <div
      className={`d-flex container-fluid flex-column ${styles.wrapperPlaylist}`}
    >
      <div
        className={`d-flex container-fluid flex-column ${styles.backgroundFilter} ${styles.header}`}
        style={{ backgroundColor: `${mainColorThumbnail}` }}
      >
        <div className={`d-flex flex-row container-fluid ${styles.nonBlurred}`}>
          <button className={`${styles.wrapperThumbnail}`}>
            <img className="" src={`${thumbnail}`} alt="" />
          </button>

          <div
            className={`d-flex container-fluid flex-column ${styles.headerText}`}
          >
            <p>Álbum</p>
            <h1>{playlistName}</h1>
            <p className={`${styles.descriptionText}`}>{description}</p>
            <div className={`d-flex flex-row`}>

              <p>{numberSongs} canciones</p>
              <p className={`me-2 ms-2`}>•</p>
              <p>{secondsToHoursAndMinutes(getTotalDurationPlaylist())} aproximadamente</p>

            </div>
          </div>
        </div>

        <div className={` ${styles.nonBlurred} ${styles.subhHeaderPlaylist}`}>
          <button className={`${styles.hoverablePlayButton} ${displayPlay}`} onClick={handlePlay}>
            <i className="fa-solid fa-circle-play" style={{ color: 'var(--primary-green)',fontSize:'3rem' }}></i>
          </button>
          <button className={`${styles.hoverablePlayButton} ${displayPause}`} onClick={handlePlay}>
            <i className="fa-solid fa-circle-pause" style={{ color: 'var(--primary-green)',fontSize:'3rem' }}></i>
          </button>
          <button className={`${styles.hoverableItemubheader} ${displayDislike}`} onClick={handleLike}>
            <i className="fa-regular fa-heart" style={{ color: 'var(--secondary-white)',fontSize:'1.75rem' }}></i>
          </button>
          <button className={`${displayLike}`} onClick={handleLike}>
            <i className="fa-solid fa-heart" style={{ color: 'var(--primary-green)',fontSize:'1.75rem' }}></i>
          </button>
          <button className={`${styles.hoverableItemubheader}`}>
            <i className="fa-regular fa-circle-down" style={{ color: 'var(--secondary-white)',fontSize:'1.75rem' }}></i>
          </button>
          <button className={`${styles.hoverableItemubheader}`}>
            <i
              className="fa-solid fa-ellipsis"
              style={{ color: 'var(--secondary-white)' }}
            ></i>
          </button>
        </div>
      </div>

      <div className={`d-flex container-fluid ${styles.wrapperSongTable}`}>
        <ul className={`d-flex flex-column container-fluid`}>
          <li
            className={`container-fluid ${styles.gridContainer} ${styles.gridContainerFirstRow}`}
          >
            <span className={` ${styles.songNumberTable}`}>#</span>
            <span
              className={` ${styles.songTitleTable}`}
              style={{ color: 'var(--secondary-white)' }}
            >
              Título
            </span>
            <span className={` ${styles.gridItem}`}>
              <i className="fa-regular fa-clock"></i>
            </span>
          </li>

          {songs &&
            songs.map((song, index) => {
              return (
                <Song
                  key={index}
                  name={song.name}
                  playlistName={playlistName}
                  artistName={song.artistName}
                  index={index + 1}
                  duration={song.duration}
                  handleSongCliked={props.changeSongName}
                  refreshPlaylistData={loadPlaylistData}
                />
              );
            })}
        </ul>
      </div>
    </div>
  );
}



function secondsToHoursAndMinutes(seconds:number) {
  const hours = Math.floor(seconds / 3600);
  const remainingSeconds = seconds % 3600;
  const minutes = Math.floor(remainingSeconds / 60);

  return hours+" h "+minutes+" min ";
}
