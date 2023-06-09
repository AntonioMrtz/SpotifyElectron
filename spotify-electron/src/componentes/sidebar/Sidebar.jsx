import React from "react";
import styles from "./sideBarCss.module.css";

export default function Sidebar() {
    return (
        <div className={`container-fluid ${styles.wrapperNavbar}`}>
            <header className={`${styles.header}`}>
                <ul className={`${styles.ul}`}>
                    <li className={`${styles.headerLi}`}>
                        <a href="">
                            <i className={`fa-solid fa-house fa-fw ${styles.headerI}`}>Home</i>
                        </a>
                    </li>

                    <li>
                        <a href="">
                            {" "}
                            <i class="fa-solid fa-magnifying-glass"> Buscar</i>
                        </a>
                    </li>
                </ul>
            </header>
        </div>
    );
}
