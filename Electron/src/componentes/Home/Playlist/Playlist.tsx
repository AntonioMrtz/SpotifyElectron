import styles from './playlistCss.module.css';
import { PropsPlaylist } from '../types/propsPlaylist.module';
import { Link } from 'react-router-dom';

export default function Home(props: PropsPlaylist) {

  let urlPlaylist = '/playlist/' + props.name;

  return (

    <span className={`rounded ${styles.card}`}>
      <Link to={urlPlaylist} key={props.name}>
        <img src={props.photo} className={`card-img-top rounded`} />
        <div className={`${styles.cardBody}`}>
          <h5 className={`${styles.tituloLista}`}>{props.name}</h5>
          <p className={`${styles.autorLista}`}>{props.description}</p>
        </div>
      </Link>
    </span>

  );

}
