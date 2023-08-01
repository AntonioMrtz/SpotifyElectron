import styles from './songInfo.module.css';
import foto from '../../../assets/imgs/quedate.jpg';
import { Favorite, FavoriteBorder } from '@mui/icons-material';
import { Fragment, useEffect, useState } from 'react';

interface PropsSongInfo {
  songInfo: JSON | undefined;
}

export default function SongInfo(props: PropsSongInfo | any) {
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

  const updateSongInfo = async () => {
    if (props.songInfo) {
      //console.log(props.songInfo)
      setName(props.songInfo['name']);
      setThumbnail(props.songInfo['photo']);
      setArtist(props.songInfo['artist']);
      setLiked(false);
    }
  };

  useEffect(() => {
    updateSongInfo();
  }, [props.songInfo]);

  return (
    <div
      className={`d-flex flex-row justify-content-start container-fluid ${styles.songInfoContainer}`}
    >
      {name && (
        <Fragment>
          <img src={thumbnail} alt="" />
          <div className={`d-flex flex-column ${styles.infoCancionContainer}`}>
            <a href="">{name}</a>
            <a href="">{artist}</a>
          </div>
          <div className={`d-flex flex-column ${styles.likeContainer}`}>
            <button onClick={handleLike} className={`btn ${displaylike}`}>
              <i>
                <FavoriteBorder sx={{ fontSize: 18 }} />
              </i>
            </button>
            <button onClick={handleLike} className={`btn ${displaydislike}`}>
              <Favorite sx={{ fontSize: 18, color: 'var(--primary-green)' }} />
            </button>
          </div>
        </Fragment>
      )}
    </div>
  );
}
