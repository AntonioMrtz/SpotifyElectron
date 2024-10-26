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
import { t } from 'i18next';
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
        title: t('registerMenu.cant-register-missing-fields-title'),
        description: t('registerMenu.cant-register-missing-fields-description'),
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
        title: t('registerMenu.cant-register-password-dont-match-title'),
        description: t(
          'registerMenu.cant-register-password-dont-match-description',
        ),
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
        title: t('registerMenu.register-success-title'),
        description: t('registerMenu.register-success-description'),
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
        title = t('commonPopover.cold-start-title');
        description = t('commonPopover.cold-start-description');
      } else {
        title = t('registerMenu.cant-register-title');
        description = t('cant-register-description');
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

        <h1>{t('registerMenu.form-register-title')}</h1>
        <form className={`d-flex flex-column ${styles.formWrapper} w-100`}>
          <label
            htmlFor="username"
            className="d-flex flex-column justify-content-start"
          >
            {t('registerMenu.form-username')}
            <input
              type="text"
              name="name"
              id="name"
              placeholder={t('registerMenu.form-username')}
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
            {t('registerMenu.form-thumbnail')}
            <input
              type="text"
              name="photo"
              id="photo"
              placeholder={t('registerMenu.form-thumbnail')}
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
              {t('registerMenu.form-password')}
              <input
                type="password"
                name="password"
                id="password"
                placeholder={t('registerMenu.form-password')}
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
              {t('registerMenu.form-password-repeat')}
              <input
                type="password"
                name="confirmpassword"
                id="confirmpassword"
                placeholder={t('registerMenu.form-password-repeat')}
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
            {t('registerMenu.form-register-button')}{' '}
            {loading && <LoadingCircleSmall />}
          </button>
        </form>

        <hr style={{ marginTop: '32px' }} />

        <div
          className={`d-flex w-100 justify-content-center ${styles.wrapperRegisterText}`}
        >
          <p style={{ color: 'var(--secondary-white)', marginRight: '8px' }}>
            {t('registerMenu.already-have-account')}
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
            {t('registerMenu.go-to-login-button')}
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
