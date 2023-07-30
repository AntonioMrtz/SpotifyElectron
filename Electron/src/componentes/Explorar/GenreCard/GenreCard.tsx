import { useEffect, useState } from "react";
import styles from "./GenreCard.module.css";

interface PropsGenreCard{
    name: any
}
export default function GenreCard(props : PropsGenreCard){
    const [name, setName] = useState<string>('');

  useEffect(() => {
    if (props.name) {
      setName(props.name);
    }
  }, [props]);

    return(
        <button className={`rounded ${styles.card}`}>
            <div className={`${styles.genreTitle}`}>{name}</div>
        </button>
    );
}