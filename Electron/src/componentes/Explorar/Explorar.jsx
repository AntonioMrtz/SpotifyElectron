import { useFetch } from "../../hooks/useFetch"
import styles from "./explorar.module.css"


export default function Explorar() {

  //const {data} = useFetch("http://127.0.0.1:8000/canciones/p3")

  const {data} = useFetch("http://127.0.0.1:8000/listas","prueba")
  console.log(data)

  //const {data} = useFetch("https://dummyjson.com/products/1")

  return (
    <div className={`container-fluid d-flex flex-column`}>
     Hola¿¿
    </div>
  )
}

