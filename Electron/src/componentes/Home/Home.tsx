import styles from './homeCss.module.css';
import foto from '../../assets/imgs/quedate.jpg';
import Song from './Song/Song';


interface PropsHome {
  changeSongName : Function;
}

export default function Home(props : PropsHome) {

  const handleDoubleClick = () =>{

    props.changeSongName("p3")

  }

  const handleDoubleClickBeta = () =>{

    props.changeSongName("loquillo")

  }

  const handleDoubleClickP3 = () =>{

    props.changeSongName("The Battle For Everyone's Soul")

  }

  return (
    <div className={`container-fluid d-flex flex-column ${styles.principal}`}>
      <div
        className={`container-fluid d-flex flex-column ${styles.columnOfListas}`}
      >
        <header
          className={`container-fluid d-flex flex-row ${styles.columnHead}`}
        >
          <div className={`container-fluid d-flex ${styles.columnTitle}`}>
            <h4 className={`${styles.tituloSeccion}`} onClick={handleDoubleClick}>Especialmente para ti</h4>
          </div>
          <div className={`container-fluid d-flex ${styles.mostrarT}`}>
            <p>Mostrar todos</p>
          </div>
        </header>


        <section className={`container-fluid d-flex flex-row ${styles.row}`}>
            <Song
              name={'Quedate'}
              autor={'Quevedo'}
              changeSongName={props.changeSongName}
            />
            <Song
              name={'Quedate'}
              autor={'Quevedo'}
              changeSongName={props.changeSongName}
            />
            <Song
              name={'Quedate'}
              autor={'Quevedo'}
              changeSongName={props.changeSongName}
            />
            <Song
              name={'Quedate'}
              autor={'Quevedo'}
              changeSongName={props.changeSongName}
            />
            <Song
              name={'Quedate'}
              autor={'Quevedo'}
              changeSongName={props.changeSongName}
            />
        </section>

      </div>


        <div
          className={`container-fluid d-flex flex-column ${styles.columnOfListas}`}
        >
          <header
            className={`container-fluid d-flex flex-row ${styles.columnHead}`}
          >
            <div className={`container-fluid d-flex ${styles.columnTitle}`}>
              <h4 className={`${styles.tituloSeccion}`} onClick={handleDoubleClick}>Escuchado recientemente</h4>
            </div>
            <div className={`container-fluid d-flex ${styles.mostrarT}`}>
              <p>Mostrar todos</p>
            </div>
          </header>

          <section className={`container-fluid d-flex flex-row ${styles.row}`}>
            <Song
              name={'Quedate'}
              autor={'Quevedo'}
              changeSongName={props.changeSongName}
            />
            <Song
              name={'Quedate'}
              autor={'Quevedo'}
              changeSongName={props.changeSongName}
            />
            <Song
              name={'Quedate'}
              autor={'Quevedo'}
              changeSongName={props.changeSongName}
            />
            <Song
              name={'Quedate'}
              autor={'Quevedo'}
              changeSongName={props.changeSongName}
            />

          </section>
        </div>
    </div>
  );
}
