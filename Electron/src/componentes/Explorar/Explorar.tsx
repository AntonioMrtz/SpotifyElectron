import useFetch from "hooks/useFetch"
import styles from "./explorar.module.css"


export default function Explorar() {

  //const {data} = useFetch("http://127.0.0.1:8000/canciones/p3")

  const { data, loading, error } = useFetch("http://127.0.0.1:8000/listas/");

  return (
    <div className={`container-fluid d-flex flex-column`}>
      {data!==null && data.prueba}

    </div>
  )
}

