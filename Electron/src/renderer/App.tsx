import styles from './AppCss.module.css';
import Sidebar from '../componentes/Sidebar/Sidebar';
import Home from '../componentes/Home/Home';
import Explorar from '../componentes/Explorar/Explorar';
import Footer from '../componentes/footer/Footer';
import { Route, Routes, useLocation } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Playlist from 'componentes/Playlist/Playlist';
import StickyHeader from 'componentes/StickyHeader/StickyHeader';

function App() {
  /* Scroll to the top if path is changed */
  const location = useLocation();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [location]);

  /* Handle reload of sidebar */

  const [triggerReloadSidebar, setTriggerReloadSidebar] = useState(false);

  const reloadSidebar = () => {
    setTriggerReloadSidebar((state) => !state);
  };

  /* Handle change song name */

  const [songName, setSongName] = useState('none');
  const changeSongName = (songName: string): void => {
    setSongName(songName);
  };

  return (
    <div className={`App d-flex flex-column ${styles.appBackground}`}>
      <StickyHeader />

      <div className="d-flex">
        <Sidebar triggerReloadSidebar={triggerReloadSidebar} />
        <div
          className={`App d-flex container-fluid ${styles.mainContentWrapper}`}
        >
          <Routes>
            <Route
              path="/playlist/:id"
              element=<Playlist
                changeSongName={changeSongName}
                triggerReloadSidebar={reloadSidebar}
              />
            />
            <Route
              path="/explorar"
              element=<Explorar changeSongName={changeSongName} />
            />
            <Route path="/" element=<Home changeSongName={changeSongName} /> />
            <Route path="*" element=<Home changeSongName={changeSongName} /> />
          </Routes>
        </div>
      </div>
      <Footer songName={songName} />
    </div>
  );
}

export default App;
