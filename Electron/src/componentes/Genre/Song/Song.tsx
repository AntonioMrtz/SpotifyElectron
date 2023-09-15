import styles from './song.module.css';
import defaultThumbnailPlaylist from '../../../assets/imgs/DefaultThumbnailPlaylist.jpg';

export interface PropsSongGenre {
  name: string;
  artist: string;
  photo: string;
  changeSongName: Function;
}

export default function Song({
  name,
  artist,
  photo,
  changeSongName,
}: PropsSongGenre) {
  const handleClickSong = () => {
    changeSongName(name);
  };

  return (
    <button
      type="button"
      className={`${styles.wrapperSongCardGenre}`}
      onClick={handleClickSong}
    >
      <div>
        <img className="img-fluid" src={defaultThumbnailPlaylist} alt="" />
      </div>
      <div className={`${styles.wrapperTextSongGenre}`}>
        <h5>{name}</h5>
        <p>{artist}</p>
      </div>
    </button>
  );
}
