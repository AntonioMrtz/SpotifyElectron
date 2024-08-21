import { Favorite, FavoriteBorder } from '@mui/icons-material';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './songInfo.module.css';
import { PropsSongInfo } from './types/propsSongInfo';
import defaultThumbnailPlaylist from '../../../assets/imgs/DefaultThumbnailPlaylist.jpg';

export default function SongInfo({ songInfo }: PropsSongInfo | any) {
  const navigate = useNavigate();

  const [name, setName] = useState<string>();
  const [thumbnail, setThumbnail] = useState<string>();
  const [artist, setArtist] = useState<string>();
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
      if (songInfo) {
        setName(songInfo.name);
        setThumbnail(
          songInfo.photo ? songInfo.photo : defaultThumbnailPlaylist,
        );
        setArtist(songInfo.artist);
        setLiked(false);
      }
    };
    updateSongInfo();
  }, [songInfo]);

  return (
    <div
      className={`d-flex flex-row justify-content-start container-fluid ${styles.songInfoContainer}`}
    >
      {name && (
        <>
          <img src={thumbnail} alt="" />
          <div className={`d-flex flex-column ${styles.infoCancionContainer}`}>
            <button type="button" onClick={() => {}}>
              {name}
            </button>
            <button type="button" onClick={handleClickArtist}>
              {artist}
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
