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
import LoadingCircleSmall from 'components/AdvancedUIComponents/LoadingCircle/LoadingCircleSmall';
import FormControl from '@mui/material/FormControl';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import Language from 'i18n/languages';
import { changeLanguage } from 'i18n/i18n';
import { t } from 'i18next';
import { getLanguageFromStorage, setLanguageStorage } from 'utils/language';
import { LoginService } from '../../swagger/api/services/LoginService';
import SpotifyElectronLogo from '../../assets/imgs/SpotifyElectronLogo.png';
import styles from './startMenu.module.css';
import englishFlag from '../../assets/flags/en_flag.svg';
import spanishFlag from '../../assets/flags/es_flag.svg';

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
  const [propsPopOver, setPropsPopOver] = useState<PropsInfoPopover | null>(
    null,
  );

  /* Loading state for auto-login */
  const [autoLoginLoading, setAutoLoginLoading] = useState(false);
  const [loginLoading, setLoginLoading] = useState(false);

  /* Form data */
  const [formData, setFormData] = useState({
    name: '',
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
      if (!formData.name || !formData.password) {
        throw new Error('Unable to login');
      }
      // eslint-disable-next-line camelcase
      const loginData: Body_login_user_login__post = {
        username: formData.name,
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
        title = t('commonPopover.cold-start-title');
        description = t('commonPopover.cold-start-description');
      } else {
        title = t('startMenu.cant-login-title');
        description = t('startMenu.cant-login-description');
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
            title: t('commonPopover.cold-start-title'),
            description: t('commonPopover.cold-start-description'),
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

  const [language, setLanguage] = useState<Language>(Language.ENGLISH);

  const loadLanguage = (lang: Language) => {
    setLanguage(lang);
    changeLanguage(lang);
    setLanguageStorage(lang);
  };

  const handleUserLanguageChange = (event: SelectChangeEvent<Language>) => {
    const languageInput = event.target.value as Language;
    loadLanguage(languageInput);
  };

  useEffect(() => {
    loadLanguage(getLanguageFromStorage());
  }, []);

  return (
    <div className={`${styles.mainModalContainer}`}>
      {!autoLoginLoading && (
        <div className={`${styles.languageContainer}`}>
          <FormControl
            sx={{
              m: 1,
              '& .Mui-focused .MuiOutlinedInput-notchedOutline': {
                borderColor: 'var(--app-logo-color) !important',
              },
            }}
          >
            <Select
              labelId="language-select-label"
              id="language-select"
              value={language}
              onChange={handleUserLanguageChange}
              inputProps={{
                // need `data-testid` as prop for tests
                'aria-label': 'Without label',
                'data-testid': 'language-select',
              }}
              sx={{
                color: 'var(--secondary-white)',
                backgroundColor: 'transparent',
                '&:hover .MuiOutlinedInput-notchedOutline': {
                  borderColor: 'var(--app-logo-color) !important',
                },
              }}
              MenuProps={{
                PaperProps: {
                  sx: {
                    backgroundColor: 'rgba(42, 42, 42, 0.5)',
                  },
                },
              }}
            >
              <MenuItem
                value={Language.ENGLISH}
                sx={{
                  display: 'flex',
                  justifyContent: 'center',
                  backgroundColor: 'transparent',
                  '&:hover': {
                    backgroundColor: 'rgba(42, 42, 42, 0.7)',
                  },
                }}
              >
                <img
                  src={englishFlag}
                  alt="english flag"
                  style={{ width: '32px' }}
                />
              </MenuItem>

              <MenuItem
                value={Language.SPANISH}
                sx={{
                  display: 'flex',
                  justifyContent: 'center',
                  backgroundColor: 'transparent',
                  '&:hover': {
                    backgroundColor: 'rgba(42, 42, 42, 0.7)',
                  },
                }}
              >
                <img
                  src={spanishFlag}
                  alt="spanish flag"
                  style={{ width: '32px' }}
                />
              </MenuItem>
            </Select>
          </FormControl>
        </div>
      )}
      {autoLoginLoading && <LoadingCircle />}
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

          <h1>{t('startMenu.form-login-title')}</h1>
          <form className={`d-flex flex-column ${styles.formWrapper}`}>
            <label
              htmlFor="username"
              className="d-flex flex-column justify-content-start"
            >
              {t('startMenu.form-username')}
              <input
                type="text"
                name="name"
                id="name"
                placeholder={t('startMenu.form-username')}
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
              {t('startMenu.form-password')}
              <input
                type="password"
                name="password"
                id="password"
                placeholder={t('startMenu.form-password')}
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
              {t('startMenu.form-login-button')}
              {loginLoading && <LoadingCircleSmall />}
            </button>
          </form>

          <hr style={{ marginTop: '32px' }} />

          <div
            className={`d-flex w-100 justify-content-center ${styles.wrapperRegisterText}`}
          >
            <p style={{ color: 'var(--secondary-white)', marginRight: '8px' }}>
              {t('startMenu.no-account')}
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
              {t('startMenu.go-to-register-button')}
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
