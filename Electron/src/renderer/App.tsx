import { Route, Routes, useLocation } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Playlist from 'pages/Playlist/Playlist';
import StickyHeader from 'components/StickyHeader/StickyHeader';
import Global from 'global/global';
import Genre from 'pages/Genre/Genre';
import ShowAllItems from 'components/ShowAllItems/ShowAllItems';
import StartMenu from 'pages/StartMenu/StartMenu';
import { ShowAllItemsTypes } from 'components/ShowAllItems/types/PropsShowAllItems';
import UserProfile from 'pages/UserProfile/UserProfile';
import { UserType } from 'utils/role';
import RegisterMenu from 'pages/StartMenu/RegisterMenu';
import styles from './AppCss.module.css';
import Sidebar from '../components/Sidebar/Sidebar';
import Home from '../pages/Home/Home';
import Explorar from '../pages/Explorar/Explorar';
import Footer from '../components/footer/Footer';

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

  const [songName, setSongName] = useState(Global.noSong);
  const changeSongName = (songNameInput: string): void => {
    setSongName(songNameInput);
  };

  /* Handle login status */

  const [isLogged, setIsLogged] = useState(false);

  const handleLogout = () => {
    changeSongName(Global.noSong);
    setIsLogged(false);
  };

  /* Handle register status */

  const [isSigningUp, setIsSigningUp] = useState(false);

  return (
    <>
      {isSigningUp && <RegisterMenu setIsSigningUp={setIsSigningUp} />}
      {!isLogged && !isSigningUp && (
        <StartMenu setIsLogged={setIsLogged} setIsSigningUp={setIsSigningUp} />
      )}
      {isLogged && (
        <div className={`App d-flex flex-column ${styles.appBackground}`}>
          <StickyHeader handleLogout={handleLogout} />

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
                <Route path="/explorar" element=<Explorar /> />
                <Route
                  path="/explorar/genre/:id"
                  element=<Genre
                    changeSongName={changeSongName}
                    refreshSidebarData={reloadSidebar}
                  />
                />

                <Route
                  path="/user/:id"
                  element=<UserProfile
                    refreshSidebarData={reloadSidebar}
                    changeSongName={changeSongName}
                    userType={UserType.USER}
                  />
                />

                <Route
                  path="/artist/:id"
                  element=<UserProfile
                    refreshSidebarData={reloadSidebar}
                    changeSongName={changeSongName}
                    userType={UserType.ARTIST}
                  />
                />

                <Route
                  path="/showAllItemsPlaylist/:id"
                  element=<ShowAllItems
                    refreshSidebarData={reloadSidebar}
                    type={ShowAllItemsTypes.ALL_PLAYLISTS}
                    changeSongName={changeSongName}
                  />
                />
                <Route
                  path="/showAllItemsArtist/:id"
                  element=<ShowAllItems
                    refreshSidebarData={reloadSidebar}
                    type={ShowAllItemsTypes.ALL_ARTISTS}
                    changeSongName={changeSongName}
                  />
                />
                <Route
                  path="/showAllPlaylistFromUser/:id/:user/:usertype"
                  element=<ShowAllItems
                    refreshSidebarData={reloadSidebar}
                    type={ShowAllItemsTypes.ALL_PLAYLIST_FROM_USER}
                    changeSongName={changeSongName}
                  />
                />
                <Route
                  path="/showAllSongsFromArtist/:id/:artist"
                  element=<ShowAllItems
                    refreshSidebarData={reloadSidebar}
                    type={ShowAllItemsTypes.ALL_SONGS_FROM_ARTIST}
                    changeSongName={changeSongName}
                  />
                />
                <Route
                  path="/"
                  element=<Home refreshSidebarData={reloadSidebar} />
                />

                <Route
                  path="*"
                  element=<Home refreshSidebarData={reloadSidebar} />
                />
              </Routes>
            </div>
          </div>
          <Footer songName={songName} />
        </div>
      )}
    </>
  );
}

export default App;
