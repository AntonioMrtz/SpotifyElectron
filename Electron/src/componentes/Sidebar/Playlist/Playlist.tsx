import styles from './playlist.module.css';
import { PropsPlaylist } from '../types/propsPlaylist.module';

export default function Playlist(props: PropsPlaylist) {

  const handleClickPlaylist = () => {

    //TODO
    props.handleUrlPlaylistClicked()
  }

  return (
    <span
      className={`container-fluid d-flex flex-row ${styles.wrapperPlaylist}`}
      onClick={handleClickPlaylist}
    >
      <img src={props.photo} alt="" className="img-fluid img-border-2" />

      <div className="container-fluid d-flex flex-column p-0 ms-2">
        <label>{props.name}</label>
        <p>Lista</p>
      </div>
    </span>
  );
}
