import styles from "./songInfo.module.css";
import foto from "../../../assets/imgs/quedate.jpg"

export default function SongInfo() {
    return (
        <div
            className={`d-flex flex-row justify-content-start container-fluid ${styles.songInfoContainer}`}
        >
            <img
                className="img-rounded"
                src={foto}
                alt=""
            />

            <div
                className={`d-flex flex-column ${styles.infoCancionContainer}`}
            >
                <a href="">Quedate</a>
                <a href="">Francisco Quevedo</a>
            </div>

            <div className={`d-flex flex-column ${styles.likeContainer}`}>
                <a href="">
                    <i className="fa-regular fa-heart"></i>
                </a>
            </div>
        </div>
    );
}
