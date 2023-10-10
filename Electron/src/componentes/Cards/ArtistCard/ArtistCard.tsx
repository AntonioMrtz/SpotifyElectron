import { Link, useNavigate } from 'react-router-dom';
import styles from '../cards.module.css';
import { PropsArtistCard } from './types/propsArtistCard';
import defaultThumbnailPlaylist from '../../../assets/imgs/DefaultThumbnailPlaylist.jpg';

export default function ArtistCard({ name, photo }: PropsArtistCard) {
  const navigate = useNavigate();

  const urlArtist = `/artist/${name}`;

  const handleClickArtist = (event: any) => {
    event.preventDefault();
    event.stopPropagation();
    navigate(urlArtist);
  };

  return (
    // eslint-disable-next-line react/jsx-no-useless-fragment
    <>
      <Link
        to={urlArtist}
        key={urlArtist + name}
        className={`rounded ${styles.card}`}
      >
        <div className={`${styles.imgContainer} ${styles.imgContainerArtist}`}>
          <img
            src={photo === '' ? defaultThumbnailPlaylist : photo}
            className="card-img-top rounded"
            alt="artist thumbnail"
          />
        </div>
        <div className={`${styles.cardBody}`}>
          <h5 className={`${styles.tituloLista}`}>{name}</h5>
          <button
            type="button"
            onClick={handleClickArtist}
            className={`${styles.autorLista}`}
          >
            Artista
          </button>
        </div>
      </Link>
    </>
  );
}
