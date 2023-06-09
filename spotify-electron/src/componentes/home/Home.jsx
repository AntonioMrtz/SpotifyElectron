import React from "react";
import styles from "./homeCss.module.css";

export default function Home() {


    return (

        <div className={`container-fluid d-flex flex-column ${styles.principal}`}>
            
            <div className={`container-fluid d-flex flex-column ${styles.columnOfListas}`}>

                <header className={`container-fluid d-flex flex-row ${styles.columnHead}`}>
                    <div className={`container-fluid d-flex ${styles.columnTitle}`}>
                        <h4>Titulo</h4>
                    </div>
                    <div className={`container-fluid d-flex ${styles.mostrarT}`}>
                        <p>Mostrar todos</p>
                    </div>
                </header>

                <section className={`container-fluid d-flex flex-row ${styles.row}`}>
                
                    <div className={`rounded ${styles.card}`}>
                        <img src={require(`./quedate.jpg`)} className={`card-img-top rounded`}/>
                            <div className={`${styles.card_body}`}>
                                <h5 className={`${styles.tituloLista}`}>Quedate</h5>
                                <p className={`${styles.autorLista}`}>Quevedo</p>
                            </div>
                    </div>

                    <div className={`rounded ${styles.card}`}>
                        <img src={require(`./quedate.jpg`)} className={`card-img-top rounded`}/>
                            <div className={`${styles.card_body}`}>
                                <h5 className={`${styles.tituloLista}`}>Quedate</h5>
                                <p className={`${styles.autorLista}`}>Quevedo</p>
                            </div>
                    </div>

                    

                    


                </section>
            </div>

            <div className={`container-fluid d-flex flex-column ${styles.columnOfListas}`}>

                <div className={`container-fluid d-flex flex-row ${styles.columnHead}`}>
                    <h4 className={`${styles.columnTitle}`}>
                        Titulo
                    </h4>
                    <p className={`${styles.mostrarT}`}>
                        Mostrar todos
                    </p>
                </div>

                <div className={`container-fluid d-flex flex-row ${styles.row}`}>
                
                <div className={`rounded ${styles.card}`}>
                        <img src={require(`./quedate.jpg`)} className={`card-img-top rounded`}/>
                            <div className={`${styles.card_body}`}>
                                <h5 className={`${styles.tituloLista}`}>Quedate</h5>
                                <p className={`${styles.autorLista}`}>Quevedo</p>
                            </div>
                    </div>

                    <div className={`rounded ${styles.card}`}>
                        <img src={require(`./quedate.jpg`)} className={`card-img-top rounded`}/>
                            <div className={`${styles.card_body}`}>
                                <h5 className={`${styles.tituloLista}`}>Quedate</h5>
                                <p className={`${styles.autorLista}`}>Quevedo</p>
                            </div>
                    </div>

                    <div className={`rounded ${styles.card}`}>
                        <img src={require(`./quedate.jpg`)} className={`card-img-top rounded`}/>
                            <div className={`${styles.card_body}`}>
                                <h5 className={`${styles.tituloLista}`}>Quedate</h5>
                                <p className={`${styles.autorLista}`}>Quevedo</p>
                            </div>
                    </div>

                    <div className={`rounded ${styles.card}`}>
                        <img src={require(`./quedate.jpg`)} className={`card-img-top rounded`}/>
                            <div className={`${styles.card_body}`}>
                                <h5 className={`${styles.tituloLista}`}>Quedate</h5>
                                <p className={`${styles.autorLista}`}>Quevedo</p>
                            </div>
                    </div>


                </div>
            </div>

            <div className={`container-fluid d-flex flex-column ${styles.columnOfListas}`}>

                <div className={`container-fluid d-flex flex-row ${styles.columnHead}`}>
                    <h4 className={`${styles.columnTitle}`}>
                        Titulo
                    </h4>
                    <p className={`${styles.mostrarT}`}>
                        Mostrar todos
                    </p>
                </div>

                <div className={`container-fluid d-flex flex-row ${styles.row}`}>
                
                <div className={`rounded ${styles.card}`}>
                        <img src={require(`./quedate.jpg`)} className={`card-img-top rounded`}/>
                            <div className={`${styles.card_body}`}>
                                <h5 className={`${styles.tituloLista}`}>Quedate</h5>
                                <p className={`${styles.autorLista}`}>Quevedo</p>
                            </div>
                    </div>

                    <div className={`rounded ${styles.card}`}>
                        <img src={require(`./quedate.jpg`)} className={`card-img-top rounded`}/>
                            <div className={`${styles.card_body}`}>
                                <h5 className={`${styles.tituloLista}`}>Quedate</h5>
                                <p className={`${styles.autorLista}`}>Quevedo</p>
                            </div>
                    </div>

                    <div className={`rounded ${styles.card}`}>
                        <img src={require(`./quedate.jpg`)} className={`card-img-top rounded`}/>
                            <div className={`${styles.card_body}`}>
                                <h5 className={`${styles.tituloLista}`}>Quedate</h5>
                                <p className={`${styles.autorLista}`}>Quevedo</p>
                            </div>
                    </div>

                    <div className={`rounded ${styles.card}`}>
                        <img src={require(`./quedate.jpg`)} className={`card-img-top rounded`}/>
                            <div className={`${styles.card_body}`}>
                                <h5 className={`${styles.tituloLista}`}>Quedate</h5>
                                <p className={`${styles.autorLista}`}>Quevedo</p>
                            </div>
                    </div>


                </div>
            </div>

            
        </div>


        

    );

}
