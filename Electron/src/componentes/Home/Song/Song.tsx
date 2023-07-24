import styles from './songCss.module.css';
import foto from '../../../assets/imgs/quedate.jpg';

interface PropsSong {
  changeSongName : Function;
  name: string;
  autor: string;
}

export default function Home(props : PropsSong) {

  const handleDoubleClick = () =>{

    props.changeSongName("p3")

  }

  return (
    <span onClick={handleDoubleClick} className={`rounded ${styles.card}`}>
              <img src={foto} className={`card-img-top rounded`} />
              <div className={`${styles.card_body}`}>
                <h5 className={`${styles.tituloLista}`}>{props.name}</h5>
                <p className={`${styles.autorLista}`}>{props.autor}</p>
              </div>
    </span>
  );

}
