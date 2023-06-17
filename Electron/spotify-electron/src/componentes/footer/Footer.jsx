import React from "react";
import styles from "./footerCss.module.css";
import SongInfo from "./SongInfo/SongInfo";
import SongConfig from "./SongConfig/SongConfig";
import Player from "./Player/Player";


export default function Footer() {
    return (
        <div
            className={`container-fluid d-flex flex-row space-evenly ${styles.wrapperFooter}`}
        >

            <SongInfo/>

            <Player/>
           
            <SongConfig/>

        </div>
    );
}
