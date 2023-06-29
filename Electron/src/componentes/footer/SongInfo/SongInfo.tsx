import styles from "./songInfo.module.css";
import foto from "../../../assets/imgs/quedate.jpg"
import { useEffect, useState } from "react";

interface PropsSongInfo{

  songInfo : JSON | undefined;

}

export default function SongInfo(props:PropsSongInfo | any) {

    const [name,setName] = useState<string>();
    const [thumbnail,setThumbnail] = useState<string>();
    const [artist,setArtist] = useState<string>();


    const updateSongInfo = async () => {

      if(props.songInfo){

        //console.log(props.songInfo)
        setName(props.songInfo["name"])
        setThumbnail(props.songInfo["photo"])
        setArtist(props.songInfo["artist"])

      };

    }

      useEffect(() => {
        updateSongInfo();
      }, [props.songInfo]);



    return (
        <div
            className={`d-flex flex-row justify-content-start container-fluid ${styles.songInfoContainer}`}
        >
            <img
                src={thumbnail}
                alt=""
            />

            <div
                className={`d-flex flex-column ${styles.infoCancionContainer}`}
            >
                <a href="">{name}</a>
                <a href="">{artist}</a>
            </div>

            <div className={`d-flex flex-column ${styles.likeContainer}`}>
                <a href="">
                    <i className="fa-regular fa-heart"></i>
                </a>
            </div>
        </div>
    );
}
