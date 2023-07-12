import styles from './AppCss.module.css';
import Sidebar from '../componentes/Sidebar/Sidebar';
import Home from '../componentes/Home/Home';
import Explorar from '../componentes/Explorar/Explorar';
import Footer from '../componentes/footer/Footer';
import { Route, Routes } from 'react-router-dom';
import { useState } from 'react';
import Playlist from 'componentes/Playlist/Playlist';
import StickyHeader from 'componentes/StickyHeader/StickyHeader';

function App() {
  const [songName, setSongName] = useState('none');

  const changeSongName = (songName: string): void => {
    setSongName(songName);
  };

  return (
    <div className={`App d-flex flex-column ${styles.appBackground}`}>
            <StickyHeader />

      <div className="d-flex">
        <Sidebar />
        <div
          className={`App d-flex container-fluid ${styles.mainContentWrapper}`}
        >
          <Routes>
            <Route
              path="/playlist/:id"
              element=<Playlist changeSongName={changeSongName} />
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
