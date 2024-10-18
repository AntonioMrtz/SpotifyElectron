import { ChangeEvent, useState, MouseEvent } from 'react';
import InfoPopover from 'components/AdvancedUIComponents/InfoPopOver/InfoPopover';
import {
  InfoPopoverType,
  PropsInfoPopover,
} from 'components/AdvancedUIComponents/InfoPopOver/types/InfoPopover';
import timeout from 'utils/timeout';
import Global from 'global/global';
import LoadingCircleSmall from 'components/AdvancedUIComponents/LoadingCircle/LoadingCircleSmall';
import { CancelablePromise } from 'swagger/api';
import styles from './startMenu.module.css';
import SpotifyElectronLogo from '../../assets/imgs/SpotifyElectronLogo.png';
import { UsersService } from '../../swagger/api/services/UsersService';

interface PropsRegisterMenu {
  setIsSigningUp: Function;
}

export default function RegisterMenu({ setIsSigningUp }: PropsRegisterMenu) {
  /* Form */

  const [formData, setFormData] = useState({
    name: '',
    password: '',
    confirmpassword: '',
    photo: '',
  });

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  /* PopOver atrributes */

  const [isOpenPopover, setisOpenPopover] = useState(false);

  const [propsPopOver, setPropsPopOver] = useState<PropsInfoPopover | null>(
    null,
  );

  /* Loading state */
  const [loading, setLoading] = useState(false);

  const handleRegister = async (e: MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    if (
      !formData.name ||
      !formData.photo ||
      !formData.password ||
      !formData.confirmpassword
    ) {
      setisOpenPopover(true);

      setPropsPopOver({
        title: 'No se han introducido todos los datos de registro obligatorios',
        description: 'Introduce los datos restantes',
        type: InfoPopoverType.ERROR,
        triggerOpenConfirmationModal: false,
        handleClose: () => {
          setisOpenPopover(false);
        },
      });
      return;
    }

    if (formData.password !== formData.confirmpassword) {
      setisOpenPopover(true);

      setPropsPopOver({
        title: 'Las contraseñas no coinciden',
        description: 'Asegúrese de que las contraseñas son iguales',
        type: InfoPopoverType.ERROR,
        triggerOpenConfirmationModal: false,
        handleClose: () => {
          setisOpenPopover(false);
        },
      });
      return;
    }

    let createUserPromise: CancelablePromise<any> | null = null;
    try {
      setLoading(true);

      createUserPromise = UsersService.createUserUsersPost(
        formData.name,
        formData.photo,
        formData.password,
      );

      await Promise.race([
        createUserPromise,
        timeout(Global.coldStartRequestTimeout),
      ]);

      setisOpenPopover(true);
      setPropsPopOver({
        title: 'Usuario registrado',
        description: 'El usuario ha sido registrado con éxito',
        type: InfoPopoverType.SUCCESS,
        triggerOpenConfirmationModal: false,
        handleClose: () => {
          setisOpenPopover(false);
          setIsSigningUp(false);
        },
      });
    } catch (error: unknown) {
      setLoading(false);
      console.log('Unable to register');

      let title: string;
      let description: string;

      if (error instanceof Error && error.message === 'Timeout') {
        createUserPromise?.cancel();

        title = 'El servidor esta iniciándose';
        description =
          'El servidor esta iniciándose (cold-start), inténtelo de nuevo en 1 minuto';
      } else {
        title = 'Los credenciales introducidos no son válidos';
        description = 'No se ha podido registrar el usuario';
      }

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
    }
  };

  const handleClickLogin = () => {
    setIsSigningUp(false);
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

        <h1>Regístrate en Spotify Electron</h1>
        <form className={`d-flex flex-column ${styles.formWrapper} w-100`}>
          <label
            htmlFor="username"
            className="d-flex flex-column justify-content-start"
          >
            Nombre de usuario
            <input
              type="text"
              name="name"
              id="name"
              placeholder="Nombre de usuario"
              onChange={handleChange}
              disabled={loading}
              spellCheck={false}
              required
            />
          </label>
          <label
            htmlFor="url"
            className="d-flex flex-column justify-content-start"
          >
            Foto de perfil
            <input
              type="text"
              name="photo"
              id="photo"
              placeholder="Foto de perfil"
              onChange={handleChange}
              disabled={loading}
              spellCheck={false}
              required
            />
          </label>

          <div className="d-flex gap-3 w-100">
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
                disabled={loading}
                spellCheck={false}
                required
              />
            </label>

            <label
              htmlFor="password"
              className="d-flex flex-column justify-content-start"
            >
              Confirma tu contraseña
              <input
                type="password"
                name="confirmpassword"
                id="confirmpassword"
                placeholder="Confirma tu contraseña"
                onChange={handleChange}
                disabled={loading}
                spellCheck={false}
                required
              />
            </label>
          </div>

          <button
            type="submit"
            style={{
              backgroundColor: 'var(--app-logo-color)',
            }}
            className={`${styles.registerButton}`}
            disabled={loading}
            onClick={handleRegister}
          >
            Registrar {loading && <LoadingCircleSmall />}
          </button>
        </form>

        <hr style={{ marginTop: '32px' }} />

        <div
          className={`d-flex w-100 justify-content-center ${styles.wrapperRegisterText}`}
        >
          <p style={{ color: 'var(--secondary-white)', marginRight: '8px' }}>
            ¿Ya tienes una cuenta?
          </p>
          <button
            onClick={handleClickLogin}
            disabled={loading}
            type="button"
            style={{
              color: 'var(--pure-white)',
              textDecoration: 'underline',
              border: 'none',
              backgroundColor: 'transparent',
              padding: '0px',
            }}
          >
            Inicia sesión en Spotify Electron
          </button>
        </div>
      </div>

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
