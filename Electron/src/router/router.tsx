import { createBrowserRouter } from 'react-router-dom';
import Playlist from 'pages/Playlist/Playlist';
import Browse from 'pages/Browse/Browse';
import Genre from 'pages/Genre/Genre';
import UserProfile from 'pages/UserProfile/UserProfile';
import ShowAllItems from 'components/ShowAllItems/ShowAllItems';
import Home from 'pages/Home/Home';
import { ShowAllItemsTypes } from 'components/ShowAllItems/types/PropsShowAllItems';
import UserType from 'utils/role';
import { Layout, LayoutContextProps } from 'layout/layout';

const createAppRouter = ({
  refreshSidebarTriggerValue,
  refreshSidebarData,
  handleLogout,
}: LayoutContextProps) => {
  const router = createBrowserRouter([
    {
      path: '/',
      element: (
        <Layout
          refreshSidebarTriggerValue={refreshSidebarTriggerValue}
          refreshSidebarData={refreshSidebarData}
          handleLogout={handleLogout}
        />
      ),
      children: [
        {
          path: 'playlist/:id',
          element: <Playlist refreshSidebarData={refreshSidebarData} />,
        },
        {
          path: 'browse',
          element: <Browse refreshSidebarData={refreshSidebarData} />,
        },
        {
          path: 'browse/genre/:id',
          element: <Genre refreshSidebarData={refreshSidebarData} />,
        },
        {
          path: 'user/:id',
          element: (
            <UserProfile
              refreshSidebarData={refreshSidebarData}
              userType={UserType.USER}
            />
          ),
        },
        {
          path: 'artist/:id',
          element: (
            <UserProfile
              refreshSidebarData={refreshSidebarData}
              userType={UserType.ARTIST}
            />
          ),
        },
        {
          path: 'showAllItemsPlaylist/:id',
          element: (
            <ShowAllItems
              refreshSidebarData={refreshSidebarData}
              type={ShowAllItemsTypes.ALL_PLAYLISTS}
            />
          ),
        },
        {
          path: 'showAllItemsArtist/:id',
          element: (
            <ShowAllItems
              refreshSidebarData={refreshSidebarData}
              type={ShowAllItemsTypes.ALL_ARTISTS}
            />
          ),
        },
        {
          path: 'showAllPlaylistFromUser/:id/:user/:usertype',
          element: (
            <ShowAllItems
              refreshSidebarData={refreshSidebarData}
              type={ShowAllItemsTypes.ALL_PLAYLIST_FROM_USER}
            />
          ),
        },
        {
          path: 'showAllSongsFromArtist/:id/:artist',
          element: (
            <ShowAllItems
              refreshSidebarData={refreshSidebarData}
              type={ShowAllItemsTypes.ALL_SONGS_FROM_ARTIST}
            />
          ),
        },
        {
          index: true,
          element: <Home refreshSidebarData={refreshSidebarData} />,
        },
        {
          path: '/*',
          element: <Home refreshSidebarData={refreshSidebarData} />,
        },
      ],
    },
  ]);
  return router;
};

export default createAppRouter;
