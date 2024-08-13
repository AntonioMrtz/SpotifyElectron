import { ChangeEvent, useState, MouseEvent } from 'react';
import Global from 'global/global';
import InfoPopover from 'components/AdvancedUIComponents/InfoPopOver/InfoPopover';
import { InfoPopoverType } from 'components/AdvancedUIComponents/InfoPopOver/types/InfoPopover';
import styles from './startMenu.module.css';
import SpotifyElectronLogo from '../../assets/imgs/SpotifyElectronLogo.png';

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

  interface IPropsPopover {
    type: InfoPopoverType;
    handleClose: Function;
    title: string;
    description: string;
  }

  const [isOpenPopover, setisOpenPopover] = useState(false);

  const [propsPopOver, setPropsPopOver] = useState<IPropsPopover | null>(null);

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
        handleClose: () => {
          setisOpenPopover(false);
        },
      });
      return;
    }

    try {
      const fetchPostUserURL = `${Global.backendBaseUrl}/users/?name=${formData.name}&photo=${formData.photo}&password=${formData.password}`;

      const requestOptions: RequestInit = {
        method: 'POST',
      };

      const resfetchPostUser = await fetch(fetchPostUserURL, requestOptions);

      if (resfetchPostUser.status !== 201) {
        const resfetchPostUserJson = await resfetchPostUser.json();
        throw new Error(resfetchPostUserJson.detail);
      } else {
        setisOpenPopover(true);

        setPropsPopOver({
          title: 'Usuario registrado',
          description: 'El usuario ha sido registrado con éxito',
          type: InfoPopoverType.SUCCESS,
          handleClose: () => {
            setisOpenPopover(false);
            setIsSigningUp(false);
          },
        });
      }
    } catch (error) {
      console.log('Unable to login');
      setisOpenPopover(true);

      setPropsPopOver({
        title: (error as Error).message,
        description: '',
        type: InfoPopoverType.ERROR,
        handleClose: () => {
          setisOpenPopover(false);
        },
      });
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
            onClick={handleRegister}
          >
            Registrar
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
