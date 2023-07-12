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


  const [mainColorThumbnail, setMainColorThumbnail] = useState('')


  /* Get current Playlist Name */
  const location = useLocation();
  let playlistName = decodeURIComponent(
    location.pathname.split('/').slice(-1)[0]
  );

  const [thumbnail, setThumbnail] = useState<string>('');
  const [numberSongs, setNumberSongs] = useState<number>(0);
  const [songs, setSongs] = useState<PropsSongs[]>();

  const handlePlaylistData = () => {
    fetch(encodeURI(Global.backendBaseUrl + 'playlists/dto/' + playlistName))
      .then((res) => res.json())
      .then((res) => {


        setThumbnail( res["photo"]==='' ? defaultThumbnailPlaylist : res["photo"])


        if (res['song_names']) {
          setNumberSongs(res['song_names'].length);
          let propsSongs: PropsSongs[] = [];

          for (let obj of res['song_names']) {
            let propsSong: PropsSongs = {
              name: obj,
              index: 0,
              handleSongCliked: props.changeSongName,
            };

            propsSongs.push(propsSong);
          }

          setSongs(propsSongs);
        }
      })
      .catch((error) => {
        console.log('No se puedo obtener la playlist');
      });
  };

  useEffect(() => {
    handlePlaylistData();
  }, [location]);

  useEffect(() => {
    /*     const fac = new FastAverageColor();

    fac.getColorAsync(`${thumbnail}?cross-origin=Anonymous`)
        .then(color => {

            setMainColorThumbnail(color.hex)
            console.log('Average color', color);
        })
        .catch(e => {
            console.log(e);
        }); */


    const fac = new FastAverageColor()

    let options = {

      crossOrigin : "*"
    }

    fac
      .getColorAsync(thumbnail,options)
      .then((color) => {
        setMainColorThumbnail(color.hex);
      })
      .catch((e) => {
        //console.log(e);
      });

      fac.destroy()



  }, [thumbnail]);


  return (
    <div
      className={`d-flex container-fluid flex-column ${styles.wrapperPlaylist}`}
    >
      <div
        className={`d-flex container-fluid flex-column ${styles.backgroundFilter} ${styles.header}`}
        style={{ backgroundColor: `${mainColorThumbnail}` }}
      >
        <div className={`d-flex flex-row container-fluid ${styles.nonBlurred}`}>
          <div className={``}>
            <img className="img-fluid" src={`${thumbnail}`} alt="" />
          </div>

          <div
            className={`d-flex container-fluid flex-column ${styles.headerText}`}
          >
            <p>Álbum</p>
            <h1>{playlistName}</h1>
            <p>{numberSongs} canciones</p>
          </div>
        </div>

        <div className={` ${styles.nonBlurred} ${styles.subhHeaderPlaylist}`}>
          Subheader
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
                  index={index + 1}
                  handleSongCliked={props.changeSongName}
                />
              );
            })}
        </ul>
      </div>
    </div>
  );
}
