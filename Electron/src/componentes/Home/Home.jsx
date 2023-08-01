import styles from './homeCss.module.css'
import foto from '../../assets/imgs/quedate.jpg'

export default function Home (props) {
  const handleDoubleClick = () => {
    props.changeSongName('p3')
  }

  const handleDoubleClickBeta = () => {
    props.changeSongName('loquillo')
  }

  const handleDoubleClickP3 = () => {
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
            <h4>Titulo</h4>
          </div>
          <div className={`container-fluid d-flex ${styles.mostrarT}`}>
            <p>Mostrar todos</p>
          </div>
        </header>

        <section className={`container-fluid d-flex flex-row ${styles.row}`}>
          <span onClick={handleDoubleClick} className={`rounded ${styles.card}`}>
            <img src={foto} className='card-img-top rounded' />
            <div className={`${styles.card_body}`}>
              <h5 className={`${styles.tituloLista}`}>Quedate</h5>
              <p className={`${styles.autorLista}`}>Quevedo</p>
            </div>
          </span>
          <span onClick={handleDoubleClickBeta} className={`rounded ${styles.card}`}>
            <img src={foto} className='card-img-top rounded' />
            <div className={`${styles.card_body}`}>
              <h5 className={`${styles.tituloLista}`}>Quedate</h5>
              <p className={`${styles.autorLista}`}>Quevedo</p>
            </div>
          </span>
          <span onClick={handleDoubleClickP3} className={`rounded ${styles.card}`}>
            <img src={foto} className='card-img-top rounded' />
            <div className={`${styles.card_body}`}>
              <h5 className={`${styles.tituloLista}`}>Quedate</h5>
              <p className={`${styles.autorLista}`}>Quevedo</p>
            </div>
          </span>
        </section>
      </div>

      <div
        className={`container-fluid d-flex flex-column ${styles.columnOfListas}`}
      >
        <div
          className={`container-fluid d-flex flex-column ${styles.columnOfListas}`}
        >
          <header
            className={`container-fluid d-flex flex-row ${styles.columnHead}`}
          >
            <div className={`container-fluid d-flex ${styles.columnTitle}`}>
              <h4>Titulo</h4>
            </div>
            <div className={`container-fluid d-flex ${styles.mostrarT}`}>
              <p>Mostrar todos</p>
            </div>
          </header>

          <section className={`container-fluid d-flex flex-row ${styles.row}`}>
            <a href='#' className={`rounded ${styles.card}`}>
              <img src={foto} className='card-img-top rounded' />
              <div className={`${styles.card_body}`}>
                <h5 className={`${styles.tituloLista}`}>Quedate</h5>
                <p className={`${styles.autorLista}`}>Quevedo</p>
              </div>
            </a>{' '}
            <a href='#' className={`rounded ${styles.card}`}>
              <img src={foto} className='card-img-top rounded' />
              <div className={`${styles.card_body}`}>
                <h5 className={`${styles.tituloLista}`}>Quedate</h5>
                <p className={`${styles.autorLista}`}>Quevedo</p>
              </div>
            </a>{' '}
            <a href='#' className={`rounded ${styles.card}`}>
              <img src={foto} className='card-img-top rounded' />
              <div className={`${styles.card_body}`}>
                <h5 className={`${styles.tituloLista}`}>Quedate</h5>
                <p className={`${styles.autorLista}`}>Quevedo</p>
              </div>
            </a>{' '}
            <a href='#' className={`rounded ${styles.card}`}>
              <img src={foto} className='card-img-top rounded' />
              <div className={`${styles.card_body}`}>
                <h5 className={`${styles.tituloLista}`}>Quedate</h5>
                <p className={`${styles.autorLista}`}>Quevedo</p>
              </div>
            </a>{' '}
            <a href='#' className={`rounded ${styles.card}`}>
              <img src={foto} className='card-img-top rounded' />
              <div className={`${styles.card_body}`}>
                <h5 className={`${styles.tituloLista}`}>Quedate</h5>
                <p className={`${styles.autorLista}`}>Quevedo</p>
              </div>
            </a>{' '}
            <a href='#' className={`rounded ${styles.card}`}>
              <img src={foto} className='card-img-top rounded' />
              <div className={`${styles.card_body}`}>
                <h5 className={`${styles.tituloLista}`}>Quedate</h5>
                <p className={`${styles.autorLista}`}>Quevedo</p>
              </div>
            </a>{' '}
          </section>
        </div>
      </div>

      <div
        className={`container-fluid d-flex flex-column ${styles.columnOfListas}`}
      >
        <header
          className={`container-fluid d-flex flex-row ${styles.columnHead}`}
        >
          <div className={`container-fluid d-flex ${styles.columnTitle}`}>
            <h4>Titulo</h4>
          </div>
          <div className={`container-fluid d-flex ${styles.mostrarT}`}>
            <p>Mostrar todos</p>
          </div>
        </header>

        <section className={`container-fluid d-flex flex-row ${styles.row}`}>
          <a href='#' className={`rounded ${styles.card}`}>
            <img src={foto} className='card-img-top rounded' />
            <div className={`${styles.card_body}`}>
              <h5 className={`${styles.tituloLista}`}>Quedate</h5>
              <p className={`${styles.autorLista}`}>Quevedo</p>
            </div>
          </a>
          <a href='#' className={`rounded ${styles.card}`}>
            <img src={foto} className='card-img-top rounded' />
            <div className={`${styles.card_body}`}>
              <h5 className={`${styles.tituloLista}`}>Quedate</h5>
              <p className={`${styles.autorLista}`}>Quevedo</p>
            </div>
          </a>
        </section>
      </div>
    </div>
  )
}
