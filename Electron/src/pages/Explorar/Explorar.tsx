import { useEffect, useState } from 'react';
import Global from 'global/global';
import genreColorsMap from 'utils/genre';
import styles from './explorar.module.css';
import GenreCard from '../../components/Cards/GenreCard/GenreCard';

export default function Explorar() {
  const [isSearchBarBeingUsed, setIsSearchBarBeingUsed] = useState(false);

  const [generos, setGeneros] = useState<{}>();

  const getGeneros = async () => {
    fetch(encodeURI(`${Global.backendBaseUrl}generos/`))
      .then((res) => res.json())
      .then(async (res) => {
        setGeneros(res);
        return null;
      })
      .catch(() => console.log('Cannot get genres'));
  };
  useEffect(() => {
    getGeneros();
  }, []);

  return (
    <div className={`container-fluid d-flex flex-column ${styles.principal}`}>
      <div
        className={`container-fluid d-flex flex-column ${styles.columnofGeneros}`}
      >
        <header className="container-fluid d-flex flex-row mb-4">
          <div className={`d-flex ${styles.searchBarWrapper}`}>
            <i className="me-2 fa-solid fa-magnifying-glass fa-fw" />
            <input
              type="text"
              placeholder="¿Qué te apetece escuchar?"
              className={`${styles.inputSearchBar}`}
            />
          </div>
        </header>
        <header className="container-fluid d-flex flex-row">
          <div className={`container-fluid d-flex ${styles.columnTitle}`}>
            <h4>Explorar Todo</h4>
          </div>
        </header>
        <div
          className={`container-fluid d-flex flex-row ${styles.cardContainer}`}
        >
          {generos &&
            Object.values(generos).map((genero) => {
              return (
                <GenreCard
                  key={genero as string}
                  name={genero as string}
                  color={genreColorsMap[genero as string]}
                />
              );
            })}
        </div>
      </div>
    </div>
  );
}
