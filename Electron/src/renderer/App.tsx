import { Route, Routes, useLocation } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Playlist from 'pages/Playlist/Playlist';
import StickyHeader from 'components/StickyHeader/StickyHeader';
import Genre from 'pages/Genre/Genre';
import ShowAllItems from 'components/ShowAllItems/ShowAllItems';
import StartMenu from 'pages/StartMenu/StartMenu';
import { ShowAllItemsTypes } from 'components/ShowAllItems/types/PropsShowAllItems';
import UserProfile from 'pages/UserProfile/UserProfile';
import UserType from 'utils/role';
import RegisterMenu from 'pages/StartMenu/RegisterMenu';
import { deleteToken } from 'utils/token';
import { NowPlayingContextProvider } from 'providers/NowPlayingProvider';
import styles from './AppCss.module.css';
import Sidebar from '../components/Sidebar/Sidebar';
import Home from '../pages/Home/Home';
import Browse from '../pages/Browse/Browse';
import Footer from '../components/footer/Footer';

function App() {
  /* Scroll to the top if path is changed */
  const location = useLocation();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [location]);

  // flag value for trigger sidebar reload from across the app
  const [refreshSidebarTriggerValue, setRefreshSidebarTriggerValue] =
    useState(false);
  // changes the flag value to its opposite so the component triggers a reload
  // wait until backend has data updated, fast requests after update can trigger 404 on backend (Ej: playlist update - sidebar - playlist)
  const refreshSidebarData = () => {
    setTimeout(() => {
      setRefreshSidebarTriggerValue((state) => !state);
    }, 500);
  };

  /* Handle login status */

  const [isLogged, setIsLogged] = useState(false);

  const handleLogout = () => {
    deleteToken();
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
      <NowPlayingContextProvider>
        {isLogged && (
          <div className={`App d-flex flex-column ${styles.appBackground}`}>
            <StickyHeader handleLogout={handleLogout} />

            <div className="d-flex">
              <Sidebar
                refreshSidebarTriggerValue={refreshSidebarTriggerValue}
                refreshSidebarData={refreshSidebarData}
              />
              <div
                className={`App d-flex container-fluid ${styles.mainContentWrapper}`}
              >
                <Routes>
                  <Route
                    path="/playlist/:id"
                    element=<Playlist refreshSidebarData={refreshSidebarData} />
                  />
                  <Route
                    path="/browse"
                    element=<Browse refreshSidebarData={refreshSidebarData} />
                  />
                  <Route
                    path="/browse/genre/:id"
                    element=<Genre refreshSidebarData={refreshSidebarData} />
                  />

                  <Route
                    path="/user/:id"
                    element=<UserProfile
                      refreshSidebarData={refreshSidebarData}
                      userType={UserType.USER}
                    />
                  />

                  <Route
                    path="/artist/:id"
                    element=<UserProfile
                      refreshSidebarData={refreshSidebarData}
                      userType={UserType.ARTIST}
                    />
                  />

                  <Route
                    path="/showAllItemsPlaylist/:id"
                    element=<ShowAllItems
                      refreshSidebarData={refreshSidebarData}
                      type={ShowAllItemsTypes.ALL_PLAYLISTS}
                    />
                  />
                  <Route
                    path="/showAllItemsArtist/:id"
                    element=<ShowAllItems
                      refreshSidebarData={refreshSidebarData}
                      type={ShowAllItemsTypes.ALL_ARTISTS}
                    />
                  />
                  <Route
                    path="/showAllPlaylistFromUser/:id/:user/:usertype"
                    element=<ShowAllItems
                      refreshSidebarData={refreshSidebarData}
                      type={ShowAllItemsTypes.ALL_PLAYLIST_FROM_USER}
                    />
                  />
                  <Route
                    path="/showAllSongsFromArtist/:id/:artist"
                    element=<ShowAllItems
                      refreshSidebarData={refreshSidebarData}
                      type={ShowAllItemsTypes.ALL_SONGS_FROM_ARTIST}
                    />
                  />
                  <Route
                    path="/"
                    element=<Home refreshSidebarData={refreshSidebarData} />
                  />

                  <Route
                    path="*"
                    element=<Home refreshSidebarData={refreshSidebarData} />
                  />
                </Routes>
              </div>
            </div>
            <Footer />
          </div>
        )}
      </NowPlayingContextProvider>
    </>
  );
}

export default App;
