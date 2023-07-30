import useFetch from "hooks/useFetch"
import styles from "./explorar.module.css"
import { ChangeEvent, FormEvent, useEffect, useState } from 'react';
import ContextMenuSong from "componentes/Playlist/Song/ContextMenuSong/ContextMenuSong"
import { useNavigate } from "react-router-dom"
import Global from "global/global"
import { Console } from "console";
import GenreCard from "./GenreCard/GenreCard";

interface PropsExplorar{

  changeSongName : (songName : string) => void
}


export default function Explorar(props:PropsExplorar) {

  const [generos, setGeneros] = useState<{}>();

  //const {data} = useFetch("http://127.0.0.1:8000/canciones/p3")

  //const { data, loading, error } = useFetch("http://127.0.0.1:8000/listas/");

/*   useEffect(() => {

    console.log(props.changeSongName)
  }, []) */

  
  let navigate = useNavigate()
  const getGeneros = async()=>{
    fetch(encodeURI(Global.backendBaseUrl + 'generos/'))
      .then((res) => res.json())
      .then(async (res) =>{
        setGeneros(res)
        console.log(res)
      })
  }
  useEffect(() => {getGeneros()},[])

  return (
    <div className={`container-fluid d-flex flex-column ${styles.principal}`}>
      <div className={`container-fluid d-flex flex-column ${styles.columnofGeneros}`}>
      <header
          className={`container-fluid d-flex flex-row`}
        >
          <div className={`container-fluid d-flex ${styles.columnTitle}`}>
            <h4>Explorar Todo</h4>
          </div>
        </header>
        <div className={`container-fluid d-flex flex-row ${styles.cardContainer}`}>
        {generos &&
            Object.values(generos).map((genero, index) => {
              return (
                <GenreCard key={index} name={genero} />
              );
            })}
        </div>
      </div >

    </div>
  )
}

