import React from "react";
import styles from "./footerCss.module.css";

export default function Footer() {
    return (
        <div
            className={`container-fluid d-flex flex-row space-evenly ${styles.wrapperFooter}`}
        >
            <div
                className={`d-flex flex-row justify-content-start container-fluid ${styles.songInfoContainer}`}
            >
                
              <img className="img-rounded" src={require(`./quedate.jpg`)} alt="" />

              <div className={`d-flex flex-column ${styles.infoCancionContainer}`}>
                  <a href="">Quedate</a>
                  <a href="">Francisco Quevedo</a>

              </div>

              <div className={`d-flex flex-column ${styles.likeContainer}`}>
                  <a href=""><i class="fa-regular fa-heart"></i></a>
              </div>

            </div>
            <div
                className={`d-flex container-fluid  justify-content-center ${styles.playerBarContainer}`}
            >
                hola
            </div>
            <div
                className={`d-flex container-fluid justify-content-end ${styles.settingsContainer}`}
            >
                hola
            </div>
        </div>
    );
}
