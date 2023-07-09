import styles from './playlist.module.css';

interface PropsPlaylist {

  name : string,
  photo : string,

}

export default function Playlist(props: PropsPlaylist) {


  return (
    <a
      href=""
      className={`container-fluid d-flex flex-row ${styles.wrapperPlaylist}`}
    >
      <img src={props.photo} alt="" className="img-fluid img-border-2" />

      <div className="container-fluid d-flex flex-column p-0 ms-2">
        <label>{props.name}</label>
      </div>
    </a>
  );
}
