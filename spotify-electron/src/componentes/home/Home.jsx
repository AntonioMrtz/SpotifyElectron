import React from "react";
import styles from "./homeCss.module.css";

export default function Home() {


    return (

        <div className={`container-fluid ${styles.clase}`}>

            <div className={`${styles.card}`}>
                <img src="..." className={`card-img-top`}/>
                    <div className={`card-body`}>
                        <h5 className={`card-title`}>Quedate</h5>
                        <p className={`card-text`}>Quevedo</p>
                    </div>
            </div>


        </div>

    );


}
