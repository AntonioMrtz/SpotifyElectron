import { Link, useNavigate } from 'react-router-dom';
import styles from '../cards.module.css';
import { PropsUserCard } from './types/propsUserCard';
import defaultThumbnailPlaylist from '../../../assets/imgs/DefaultThumbnailPlaylist.jpg';

export default function UserCard({ name, photo }: PropsUserCard) {
  const navigate = useNavigate();

  const urlUser = `/user/${name}`;

  const handleClickUser = (event: any) => {
    event.preventDefault();
    event.stopPropagation();
    navigate(urlUser);
  };

  return (
    // eslint-disable-next-line react/jsx-no-useless-fragment
    <>
      <Link
        to={urlUser}
        key={urlUser + name}
        className={`rounded ${styles.card}`}
      >
        <div className={`${styles.imgContainer} ${styles.imgContainerArtist}`}>
          <img
            src={photo === '' ? defaultThumbnailPlaylist : photo}
            className="card-img-top rounded"
            alt="user thumbnail"
          />
        </div>
        <div className={`${styles.cardBody}`}>
          <h5 className={`${styles.tituloLista}`}>{name}</h5>
          <button
            type="button"
            onClick={handleClickUser}
            className={`${styles.autorLista}`}
          >
            Usuario
          </button>
        </div>
      </Link>
    </>
  );
}
