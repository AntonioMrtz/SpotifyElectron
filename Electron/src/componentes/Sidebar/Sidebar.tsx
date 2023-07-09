import { useEffect, useState } from 'react';
import styles from './sideBarCss.module.css';
import Playlist from './Playlist/Playlist';
import ModalAddSongPlaylist from './ModalAddSongPlaylist/ModalAddSongPlaylist';
import { Link } from 'react-router-dom';
import defaultThumbnailPlaylist from '../../assets/imgs/DefaultThumbnailPlaylist.jpg';
import { PropsPlaylist } from './types/propsPlaylist.module';

export default function Sidebar() {
  //* RELOAD SIDEBAR

  const reloadSideBar = () => {
    /* Force reload by changing reload variable */
    const delay = 500;

    const timer = setTimeout(() => {
      handlePlaylists();
    }, delay);

    return () => clearTimeout(timer);
  };

  //* MENU HOVER

  let [listItemInicio, setHoverInicio] = useState('');
  let [listItemBuscar, setHoverBuscar] = useState('');

  const [isHoveredInicio, setIsHovered] = useState(false);
  const [isHoveredBuscar, setIsHoveredBuscar] = useState(false);

  const handleMouseOverInicio = () => {
    setIsHovered(true);
  };

  const handleMouseOutInicio = () => {
    setIsHovered(false);
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

  //* HIGHLIGHT CURRENT SECTION LI

  const [selectedID, setSelectedID] = useState<string>(); // you could set a default id as well

  const getSelectedClass = (id: string) =>
    selectedID === id ? styles.linksubtleClicked : '';

  const [url, setUrl] = useState('/');

  useEffect(() => {
    //console.log(url)
    if (url === '/') {
      setSelectedID('li-inicio');
    } else if (url === '/explorar') {
      setSelectedID('li-buscar');
    }
  }, [url]);

  const handleUrlInicioClicked = () => {
    setUrl('/');
  };

  const handleUrlBuscarClicked = () => {
    setUrl('/explorar');
  };

  const handleUrlPlaylistClicked = () => {
    setUrl('');
  };

  //* PLAYLISTS

  const [playlists, setPlaylists] = useState<PropsPlaylist[]>();

  const handlePlaylists = () => {
    fetch('http://127.0.0.1:8000/playlists/', {
      headers: { 'Access-Control-Allow-Origin': '*' },
    })
      .then((res) => res.json())
      .then((res) => {
        if (res['playlists']) {
          let propsPlaylists: PropsPlaylist[] = [];

          for (let obj of res['playlists']) {
            obj = JSON.parse(obj);
            let propsPlaylist: PropsPlaylist = {
              name: obj['name'],
              photo:
                obj['photo'] === '' ? defaultThumbnailPlaylist : obj['photo'],
              handleUrlPlaylistClicked: handleUrlPlaylistClicked,
            };

            propsPlaylists.push(propsPlaylist);
          }
          setPlaylists(propsPlaylists);
        }
      })
      .catch((error) => {
        console.log(error);
        console.log('No se pudieron obtener las playlists');
      });
  };

  useEffect(() => {
    handlePlaylists();
  }, []);

  return (
    <div className={`container-fluid ${styles.wrapperNavbar}`}>
      <header className={`${styles.header}`}>
        <ul className={`${styles.ul}`}>
          <li
            className={`${styles.headerLi} ${listItemInicio} ${getSelectedClass(
              'li-inicio'
            )} `}
            onMouseOver={handleMouseOverInicio}
            onMouseOut={handleMouseOutInicio}
            onClick={handleUrlInicioClicked}
            id="li-inicio"
          >
            <Link to="/">
              <i className={`fa-solid fa-house fa-fw ${styles.headerI}`}></i>
              <span className={`${styles.headerI}`}>Inicio</span>
            </Link>
          </li>
          <li
            className={`${styles.headerLi} ${listItemBuscar} ${getSelectedClass(
              'li-buscar'
            )}`}
            onMouseOver={handleMouseOverBuscar}
            onMouseOut={handleMouseOutBuscar}
            onClick={handleUrlBuscarClicked}
            id="li-buscar"
          >
            <Link to="/explorar" className={`${styles.aHeader}`}>
              <i
                className={`fa-solid fa-magnifying-glass fa-fw ${styles.headerI}`}
              ></i>
              <span className={`${styles.headerI}`}>Buscar</span>
            </Link>
          </li>
        </ul>
      </header>

      <div
        className={`container-fluid d-flex flex-column ${styles.libraryWrapper}`}
      >
        <header className={`container-fluid d-flex flex-column`}></header>
        <div
          className={`container-fluid d-flex flex-column p-0 ${styles.playlistUlWrapper}`}
        >
          <header
            className={`container-fluid d-flex flex-row pb-4 ${styles.headerTuBiblioteca}`}
          >
            <div className={`container-fluid d-flex justify-content-start p-0`}>
              <div className={`container-fluid ps-0`}>
                <i className="fa-solid fa-swatchbook fa-fw"></i>Tu biblioteca
              </div>
            </div>

            <div
              className={`container-fluid d-flex justify-content-end p-0`}
              style={{ width: '25%' }}
            >
              <ModalAddSongPlaylist reloadSidebar={reloadSideBar} />
            </div>
          </header>
          <ul
            className={`container-fluid d-flex flex-column ${styles.ulPlaylist}`}
          >
            {playlists &&
              playlists.map((playlist) => {
                let urlPlaylist = '/playlist/' + playlist.name;
                return (
                  <Link to={urlPlaylist} key={playlist.name}>
                    <Playlist
                      handleUrlPlaylistClicked={handleUrlPlaylistClicked}
                      name={playlist.name}
                      photo={playlist.photo}
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
