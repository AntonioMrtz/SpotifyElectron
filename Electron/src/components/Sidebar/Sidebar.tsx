import { useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import Token from 'utils/token';
import LoadingCircle from 'components/AdvancedUIComponents/LoadingCircle/LoadingCircle';
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
      setSelectedID('li-inicio');
    } else if (location.pathname.includes('/explorar')) {
      setSelectedID('li-buscar');
    } else {
      setSelectedID('');
    }
  }, [location]);

  //* MENU HOVER

  const [listItemInicio, setHoverInicio] = useState('');
  const [listItemBuscar, setHoverBuscar] = useState('');

  const [isHoveredInicio, setIsHoveredInicio] = useState(false);
  const [isHoveredBuscar, setIsHoveredBuscar] = useState(false);

  const handleMouseOverInicio = () => {
    setIsHoveredInicio(true);
  };

  const handleMouseOutInicio = () => {
    setIsHoveredInicio(false);
  };

  const handleMouseOverBuscar = () => {
    setIsHoveredBuscar(true);
  };

  const handleMouseOutBuscar = () => {
    setIsHoveredBuscar(false);
  };

  useEffect(() => {
    setHoverInicio(isHoveredInicio ? styles.linksubtle : '');
    setHoverBuscar(isHoveredBuscar ? styles.linksubtle : '');
  }, [isHoveredBuscar, isHoveredInicio]);

  const handleUrlInicioClicked = () => {
    setSelectedPlaylist('');
  };

  const handleUrlBuscarClicked = () => {
    setSelectedPlaylist('');
  };

  const handleUrlPlaylistClicked = (name: string) => {
    setSelectedPlaylist(name); // Actualizar el estado cuando se hace clic en una playlist
  };

  const userName = Token.getTokenUsername();

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
                onFocus={handleMouseOverInicio}
                onBlur={handleMouseOutInicio}
                className={`${
                  styles.headerLi
                } ${listItemInicio} ${getSelectedClass('li-inicio')} `}
                onMouseOver={handleMouseOverInicio}
                onMouseOut={handleMouseOutInicio}
                onClick={handleUrlInicioClicked}
                id="li-inicio"
              >
                <i className={`fa-solid fa-house fa-fw ${styles.headerI}`} />
                <span className={`${styles.headerI}`}>Inicio</span>
              </button>
            </Link>
          </li>
          <li>
            <Link to="/explorar" className={`${styles.aHeader}`}>
              <button
                type="button"
                onFocus={handleMouseOverBuscar}
                onBlur={handleMouseOutBuscar}
                className={`${
                  styles.headerLi
                } ${listItemBuscar} ${getSelectedClass('li-buscar')}`}
                onMouseOver={handleMouseOverBuscar}
                onMouseOut={handleMouseOutBuscar}
                onClick={handleUrlBuscarClicked}
                id="li-buscar"
              >
                <i
                  className={`fa-solid fa-magnifying-glass fa-fw ${styles.headerI}`}
                />
                <span className={`${styles.headerI}`}>Buscar</span>
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
