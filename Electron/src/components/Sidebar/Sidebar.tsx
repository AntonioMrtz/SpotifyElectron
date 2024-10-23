import { useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { getTokenUsername } from 'utils/token';
import LoadingCircle from 'components/AdvancedUIComponents/LoadingCircle/LoadingCircle';
import styles from './sideBarCss.module.css';
import PlaylistSidebar from './Playlist/PlaylistSidebar';
import ModalAddSongPlaylist from './ModalAddSongPlaylist/ModalAddSongPlaylist';
import useFetchGetUserRelevantPlaylists from '../../hooks/useFetchGetUserRelevantPlaylists';
import { useSidebar } from './SidebarContext'; // Import the useSidebar hook

export default function Sidebar() {
  const [selectedID, setSelectedID] = useState<string>(''); // Track selected menu item
  const [selectedPlaylist, setSelectedPlaylist] = useState<string>(''); // Track selected playlist
  const { refreshSidebarData } = useSidebar(); // Get the refreshSidebarData from context
  const location = useLocation(); // Access the current location

  // Handling the selected class for menu items
  const getSelectedClass = (id: string) =>
    selectedID === id ? styles.linksubtleClicked : '';

  // Update selectedID based on URL
  useEffect(() => {
    if (location.pathname === '/') {
      setSelectedID('li-inicio');
    } else if (location.pathname.includes('/explorar')) {
      setSelectedID('li-buscar');
    } else {
      setSelectedID('');
    }
  }, [location]);

  //* MENU HOVER STATE HANDLERS
  const [isHoveredInicio, setIsHoveredInicio] = useState(false);
  const [isHoveredBuscar, setIsHoveredBuscar] = useState(false);

  const handleMouseOverInicio = () => setIsHoveredInicio(true);
  const handleMouseOutInicio = () => setIsHoveredInicio(false);
  const handleMouseOverBuscar = () => setIsHoveredBuscar(true);
  const handleMouseOutBuscar = () => setIsHoveredBuscar(false);

  // Playlist click handlers
  const handleUrlInicioClicked = () => setSelectedPlaylist('');
  const handleUrlBuscarClicked = () => setSelectedPlaylist('');
  const handleUrlPlaylistClicked = (name: string) => setSelectedPlaylist(name);

  // Get the user's relevant playlists using the custom hook
  const userName = getTokenUsername();
  const { playlists, loading } = useFetchGetUserRelevantPlaylists(
    userName,
    false,
  );

  return (
    <div className={`container-fluid ${styles.wrapperNavbar}`}>
      <header className={styles.header}>
        <ul className={styles.ulNavigation}>
          <li>
            <Link to="/">
              <button
                type="button"
                onFocus={handleMouseOverInicio}
                onBlur={handleMouseOutInicio}
                className={`${styles.headerLi} ${isHoveredInicio ? styles.linksubtle : ''} ${getSelectedClass('li-inicio')}`}
                onMouseOver={handleMouseOverInicio}
                onMouseOut={handleMouseOutInicio}
                onClick={handleUrlInicioClicked}
                id="li-inicio"
              >
                <i className={`fa-solid fa-house fa-fw ${styles.headerI}`} />
                <span className={styles.headerI}>Inicio</span>
              </button>
            </Link>
          </li>
          <li>
            <Link to="/explorar" className={styles.aHeader}>
              <button
                type="button"
                onFocus={handleMouseOverBuscar}
                onBlur={handleMouseOutBuscar}
                className={`${styles.headerLi} ${isHoveredBuscar ? styles.linksubtle : ''} ${getSelectedClass('li-buscar')}`}
                onMouseOver={handleMouseOverBuscar}
                onMouseOut={handleMouseOutBuscar}
                onClick={handleUrlBuscarClicked}
                id="li-buscar"
              >
                <i
                  className={`fa-solid fa-magnifying-glass fa-fw ${styles.headerI}`}
                />
                <span className={styles.headerI}>Buscar</span>
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
                Tu biblioteca
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
            {loading && <LoadingCircle />}{' '}
            {/* Show loading spinner while loading */}
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
