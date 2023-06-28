import { useEffect, useState } from 'react';
import styles from './sideBarCss.module.css';
import Playlist from './Playlist/Playlist';

export default function Sidebar() {
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

  /*  HIGHLIGHT CURRENT SECTION LI */

  const [selectedID, setSelectedID] = useState<string>(); // you could set a default id as well

  const getSelectedClass = (id: string) =>
    selectedID === id ? styles.linksubtleClicked : '';

  const [url, setUrl] = useState('');

  useEffect(() => {
    if (url === '') {
      setSelectedID('li-inicio');
    } else if (url === 'explorar') {
      setSelectedID('li-buscar');
    }
  }, [url]);

  // handle Button Clicked by looking at the Current Url
  useEffect(() => {
    const url = window.location.href;

    let splitBySlash = url.split('/');

    setUrl(splitBySlash[splitBySlash.length - 1]);
  }, []);

  /* Handle add playlist button */

  const handleAddPlaylist = () => {};

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
            id="li-inicio"
          >
            <a href="/">
              <i className={`fa-solid fa-house fa-fw ${styles.headerI}`}></i>
              <span className={`${styles.headerI}`}>Inicio</span>
            </a>
          </li>
          <li
            className={`${styles.headerLi} ${listItemBuscar} ${getSelectedClass(
              'li-buscar'
            )}`}
            onMouseOver={handleMouseOverBuscar}
            onMouseOut={handleMouseOutBuscar}
            id="li-buscar"
          >
            <a className={`${styles.aHeader}`} href="explorar">
              <i
                className={`fa-solid fa-magnifying-glass fa-fw ${styles.headerI}`}
              ></i>
              <span className={`${styles.headerI}`}>Buscar</span>
            </a>
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
              <button className={`btn`} onClick={handleAddPlaylist}>
                <i className="fa-solid fa-plus fa-fw"></i>
              </button>
            </div>
          </header>
          <ul
            className={`container-fluid d-flex flex-column ${styles.ulPlaylist}`}
          >
            <Playlist />
            <Playlist />
            <Playlist />
            <Playlist />
            <Playlist />
            <Playlist />
            <Playlist />
            <Playlist />
            <Playlist />
            <Playlist />
            <Playlist />
            <Playlist />
            <Playlist />
            <Playlist />
            <Playlist />
            <Playlist />
            <Playlist />
            <Playlist />
            <Playlist />
            <Playlist />
          </ul>
        </div>
      </div>
    </div>
  );
}
