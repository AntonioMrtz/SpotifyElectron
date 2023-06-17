import React from "react";
import styles from "./player.module.css";

export default function Player() {
    return (
        <div className={`d-flex container-fluid flex-column ${styles.playerBarContainer}`}>
            <div
                className={`d-flex container-fluid flex-row ${styles.buttonsPlayerContainer}`}
            >
                <a href="">
                    <i class="fa-solid fa-shuffle fa-fw"></i>
                </a>
                <a href="">
                    <i class="fa-solid fa-backward-step fa-fw"></i>
                </a>
                <a href="">
                    <i class="fa-solid fa-circle-play fa-fw"></i>
                </a>
                <a href="">
                    <i class="fa-solid fa-circle-pause fa-fw"></i>
                </a>
                <a href="">
                    <i class="fa-solid fa-forward-step fa-fw"></i>
                </a>
                <a href="">
                    <i class="fa-solid fa-repeat fa-fw"></i>
                </a>
            </div>

            <div
                className={`d-flex container-fluid flex-row ${styles.barPlayerContainer}`}
            >
                
                <p>1:26</p>

                <div className={`d-flex container-fluid ${styles.playerContainer}`}>
                    --------------------------------------------------------------------------------------------</div>

                <p>3:46</p>

            </div>
        </div>
    );
}
