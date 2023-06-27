import styles from "./songInfo.module.css";
import foto from "../../../assets/imgs/quedate.jpg"
import { useEffect, useState } from "react";

interface PropsSongInfo{

    thumbnailUrl : string;

}

export default function SongInfo(props:PropsSongInfo) {

    const [thumbNail,setThumbNail] = useState<any>();

    const fetchImage = async () => {
        const res = await fetch(props.thumbnailUrl);
            const imageBlob = await res.blob();
            const imageObjectURL = URL.createObjectURL(imageBlob);
            setThumbNail(imageObjectURL);
      };
    
      useEffect(() => {
        fetchImage();
      }, [props.thumbnailUrl]);
    
    

    return (
        <div
            className={`d-flex flex-row justify-content-start container-fluid ${styles.songInfoContainer}`}
        >
            <img
                src={thumbNail}
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
