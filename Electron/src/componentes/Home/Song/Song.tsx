import styles from './songCss.module.css';
import { PropsPlaylist } from '../types/propsPlaylist.module';

export default function Home(props : PropsPlaylist) {



  return (
    <span className={`rounded ${styles.card}`}>
              <img src={props.photo} className={`card-img-top rounded`} />
              <div className={`${styles.card_body}`}>
                <h5 className={`${styles.tituloLista}`}>{props.name}</h5>
                <p className={`${styles.autorLista}`}>{props.description}</p>
              </div>
    </span>
  );

}
