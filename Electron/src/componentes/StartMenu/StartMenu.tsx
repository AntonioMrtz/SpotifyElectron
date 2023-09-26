import styles from './startMenu.module.css';
import SpotifyElectronLogo from '../../assets/imgs/SpotifyElectronLogo.png';

export default function StartMenu() {
  return (
    <div className={`${styles.mainModalContainer}`}>
      <div className={`${styles.contentWrapper}`}>
        <div className={`d-flex flex-row ${styles.titleContainer}`}>
          <img
            src={SpotifyElectronLogo}
            className="img-fluid"
            alt="Spotify Electron Logo"
          />
          <h2>Spotify Electron</h2>
        </div>

        <hr />

        <h1>Inicia sesión en Spotify Electron</h1>
        <div className={`d-flex flex-column ${styles.formWrapper}`}>
          <label
            htmlFor="username"
            className="d-flex flex-column justify-content-start"
            placeholder="Nombre de usuario"
          >
            Nombre de usuario
            <input type="text" />
          </label>
          <label
            htmlFor="password"
            className="d-flex flex-column justify-content-start"
            placeholder="Contraseña"
          >
            Contraseña
            <input type="text" />
          </label>

          <button type="button" className={`${styles.loginButton}`}>
            Iniciar sesión
          </button>
        </div>

        <hr style={{ marginTop: '32px' }} />

        <div
          className={`d-flex w-100 justify-content-center ${styles.wrapperRegisterText}`}
        >
          <p>¿No tienes cuenta?</p>
          <p style={{}}>Registrate en Spotify</p>
        </div>
      </div>
    </div>
  );
}
