import { ChangeEvent, useState, MouseEvent } from 'react';
import Global from 'global/global';
import { InfoPopoverType } from 'components/AdvancedUIComponents/InfoPopOver/types/InfoPopover';
import InfoPopover from 'components/AdvancedUIComponents/InfoPopOver/InfoPopover';
import styles from './startMenu.module.css';
import SpotifyElectronLogo from '../../assets/imgs/SpotifyElectronLogo.png';

interface PropsStartMenu {
  setIsLogged: Function;
  setIsSigningUp: Function;
}

export default function StartMenu({
  setIsLogged,
  setIsSigningUp,
}: PropsStartMenu) {
  /* Popover */

  const [isOpenPopover, setisOpenPopover] = useState(false);

  /* Form data */

  const [formData, setFormData] = useState({
    nombre: '',
    password: '',
  });

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleLogin = async (e: MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    try {
      if (!formData.nombre || !formData.password) {
        throw new Error('Unable to login');
      }

      const fetchParameters = new URLSearchParams();
      fetchParameters.append('username', formData.nombre);
      fetchParameters.append('password', formData.password);

      const requestOptions: RequestInit = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },

        body: fetchParameters.toString(),
      };

      const fetchUrlLogin = `${Global.backendBaseUrl}/login/`;
      const resFetchUrlLogin = await fetch(fetchUrlLogin, requestOptions);
      const resFetchUrlLoginJson = await resFetchUrlLogin.json();

      if (resFetchUrlLogin.status !== 200) {
        setIsLogged(false);
        throw new Error('Unable to login');
      } else {
        localStorage.setItem('jwt', resFetchUrlLoginJson);
        setIsLogged(true);
      }
    } catch {
      console.log('Unable to login');
      setisOpenPopover(true);
    }
  };

  const handleClickRegister = () => {
    setIsSigningUp(true);
  };

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
        <form className={`d-flex flex-column ${styles.formWrapper}`}>
          <label
            htmlFor="username"
            className="d-flex flex-column justify-content-start"
          >
            Nombre de usuario
            <input
              type="text"
              name="nombre"
              id="nombre"
              placeholder="Nombre de usuario"
              onChange={handleChange}
              spellCheck={false}
              required
            />
          </label>
          <label
            htmlFor="password"
            className="d-flex flex-column justify-content-start"
          >
            Contraseña
            <input
              type="password"
              name="password"
              id="password"
              placeholder="Contraseña"
              onChange={handleChange}
              spellCheck={false}
              required
            />
          </label>

          <button
            type="submit"
            className={`${styles.loginButton}`}
            onClick={handleLogin}
          >
            Iniciar sesión
          </button>
        </form>

        <hr style={{ marginTop: '32px' }} />

        <div
          className={`d-flex w-100 justify-content-center ${styles.wrapperRegisterText}`}
        >
          <p style={{ color: 'var(--secondary-white)', marginRight: '8px' }}>
            ¿No tienes cuenta?
          </p>
          <button
            onClick={handleClickRegister}
            type="button"
            style={{
              color: 'var(--pure-white)',
              textDecoration: 'underline',
              border: 'none',
              backgroundColor: 'transparent',
              padding: '0px',
            }}
          >
            Regístrate en Spotify Electron
          </button>
        </div>
      </div>

      <InfoPopover
        type={InfoPopoverType.ERROR}
        handleClose={() => {
          setisOpenPopover(false);
        }}
        description="Los credenciales introducidos no son válidos"
        title="No se ha podido iniciar sesión"
        triggerOpenConfirmationModal={isOpenPopover}
      />
    </div>
  );
}
