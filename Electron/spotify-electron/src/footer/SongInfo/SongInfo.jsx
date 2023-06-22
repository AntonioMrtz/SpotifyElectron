import styles from "./songInfo.module.css";

export default function SongInfo() {
    return (
        <div
            className={`d-flex flex-row justify-content-start container-fluid ${styles.songInfoContainer}`}
        >
            <img
                className="img-rounded"
                src={"assets/imgs/quedate.jpg"}
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
                    <i class="fa-regular fa-heart"></i>
                </a>
            </div>
        </div>
    );
}
