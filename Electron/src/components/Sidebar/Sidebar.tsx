import { useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { getTokenUsername } from 'utils/token';
import LoadingCircle from 'components/AdvancedUIComponents/LoadingCircle/LoadingCircle';
import { t } from 'i18next';
import styles from './sideBarCss.module.css';
import PlaylistSidebar from './Playlist/PlaylistSidebar';
import ModalAddSongPlaylist from './ModalAddSongPlaylist/ModalAddSongPlaylist';
import useFetchGetUserRelevantPlaylists from '../../hooks/useFetchGetUserRelevantPlaylists';

interface PropsSidebar {
  refreshSidebarTriggerValue: boolean;
  refreshSidebarData: () => void;
}

//* HIGHLIGHT CURRENT SECTION LI
export default function Sidebar({
  refreshSidebarTriggerValue,
  refreshSidebarData,
}: PropsSidebar) {
  const [selectedID, setSelectedID] = useState<string>();
  const [selectedPlaylist, setSelectedPlaylist] = useState<string>('');

  const getSelectedClass = (id: string) =>
    selectedID === id ? styles.linksubtleClicked : '';

  const location = useLocation();

  useEffect(() => {
    if (location.pathname === '/') {
      setSelectedID('li-home');
    } else if (location.pathname.includes('/browse')) {
      setSelectedID('li-browse');
    } else {
      setSelectedID('');
    }
  }, [location]);

  //* MENU HOVER

  const [listItemHome, setHoverHome] = useState('');
  const [listItemBrowse, setHoverBrowse] = useState('');

  const [isHoveredHome, setIsHoveredHome] = useState(false);
  const [isHoveredBrowse, setIsHoveredBrowse] = useState(false);

  const handleMouseOverHome = () => {
    setIsHoveredHome(true);
  };

  const handleMouseOutHome = () => {
    setIsHoveredHome(false);
  };

  const handleMouseOverBrowse = () => {
    setIsHoveredBrowse(true);
  };

  const handleMouseOutBrowse = () => {
    setIsHoveredBrowse(false);
  };

  useEffect(() => {
    setHoverHome(isHoveredHome ? styles.linksubtle : '');
    setHoverBrowse(isHoveredBrowse ? styles.linksubtle : '');
  }, [isHoveredBrowse, isHoveredHome]);

  const handleUrlHomeClicked = () => {
    setSelectedPlaylist('');
  };

  const handleUrlOnBrowseClicked = () => {
    setSelectedPlaylist('');
  };

  const handleUrlPlaylistClicked = (name: string) => {
    setSelectedPlaylist(name); // Actualizar el estado cuando se hace clic en una playlist
  };

  const userName = getTokenUsername();

  const { playlists, loading } = useFetchGetUserRelevantPlaylists(
    userName,
    refreshSidebarTriggerValue,
  );

  return (
    <div className={`container-fluid ${styles.wrapperNavbar}`}>
      <header className={`${styles.header}`}>
        <ul className={`${styles.ulNavigation}`}>
          <li>
            <Link to="/">
              <button
                type="button"
                onFocus={handleMouseOverHome}
                onBlur={handleMouseOutHome}
                className={`${
                  styles.headerLi
                } ${listItemHome} ${getSelectedClass('li-home')} `}
                onMouseOver={handleMouseOverHome}
                onMouseOut={handleMouseOutHome}
                onClick={handleUrlHomeClicked}
                id="li-home"
              >
                <i className={`fa-solid fa-house fa-fw ${styles.headerI}`} />
                <span className={`${styles.headerI}`}>{t('sidebar.home')}</span>
              </button>
            </Link>
          </li>
          <li>
            <Link to="/browse" className={`${styles.aHeader}`}>
              <button
                type="button"
                onFocus={handleMouseOverBrowse}
                onBlur={handleMouseOutBrowse}
                className={`${
                  styles.headerLi
                } ${listItemBrowse} ${getSelectedClass('li-browse')}`}
                onMouseOver={handleMouseOverBrowse}
                onMouseOut={handleMouseOutBrowse}
                onClick={handleUrlOnBrowseClicked}
                id="li-browse"
              >
                <i
                  className={`fa-solid fa-magnifying-glass fa-fw ${styles.headerI}`}
                />
                <span className={`${styles.headerI}`}>
                  {t('sidebar.browse')}
                </span>
              </button>
            </Link>
          </li>
        </ul>
      </header>

      <div
        className={`container-fluid d-flex flex-column ${styles.libraryWrapper}`}
      >
        <div
          className={`container-fluid d-flex flex-column p-0 ${styles.playlistUlWrapper}`}
        >
          <header
            className={`container-fluid d-flex flex-row pb-4 ${styles.headerTuBiblioteca}`}
          >
            <div className="container-fluid d-flex justify-content-start p-0">
              <div className="container-fluid ps-0">
                <i className="fa-solid fa-swatchbook fa-fw" />
                {t('sidebar.your-library')}
              </div>
            </div>

            <div
              className="container-fluid d-flex justify-content-end p-0"
              style={{ width: '25%' }}
            >
              <ModalAddSongPlaylist refreshSidebarData={refreshSidebarData} />
            </div>
          </header>
          <ul
            className={`container-fluid d-flex flex-column ${styles.ulPlaylist}`}
          >
            {loading && <LoadingCircle />}

            {!loading &&
              playlists &&
              playlists.map((playlist) => {
                const urlPlaylist = `/playlist/${playlist.name}`;

                const playlistStyle =
                  playlist.name === selectedPlaylist
                    ? styles.selectedPlaylist
                    : '';

                return (
                  <Link to={urlPlaylist} key={playlist.name}>
                    <PlaylistSidebar
                      handleUrlPlaylistClicked={handleUrlPlaylistClicked}
                      name={playlist.name}
                      photo={playlist.photo}
                      owner={playlist.owner}
                      playlistStyle={playlistStyle}
                      refreshSidebarData={refreshSidebarData}
                    />
                  </Link>
                );
              })}
          </ul>
        </div>
      </div>
    </div>
  );
}
