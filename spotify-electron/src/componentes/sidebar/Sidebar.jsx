import React from "react";
import styles from "./sideBarCss.module.css";

export default function Sidebar() {
    return (
        <div className={`container-fluid ${styles.wrapperNavbar}`}>
            <header className={`${styles.header}`}>
                <ul className={`${styles.ul}`}>
                    <li className={`${styles.headerLi}`}>
                        <a href="">
                            <i className={`fa-solid fa-house fa-fw ${styles.headerI}`}></i>
							<span className={`${styles.headerI}`}>Inicio</span>
                        </a>
                    </li>
					<li className={`${styles.headerLi}`}>
                        <a href="">
                            <i className={`fa-solid fa-magnifying-glass fa-fw ${styles.headerI}`}></i>
							<span className={`${styles.headerI}`}>Buscar</span>
                        </a>
                    </li>

                </ul>
            </header>
        </div>
    );
}
