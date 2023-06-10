import React, { useEffect, useState } from "react";
import styles from "./sideBarCss.module.css";
import variables from "./../../index.css";

export default function Sidebar() {

	//* MENU HOVER

    let [listItemInicio, setHoverInicio] = useState("");
    let [listItemBuscar, setHoverBuscar] = useState("");


    const [isHoveredInicio, setIsHovered] = useState(false);
	const [isHoveredBuscar, setIsHoveredBuscar] = useState(false);

    const handleMouseOverInicio = () => {
        setIsHovered(true);
    };

    const handleMouseOutInicio = () => {
        setIsHovered(false);
    };

    const handleMouseOverBuscar = () => {
        setIsHoveredBuscar(true);
    };

    const handleMouseOutBuscar = () => {
        setIsHoveredBuscar(false);
    };

    useEffect(() => {
        setHoverInicio(isHoveredInicio ? styles.linksubtle : "");
        setHoverBuscar(isHoveredBuscar ? styles.linksubtle : "");
    }, [isHoveredBuscar, isHoveredInicio]);




    return (
        <div className={`container-fluid ${styles.wrapperNavbar}`}>
            <header className={`${styles.header}`}>
                <ul className={`${styles.ul}`}>
                    <li
                        className={`${styles.headerLi} ${listItemInicio}`}
                        onMouseOver={handleMouseOverInicio}
                        onMouseOut={handleMouseOutInicio}
                    >
                        <a href="">
                            <i
                                className={`fa-solid fa-house fa-fw ${styles.headerI}`}
                            ></i>
                            <span className={`${styles.headerI}`}>Inicio</span>
                        </a>
                    </li>
                    <li
                        className={`${styles.headerLi} ${listItemBuscar}`}
                        onMouseOver={handleMouseOverBuscar}
                        onMouseOut={handleMouseOutBuscar}
                    >
                        <a className={`${styles.aHeader}`} href="/explorar">
                            <i
                                className={`fa-solid fa-magnifying-glass fa-fw ${styles.headerI}`}
                            ></i>
                            <span className={`${styles.headerI}`}>Buscar</span>
                        </a>
                    </li>
                </ul>
            </header>
        </div>
    );
}
