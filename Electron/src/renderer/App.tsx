import { useState } from 'react';
import { RouterProvider } from 'react-router-dom';
import RegisterMenu from 'pages/StartMenu/RegisterMenu';
import StartMenu from 'pages/StartMenu/StartMenu';
import { deleteToken } from 'utils/token';
import { NowPlayingContextProvider } from 'providers/NowPlayingProvider';
import createAppRouter from 'router/router';

function App() {
  const [refreshSidebarTriggerValue, setRefreshSidebarTriggerValue] =
    useState(false);
  const refreshSidebarData = () => {
    setTimeout(() => setRefreshSidebarTriggerValue((prev) => !prev), 500);
  };

  const [isLogged, setIsLogged] = useState(false);
  const [isSigningUp, setIsSigningUp] = useState(false);
  const handleLogout = () => {
    deleteToken();
    setIsLogged(false);
  };

  const router = createAppRouter({
    refreshSidebarTriggerValue,
    refreshSidebarData,
    handleLogout,
  });

  return (
    <>
      {isSigningUp && <RegisterMenu setIsSigningUp={setIsSigningUp} />}
      {!isLogged && !isSigningUp && (
        <StartMenu setIsLogged={setIsLogged} setIsSigningUp={setIsSigningUp} />
      )}
      <NowPlayingContextProvider>
        {isLogged && <RouterProvider router={router} />}
      </NowPlayingContextProvider>
    </>
  );
}

export default App;
