import { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Global from 'global/global';
import styles from './stickyHeader.module.css';
import groupIcon from '../../assets/imgs/groupIcon.png';

export default function StickyHeader() {
  const navigate = useNavigate();

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [profileIcon, setProfileIcon] = useState(
    'https://i.scdn.co/image/ab67757000003b82ae8c728abc415a173667ff85'
  );

  // TODO cambiar usuario real

  const handleProfileButon = () => {
    navigate(`/user/${'usuarioprovisionalcambiar'}`);
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
