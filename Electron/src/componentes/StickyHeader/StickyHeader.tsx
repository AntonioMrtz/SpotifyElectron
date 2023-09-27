import { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Global from 'global/global';
import styles from './stickyHeader.module.css';
import groupIcon from '../../assets/imgs/groupIcon.png';
import defaultThumbnailPlaylist from '../../assets/imgs/DefaultThumbnailPlaylist.jpg';

export default function StickyHeader() {
  const navigate = useNavigate();

  const [profileIcon, setProfileIcon] = useState(defaultThumbnailPlaylist);

  const handleThumbnail = async () => {
    const resFetchWhoAmIUser = await fetch(
      `${Global.backendBaseUrl}usuarios/whoami`,
      {
        headers: { Authorization: Global.getToken() },
      }
    );

    const resFetchWhoAmIJson = await resFetchWhoAmIUser.json();

    const resFetchUser = await fetch(
      `${Global.backendBaseUrl}usuarios/${resFetchWhoAmIJson.username}`,
      {
        headers: { Authorization: Global.getToken() },
      }
    );

    const resFetchUserJson = await resFetchUser.json();

    if (resFetchUserJson && resFetchUserJson.photo) {
      setProfileIcon(
        resFetchUserJson.photo === ''
          ? defaultThumbnailPlaylist
          : resFetchUserJson.photo
      );
    }
  };

  const handleProfileButon = async () => {
    const resFetchWhoAmIUser = await fetch(
      `${Global.backendBaseUrl}usuarios/whoami`,
      {
        headers: { Authorization: Global.getToken() },
      }
    );

    const resFetchWhoAmIJson = await resFetchWhoAmIUser.json();

    navigate(`/user/${resFetchWhoAmIJson.username}`);
  };

  const [visibleBackground, setVisibleBackground] = useState({});

  const handleScroll = () => {
    if (window.scrollY > 200) {
      setVisibleBackground({
        backgroundColor: 'var(--sticky-header-blue)',
        marginTop: '0',
      });
    } else if (window.scrollY > 150) {
      setVisibleBackground({
        backgroundColor: 'var(--sticky-header-blue)',
        marginTop: '0',
        opacity: '0.7',
      });
    } else if (window.scrollY > 100) {
      setVisibleBackground({
        backgroundColor: 'var(--sticky-header-blue)',
        marginTop: '0',
        opacity: '0.5',
      });
    } else {
      setVisibleBackground({});
    }
  };

  useEffect(() => {
    handleThumbnail();
    window.addEventListener('scroll', handleScroll);
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  const handleGoingBackArrows = () => {
    window.electron.loadPreviousUrl.sendMessage('load-previous-url');
  };

  const handleGoingForwardArrows = () => {
    window.electron.loadForwardUrl.sendMessage('load-forward-url');
  };

  const location = useLocation();

  const [arrowState, setArrowState] = useState<Global.HandleUrlChangeResponse>({
    canGoBack: false,
    canGoForward: false,
  });

  const handleUrlChange = async () => {
    try {
      const response = await window.electron.handleUrlChange.sendMessage(
        'handle-url-change'
      );
      const responseObj: Global.HandleUrlChangeResponse = {
        canGoBack: response.canGoBack,
        canGoForward: response.canGoForward,
      };
      setArrowState(responseObj);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  useEffect(() => {
    handleUrlChange();
  }, [location]);

  const [backArrowStyle, setBackArrowStyle] = useState('');
  const [forwardArrowStyle, setForwardArrowStyle] = useState('');

  useEffect(() => {
    setBackArrowStyle(!arrowState.canGoBack ? styles.arrowOpacity : '');
    setForwardArrowStyle(!arrowState.canGoForward ? styles.arrowOpacity : '');
  }, [arrowState]);

  return (
    <header
      style={visibleBackground}
      className={`d-flex flex-row justify-content-space-evenly ${styles.wrapperStickyHeader}`}
    >
      <div
        className={`d-flex flex-row container-fluid ${styles.wrapperDirectionArrows}`}
      >
        <button type="button" onClick={handleGoingBackArrows}>
          <i className={`fa-solid fa-chevron-left ${backArrowStyle}`} />
        </button>
        <button type="button" onClick={handleGoingForwardArrows}>
          <i className={`fa-solid fa-chevron-right ${forwardArrowStyle}`} />
        </button>
      </div>

      <div
        className={`d-flex flex-row container-fluid  ${styles.wrapperProfileOptions}`}
      >
        <button type="button" onClick={handleProfileButon}>
          <img src={profileIcon} alt="" />
        </button>

        <button type="button">
          <img className={`${styles.groupIcon}`} src={groupIcon} alt="" />
        </button>
      </div>
    </header>
  );
}
