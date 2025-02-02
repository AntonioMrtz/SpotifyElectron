import { useEffect, useState, MouseEvent } from 'react';
import { useLocation } from 'react-router-dom';
import Global from 'global/global';
import { getTokenUsername } from 'utils/token';
import Popover, { PopoverPosition } from '@mui/material/Popover';
import ContextMenuProfile from 'components/AdvancedUIComponents/ContextMenu/Profile/ContextMenuProfile';
import useFetchGetUser from 'hooks/useFetchGetUser';
import { useNowPlayingContext } from 'hooks/useNowPlayingContext';
import styles from './stickyHeader.module.css';
import groupIcon from '../../assets/imgs/groupIcon.png';
import defaultThumbnailPlaylist from '../../assets/imgs/DefaultThumbnailPlaylist.jpg';

interface PropsStickyHeader {
  handleLogout: Function;
}

export default function StickyHeader({ handleLogout }: PropsStickyHeader) {
  const { changeSongName } = useNowPlayingContext();

  const username = getTokenUsername();
  const { user } = useFetchGetUser(username);
  const [profileIcon, setProfileIcon] = useState(defaultThumbnailPlaylist);

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
    if (user?.photo) {
      setProfileIcon(user.photo === '' ? defaultThumbnailPlaylist : user.photo);
    }
    window.addEventListener('scroll', handleScroll);
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, [user]);

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
      const response =
        await window.electron.handleUrlChange.sendMessage('handle-url-change');
      const responseObj: Global.HandleUrlChangeResponse = {
        canGoBack: response.canGoBack,
        canGoForward: response.canGoForward,
      };
      setArrowState(responseObj);
    } catch (error) {
      console.log('Error handling URL change:', error);
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

  /* Context Menu */

  const [isOpen, setIsOpen] = useState(false);

  const [anchorPosition, setAnchorPosition] = useState<{
    top: number;
    left: number;
  } | null>(null);

  const open = Boolean(anchorPosition);
  const id = open ? 'parent-popover' : undefined;

  const handleOpenContextMenu = (event: MouseEvent<HTMLButtonElement>) => {
    setIsOpen(!isOpen);
    setAnchorPosition({
      top: event.clientY,
      left: event.clientX,
    });
  };

  const handleCloseContextMenu = () => {
    setAnchorPosition(null);
    setIsOpen(false);
  };

  useEffect(() => {
    if (!isOpen) {
      handleCloseContextMenu();
    }
  }, [isOpen]);

  const handleProfileButon = async (e: MouseEvent<HTMLButtonElement>) => {
    handleOpenContextMenu(e);
  };

  const logOut = (args: any) => {
    changeSongName(Global.noSongPlaying);
    handleLogout(args);
  };

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
          <img src={profileIcon} alt="profile-icon" />
        </button>

        <button type="button">
          <img className={`${styles.groupIcon}`} src={groupIcon} alt="" />
        </button>
      </div>

      <div>
        <Popover
          id={id}
          open={open}
          onClose={handleCloseContextMenu}
          anchorReference="anchorPosition"
          anchorPosition={anchorPosition as PopoverPosition}
          anchorOrigin={{
            vertical: 'top',
            horizontal: 'left',
          }}
          transformOrigin={{
            vertical: 'top',
            horizontal: 'left',
          }}
          sx={{
            '& .MuiPaper-root': {
              backgroundColor: 'var(--hover-white)',
            },
            '& . MuiPopover-root': {
              zIndex: '1000',
            },
          }}
        >
          <ContextMenuProfile
            handleLogout={logOut}
            handleClose={handleCloseContextMenu}
          />
        </Popover>
      </div>
    </header>
  );
}
