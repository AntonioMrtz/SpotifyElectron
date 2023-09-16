import styles from './songCard.module.css';
import defaultThumbnailPlaylist from '../../assets/imgs/DefaultThumbnailPlaylist.jpg';

export interface PropsSongCard {
  name: string;
  artist: string;
  photo: string;
  changeSongName: Function;
}

export default function SongCard({
  name,
  artist,
  photo,
  changeSongName,
}: PropsSongCard) {
  const handleClickSong = () => {
    changeSongName(name);
  };

  return (
    <button
      type="button"
      className={`${styles.wrapperSongCardGenre}`}
      onDoubleClick={handleClickSong}
    >
      <div className={`${styles.wrapperImageCard}`}>
        <img
          className="img-fluid"
          src={photo === '' ? defaultThumbnailPlaylist : photo}
          alt=""
        />
      </div>
      <div className={`${styles.wrapperTextSongGenre}`}>
        <h5>{name}</h5>
        <p>{artist}</p>
      </div>
    </button>
  );
}
