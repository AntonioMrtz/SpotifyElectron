import React, { useEffect, useState } from 'react';
import { Route, Routes, useLocation } from 'react-router-dom';
import Playlist from 'pages/Playlist/Playlist';
import StickyHeader from 'components/StickyHeader/StickyHeader';
import Global from 'global/global';
import Genre from 'pages/Genre/Genre';
import ShowAllItems from 'components/ShowAllItems/ShowAllItems';
import StartMenu from 'pages/StartMenu/StartMenu';
import { ShowAllItemsTypes } from 'components/ShowAllItems/types/PropsShowAllItems';
import UserProfile from 'pages/UserProfile/UserProfile';
import UserType from 'utils/role';
import RegisterMenu from 'pages/StartMenu/RegisterMenu';
import { deleteToken } from 'utils/token';
import Sidebar from 'components/Sidebar/Sidebar';
import Home from 'pages/Home/Home';
import Explorar from 'pages/Explorar/Explorar';
import Footer from 'components/footer/Footer';
import { SidebarProvider, useSidebar } from 'components/Sidebar/SidebarContext';
import styles from './AppCss.module.css';

function App() {
  const location = useLocation();
  const [songName, setSongName] = useState<string>(Global.noSongPlaying);
  const [isLogged, setIsLogged] = useState<boolean>(false);
  const [isSigningUp, setIsSigningUp] = useState<boolean>(false);

  // Call useSidebar here, outside of conditional rendering
  const { refreshSidebarData } = useSidebar();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [location]);

  const changeSongName = (songNameInput: string): void => {
    setSongName(songNameInput);
  };

  const handleLogout = (): void => {
    changeSongName(Global.noSongPlaying);
    deleteToken();
    setIsLogged(false);
  };

  return (
    <>
      {isSigningUp && <RegisterMenu setIsSigningUp={setIsSigningUp} />}
      {!isLogged && !isSigningUp && (
        <StartMenu setIsLogged={setIsLogged} setIsSigningUp={setIsSigningUp} />
      )}
      {isLogged && (
        <SidebarProvider>
          <div className={`App d-flex flex-column ${styles.appBackground}`}>
            <StickyHeader handleLogout={handleLogout} />
            <div className="d-flex">
              <Sidebar />
              <div
                className={`App d-flex container-fluid ${styles.mainContentWrapper}`}
              >
                <Routes>
                  <Route
                    path="/playlist/:id"
                    element={
                      <Playlist
                        changeSongName={changeSongName}
                        refreshSidebarData={refreshSidebarData}
                      />
                    }
                  />
                  <Route
                    path="/explorar"
                    element={
                      <Explorar
                        changeSongName={changeSongName}
                        refreshSidebarData={refreshSidebarData} // Pass the missing prop here
                      />
                    }
                  />
                  <Route
                    path="/explorar/genre/:id"
                    element={
                      <Genre
                        changeSongName={changeSongName}
                        refreshSidebarData={refreshSidebarData} // Pass the missing prop here
                      />
                    }
                  />
                  <Route
                    path="/user/:id"
                    element={
                      <UserProfile
                        changeSongName={changeSongName}
                        userType={UserType.USER}
                        refreshSidebarData={refreshSidebarData} // Pass the missing prop here
                      />
                    }
                  />
                  <Route
                    path="/artist/:id"
                    element={
                      <UserProfile
                        changeSongName={changeSongName}
                        userType={UserType.ARTIST}
                        refreshSidebarData={refreshSidebarData} // Pass the missing prop here
                      />
                    }
                  />
                  <Route
                    path="/showAllItemsPlaylist/:id"
                    element={
                      <ShowAllItems
                        type={ShowAllItemsTypes.ALL_PLAYLISTS}
                        changeSongName={changeSongName}
                        refreshSidebarData={refreshSidebarData} // Pass the missing prop here
                      />
                    }
                  />
                  <Route
                    path="/showAllItemsArtist/:id"
                    element={
                      <ShowAllItems
                        type={ShowAllItemsTypes.ALL_ARTISTS}
                        changeSongName={changeSongName}
                        refreshSidebarData={refreshSidebarData} // Pass the missing prop here
                      />
                    }
                  />
                  <Route
                    path="/showAllPlaylistFromUser/:id/:user/:usertype"
                    element={
                      <ShowAllItems
                        type={ShowAllItemsTypes.ALL_PLAYLIST_FROM_USER}
                        changeSongName={changeSongName}
                        refreshSidebarData={refreshSidebarData} // Pass the missing prop here
                      />
                    }
                  />
                  <Route
                    path="/showAllSongsFromArtist/:id/:artist"
                    element={
                      <ShowAllItems
                        type={ShowAllItemsTypes.ALL_SONGS_FROM_ARTIST}
                        changeSongName={changeSongName}
                        refreshSidebarData={refreshSidebarData} // Pass the missing prop here
                      />
                    }
                  />
                  <Route
                    path="/"
                    element={<Home refreshSidebarData={refreshSidebarData} />} // Pass the missing prop here
                  />
                  <Route
                    path="*"
                    element={<Home refreshSidebarData={refreshSidebarData} />}
                  />{' '}
                  {/* Pass the missing prop here */}
                </Routes>
              </div>
            </div>
            <Footer songName={songName} />
          </div>
        </SidebarProvider>
      )}
    </>
  );
}

export default App;
