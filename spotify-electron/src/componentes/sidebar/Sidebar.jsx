import React from "react";
import styles from "./sideBarCss.module.css";
import variables from "./../../index.css"

import { useState } from "react";

export default function Sidebar() {


	const [isHovered, setIsHovered] = useState(false);

	const handleMouseOver = () => {
	  setIsHovered(true);
	};
  
	const handleMouseOut = () => {
	  setIsHovered(false);
	};
  
	const getColor = () => {
	  return isHovered ? '#dfdfdf' : '#b3b3b3'; // Cambia 'red' y 'blue' por los colores que desees
	};


	const [isHoveredBuscar, setIsHoveredBuscar] = useState(false);

	const handleMouseOverBuscar = () => {
		setIsHoveredBuscar(true);
	};
  
	const handleMouseOutBuscar = () => {
		setIsHoveredBuscar(false);
	};
  
	const getColorBuscar = () => {
	  return isHoveredBuscar ? '#dfdfdf' : '#b3b3b3'; // Cambia 'red' y 'blue' por los colores que desees
	};



    return (


		
        <div className={`container-fluid ${styles.wrapperNavbar}`}>
            <header className={`${styles.header}`}>
                <ul className={`${styles.ul}`}>
                    <li className={`${styles.headerLi}`} 
						onMouseOver={handleMouseOver}
						onMouseOut={handleMouseOut}
						
					>
                        <a href="">
                            <i style={{ color: getColor() }} className={`fa-solid fa-house fa-fw ${styles.headerI}`}></i>
							<span style={{ color: getColor() }} className={`${styles.headerI}`}>Inicio</span>
                        </a>
                    </li>
					<li className={`${styles.headerLi}`}
						onMouseOver={handleMouseOverBuscar}
						onMouseOut={handleMouseOutBuscar}
					>
                        <a className={`${styles.aHeader}`} href="">
                            <i style={{ color: getColorBuscar() }} className={`fa-solid fa-magnifying-glass fa-fw ${styles.headerI}`}></i>
							<span style={{ color: getColorBuscar() }} className={`${styles.headerI}`}>Buscar</span>
                        </a>
                    </li>

                </ul>
            </header>
        </div>
    );
}
