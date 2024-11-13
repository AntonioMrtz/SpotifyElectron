import { Favorite, FavoriteBorder } from '@mui/icons-material';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './songInfo.module.css';
import { PropsSongInfo } from './types/propsSongInfo';
import defaultThumbnailPlaylist from '../../../assets/imgs/DefaultThumbnailPlaylist.jpg';

export default function SongInfo({ name, artist, thumbnail }: PropsSongInfo) {
  const navigate = useNavigate();

  const [songName, setSongName] = useState<string>();
  const [songThumbnail, setSongThumbnail] = useState<string>();
  const [songArtist, setSongArtist] = useState<string>();
  const [liked, setLiked] = useState(false);
  const [displaylike, setdisplaylike] = useState('');
  const [displaydislike, setdisplaydislike] = useState(styles.displayNoneLike);

  const handleLike = (): void => {
    if (liked === false) {
      setdisplaylike(styles.displayNoneLike);
      setdisplaydislike('');
      setLiked(true);
    } else {
      setdisplaylike('');
      setdisplaydislike(styles.displayNoneLike);
      setLiked(false);
    }
  };

  const handleClickArtist = () => {
    navigate(`/artist/${artist}`);
  };

  useEffect(() => {
    const updateSongInfo = () => {
      if (name && artist) {
        setSongName(name);
        setSongThumbnail(thumbnail || defaultThumbnailPlaylist);
        setSongArtist(artist);
        setLiked(false);
      }
    };
    updateSongInfo();
  }, [artist, name, thumbnail]);

  return (
    <div
      className={`d-flex flex-row justify-content-start container-fluid ${styles.songInfoContainer}`}
    >
      {songName && (
        <>
          <img src={songThumbnail} alt="song thumbnail" />
          <div className={`d-flex flex-column ${styles.infoCancionContainer}`}>
            <button
              data-testid="songinfo-name"
              type="button"
              onClick={() => {}}
            >
              {songName}
            </button>
            <button type="button" onClick={handleClickArtist}>
              {songArtist}
            </button>
          </div>
          <div className={`d-flex flex-column ${styles.likeContainer}`}>
            <button
              type="button"
              onClick={handleLike}
              className={`btn ${displaylike}`}
              data-testid="songinfo-like-button"
            >
              <i>
                <FavoriteBorder sx={{ fontSize: 18 }} />
              </i>
            </button>
            <button
              type="button"
              onClick={handleLike}
              className={`btn ${displaydislike}`}
              data-testid="songinfo-unlike-button"
            >
              <Favorite sx={{ fontSize: 18, color: 'var(--primary-green)' }} />
            </button>
          </div>
        </>
      )}
    </div>
  );
}
