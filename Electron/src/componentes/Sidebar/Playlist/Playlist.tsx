import {useEffect} from 'react'
import styles from "./playlist.module.css";
import foto from "../../../assets/imgs/quedate.jpg"

export default function Playlist() {
  return (
    <a href="" className={`container-fluid d-flex flex-row ${styles.wrapperPlaylist}`}>

        <img src={foto} alt="" className="img-fluid img-border-2" />


        <div className="container-fluid d-flex flex-column p-0 ms-2">
            <label>Quedate</label>
            <p>Quevedo</p>

        </div>

    </a>
  )
}
