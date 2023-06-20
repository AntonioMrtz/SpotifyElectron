import {useEffect} from 'react'
import styles from "./playlist.module.css";


export default function Playlist() {
  return (
    <span className={`container-fluid d-flex flex-row ${styles.wrapperPlaylist}`}>

        <img src={"/assets/imgs/quedate.jpg"} alt="" className="img-fluid img-border-2" />


        <div className="container-fluid d-flex flex-column p-0 ms-2">
            <label>Quedate</label>
            <p>Quevedo</p>

        </div>

    </span>
  )
}
