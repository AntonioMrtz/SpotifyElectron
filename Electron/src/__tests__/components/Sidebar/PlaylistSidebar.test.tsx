import '@testing-library/jest-dom';
import { act, fireEvent, render } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { MemoryRouter } from 'react-router-dom';
import Global from 'global/global';
import UserType from 'utils/role';
import PlaylistSidebar from 'components/Sidebar/Playlist/PlaylistSidebar';
import getMockHeaders from 'utils/mockHeaders';
import * as router from 'react-router';
import * as TokenModule from 'utils/token';
import { t } from 'i18next';
import { SidebarProvider } from 'providers/SidebarProvider';

const playlistName = 'playlisttest';
const songName = 'songName';
const userName = 'prueba';
const roleUser = UserType.ARTIST;

const navigate = jest.fn();
jest.spyOn(router, 'useNavigate').mockImplementation(() => navigate);

const artistMockFetch = {
  name: userName,
  photo: 'photo',
  register_date: 'date',
  password: 'hashpassword',
  playback_history: [songName],
  playlists: [playlistName],
  saved_playlists: [playlistName],
  uploaded_songs: [songName],
};

const playlistDTOMockFetch = {
  name: playlistName,
  photo: 'playlist',
  description: 'des',
  upload_date: 'date',
  owner: userName,
  song_names: [],
};

jest.spyOn(TokenModule, 'getTokenUsername').mockReturnValue(userName);
jest.spyOn(TokenModule, 'getTokenRole').mockReturnValue(roleUser);

test('render Sidebar Playlist', async () => {
  const handleUrlPlaylistClicked = () => jest.fn();
  const refreshSidebarData = () => jest.fn();

  const component = await act(() => {
    return render(
      <MemoryRouter>
        <SidebarProvider>
          <PlaylistSidebar
            name={playlistDTOMockFetch.name}
            photo={playlistDTOMockFetch.photo}
            owner={artistMockFetch.name}
            playlistStyle=""
            handleUrlPlaylistClicked={handleUrlPlaylistClicked}
            refreshSidebarData={refreshSidebarData}
          />
        </SidebarProvider>
      </MemoryRouter>,
    );
  });

  expect(component).toBeTruthy();
  expect(component.queryByText(playlistName)).toBeInTheDocument();
});

test('Sidebar Playlist handle open context menu', async () => {
  const handleUrlPlaylistClickedMock = jest.fn();
  const refreshSidebarDataMock = jest.fn();

  global.fetch = jest.fn(async (url: string) => {
    if (url === `${Global.backendBaseUrl}/artists/${artistMockFetch.name}`) {
      return Promise.resolve({
        json: () => artistMockFetch,
        status: 200,
        ok: true,
        headers: getMockHeaders(),
      }).catch((error) => {
        console.log(error);
      });
    }
    if (url === `${Global.backendBaseUrl}/playlists/selected/${playlistName}`) {
      return Promise.resolve({
        json: () =>
          Promise.resolve({
            playlists: [playlistDTOMockFetch],
          }),
        status: 200,
        ok: true,
        headers: getMockHeaders(),
      }).catch((error) => {
        console.log(error);
      });
    }

    // In case the URL doesn't match, return a rejected promise
    return Promise.reject(new Error(`Unhandled URL in fetch mock: ${url}`));
  }) as jest.Mock;

  const component = await act(() => {
    return render(
      <MemoryRouter>
        <SidebarProvider>
          <PlaylistSidebar
            name={playlistDTOMockFetch.name}
            photo={playlistDTOMockFetch.photo}
            owner={artistMockFetch.name}
            playlistStyle=""
            handleUrlPlaylistClicked={handleUrlPlaylistClickedMock}
            refreshSidebarData={refreshSidebarDataMock}
          />
        </SidebarProvider>
      </MemoryRouter>,
    );
  });

  const playlistItemClickable = component.getByTestId(
    'sidebar-playlist-wrapper',
  );

  await act(async () => {
    fireEvent.contextMenu(playlistItemClickable);
  });

  expect(
    component.getByText(t('contextMenuPlaylist.create-similar-playlist')),
  ).toBeInTheDocument();
});

test('Sidebar Playlist left-click', async () => {
  const handleUrlPlaylistClickedMock = jest.fn();
  const refreshSidebarDataMock = jest.fn();

  global.fetch = jest.fn(async (url: string) => {
    if (url === `${Global.backendBaseUrl}/artists/${artistMockFetch.name}`) {
      return Promise.resolve({
        json: () => artistMockFetch,
        status: 200,
        ok: true,
        headers: getMockHeaders(),
      }).catch((error) => {
        console.log(error);
      });
    }
    if (url === `${Global.backendBaseUrl}/playlists/selected/${playlistName}`) {
      return Promise.resolve({
        json: () =>
          Promise.resolve({
            playlists: [playlistDTOMockFetch],
          }),
        status: 200,
        ok: true,
        headers: getMockHeaders(),
      }).catch((error) => {
        console.log(error);
      });
    }

    // In case the URL doesn't match, return a rejected promise
    return Promise.reject(new Error(`Unhandled URL in fetch mock: ${url}`));
  }) as jest.Mock;

  const component = await act(() => {
    return render(
      <MemoryRouter>
        <SidebarProvider>
          <PlaylistSidebar
            name={playlistDTOMockFetch.name}
            photo={playlistDTOMockFetch.photo}
            owner={artistMockFetch.name}
            playlistStyle=""
            handleUrlPlaylistClicked={handleUrlPlaylistClickedMock}
            refreshSidebarData={refreshSidebarDataMock}
          />
        </SidebarProvider>
      </MemoryRouter>,
    );
  });

  const playlistItemClickable = component.getByTestId(
    'sidebar-playlist-wrapper',
  );

  await act(async () => {
    fireEvent.click(playlistItemClickable);
  });

  expect(handleUrlPlaylistClickedMock).toHaveBeenCalledWith(playlistName);
});
