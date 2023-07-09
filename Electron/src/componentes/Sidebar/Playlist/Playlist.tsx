import styles from './playlist.module.css';
import { useEffect } from 'react';

interface PropsPlaylist {
  name: string;
  photo: string;
}

export default function Playlist(props: PropsPlaylist) {

  const handleClickPlaylist = () => {

    //TODO
  }

 /*  useEffect(() => {

    if(props.photo === ''){
      import foto from '../../../assets/imgs/quedate.jpg';
      props.photo= {foto};


    }

  }, []) */


  return (
    <span
      className={`container-fluid d-flex flex-row ${styles.wrapperPlaylist}`}
      onClick={handleClickPlaylist}
    >
      <img src={props.photo} alt="" className="img-fluid img-border-2" />

      <div className="container-fluid d-flex flex-column p-0 ms-2">
        <label>{props.name}</label>
      </div>
    </span>
  );
}
