import { useNavigate } from 'react-router-dom';
import styles from './GenreCard.module.css';

interface PropsGenreCard {
  name: string;
  color: string;
}

export default function GenreCard({ name, color }: PropsGenreCard) {
  const navigate = useNavigate();

  const backgroundColor = {
    backgroundColor: color, // Use the provided background color or default to 'blue'
  };

  const handleClick = () => {
    navigate(`/explore/genre/${name}`);
  };

  return (
    <button
      type="button"
      className={`${styles.card} ${backgroundColor}`}
      style={backgroundColor}
      onClick={handleClick}
    >
      {' '}
      <div className={`${styles.genreTitle}`}>{name}</div>
    </button>
  );
}
