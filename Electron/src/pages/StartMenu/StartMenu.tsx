import { ChangeEvent, useState, MouseEvent, useEffect } from 'react';
import {
  InfoPopoverType,
  PropsInfoPopover,
} from 'components/AdvancedUIComponents/InfoPopOver/types/InfoPopover';
import InfoPopover from 'components/AdvancedUIComponents/InfoPopOver/InfoPopover';
import { getToken } from 'utils/token';
// eslint-disable-next-line camelcase
import { Body_login_user_login__post } from 'swagger/api/models/Body_login_user_login__post';
import timeout from 'utils/timeout';
import LoadingCircle from 'components/AdvancedUIComponents/LoadingCircle/LoadingCircle';
import Global from 'global/global';
import { CancelablePromise } from 'swagger/api';
import styles from './startMenu.module.css';
import SpotifyElectronLogo from '../../assets/imgs/SpotifyElectronLogo.png';
import { LoginService } from '../../swagger/api/services/LoginService';

interface PropsStartMenu {
  setIsLogged: Function;
  setIsSigningUp: Function;
}

const coldStartTimeoutErrorTitle = 'El servidor esta iniciándose';
const coldStartTimeoutErrorDescription =
  'El servidor esta iniciándose (cold-start), inténtelo de nuevo en 1 minuto';

export default function StartMenu({
  setIsLogged,
  setIsSigningUp,
}: PropsStartMenu) {
  /* Popover */
  const [isOpenPopover, setisOpenPopover] = useState(false);
  const [propsPopOver, setPropsPopOver] = useState<PropsInfoPopover | null>(
    null,
  );

  /* Loading state for auto-login */
  const [autoLoginLoading, setAutoLoginLoading] = useState(false);
  const [loginLoading, setLoginLoading] = useState(false);

  /* Form data */
  const [formData, setFormData] = useState({
    nombre: '',
    password: '',
  });

  const showErrorPopover = ({
    title,
    description,
  }: Pick<PropsInfoPopover, 'title' | 'description'>) => {
    setPropsPopOver({
      title,
      description,
      type: InfoPopoverType.ERROR,
      triggerOpenConfirmationModal: false,
      handleClose: () => {
        setisOpenPopover(false);
      },
    });
    setisOpenPopover(true);
  };

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleLogin = async (e: MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();

    let loginUserPromise: CancelablePromise<any> | null = null;
    try {
      setLoginLoading(true);
      if (!formData.nombre || !formData.password) {
        throw new Error('Unable to login');
      }
      // eslint-disable-next-line camelcase
      const loginData: Body_login_user_login__post = {
        username: formData.nombre,
        password: formData.password,
      };

      loginUserPromise = LoginService.loginUserLoginPost(loginData);
      const loginResponse = await Promise.race([
        loginUserPromise,
        timeout(Global.coldStartRequestTimeout),
      ]);
      localStorage.setItem('jwt', loginResponse);
      setIsLogged(true);
    } catch (error: unknown) {
      setIsLogged(false);
      console.log('Unable to login');

      let title: string;
      let description: string;

      if (error instanceof Error && error.message === 'Timeout') {
        loginUserPromise?.cancel();

        title = coldStartTimeoutErrorTitle;
        description = coldStartTimeoutErrorDescription;
      } else {
        title = 'Los credenciales introducidos no son válidos';
        description = 'No se ha podido iniciar sesión';
      }

      showErrorPopover({ title, description });
    } finally {
      setLoginLoading(false);
    }
  };

  const handleClickRegister = () => {
    setIsSigningUp(true);
  };

  useEffect(() => {
    const handleAutoLogin = async () => {
      let autoLoginPromise: CancelablePromise<any> | null = null;
      try {
        setAutoLoginLoading(true);
        const token = getToken();
        if (!token) return;
        autoLoginPromise =
          LoginService.loginUserWithJwtLoginTokenTokenPost(token);
        await Promise.race([
          autoLoginPromise,
          timeout(Global.coldStartRequestTimeout),
        ]);
        setIsLogged(true);
      } catch (error) {
        if (error instanceof Error && error.message === 'Timeout') {
          autoLoginPromise?.cancel();
          showErrorPopover({
            title: coldStartTimeoutErrorTitle,
            description: coldStartTimeoutErrorDescription,
          });
        } else {
          console.log(`User invalid credentials for auto login with JWT token`);
        }
      } finally {
        setAutoLoginLoading(false);
      }
    };
    handleAutoLogin();
  }, [setIsLogged]);

  return (
    <div className={`${styles.mainModalContainer}`}>
      {(autoLoginLoading || loginLoading) && (
        <div className={`${styles.loadingCircleWrapper}`}>
          <LoadingCircle />
        </div>
      )}
      {!autoLoginLoading && (
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
                disabled={loginLoading}
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
                disabled={loginLoading}
                spellCheck={false}
                required
              />
            </label>

            <button
              type="submit"
              className={`${styles.loginButton}`}
              onClick={handleLogin}
              disabled={loginLoading}
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
              disabled={loginLoading}
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
      )}

      {propsPopOver && (
        <InfoPopover
          type={propsPopOver.type}
          handleClose={propsPopOver.handleClose}
          description={propsPopOver.description}
          title={propsPopOver.title}
          triggerOpenConfirmationModal={isOpenPopover}
        />
      )}
    </div>
  );
}
