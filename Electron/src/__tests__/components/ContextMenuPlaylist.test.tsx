import '@testing-library/jest-dom';
import { act, fireEvent, render } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import ContextMenuPlaylist from 'components/AdvancedUIComponents/ContextMenu/Playlist/ContextMenuPlaylist';
import Playlist from 'pages/Playlist/Playlist';
import Global from 'global/global';
import UserType from 'utils/role';
import getMockHeaders from 'utils/mockHeaders';
import * as TokenModule from 'utils/token';
import { NowPlayingContextProvider } from 'providers/NowPlayingProvider';
import * as router from 'react-router';

const userName = 'testuser';
const roleUser = UserType.USER;
const playlistName = 'testplaylist';
const songName = 'testsong';

const playlistDTOMockFetch = {
  name: playlistName,
  photo: 'playlist',
  description: 'test description',
  upload_date: 'date',
  owner: userName,
  song_names: [songName],
};

const songMockFetch = {
  name: songName,
  artist: 'artist',
  photo: 'photo',
  seconds_duration: '180',
  genre: 'Rock',
  streams: 2,
  file: '',
};

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

const userMockFetch = {
  name: userName,
  photo: 'photo',
  register_date: 'date',
  password: 'hashpassword',
  playback_history: [songName],
  playlists: [playlistName],
  saved_playlists: [playlistName],
};

jest.spyOn(TokenModule, 'getTokenUsername').mockReturnValue(userName);
jest.spyOn(TokenModule, 'getTokenRole').mockReturnValue(roleUser);

const mockNavigate = jest.fn();

beforeEach(() => {
  jest.spyOn(router, 'useNavigate').mockImplementation(() => mockNavigate);
  jest.clearAllMocks();
  localStorage.clear();
});

test('Context menu edit playlist navigates to correct route', async () => {
  const mockHandleClose = jest.fn();
  const mockRefreshPlaylistData = jest.fn();
  const mockRefreshSidebarData = jest.fn();

  const component = render(
    <MemoryRouter>
      <ContextMenuPlaylist
        playlistName={playlistName}
        owner={userName}
        handleCloseParent={mockHandleClose}
        refreshPlaylistData={mockRefreshPlaylistData}
        refreshSidebarData={mockRefreshSidebarData}
      />
    </MemoryRouter>
  );

  // Find the edit button
  const editButton = component.getByText('contextMenuPlaylist.edit');
  
  await act(async () => {
    fireEvent.click(editButton);
  });

  // Verify navigation was called with correct route (singular /playlist/, not /playlists/)
  expect(mockNavigate).toHaveBeenCalledWith(`/playlist/${playlistName}?edit=true`, { replace: true });
  
  // Verify localStorage was set
  expect(localStorage.getItem('playlistEdit')).toBe('true');
  
  // Verify close handler was called
  expect(mockHandleClose).toHaveBeenCalled();
});

test('Edit playlist modal opens when navigating with edit=true parameter', async () => {
  global.fetch = jest.fn((url: string) => {
    if (url === `${Global.backendBaseUrl}/playlists/${playlistDTOMockFetch.name}`) {
      return Promise.resolve({
        json: () => playlistDTOMockFetch,
        status: 200,
        ok: true,
        headers: getMockHeaders(),
      });
    }
    if (url === `${Global.backendBaseUrl}/artists/${artistMockFetch.name}`) {
      return Promise.resolve({
        json: () => artistMockFetch,
        status: 200,
        ok: true,
        headers: getMockHeaders(),
      });
    }
    if (url === `${Global.backendBaseUrl}/songs/metadata/${songName}`) {
      return Promise.resolve({
        json: () => songMockFetch,
        status: 200,
        ok: true,
        headers: getMockHeaders(),
      });
    }
    if (url === `${Global.backendBaseUrl}/users/${userMockFetch.name}`) {
      return Promise.resolve({
        json: () => userMockFetch,
        status: 200,
        ok: true,
        headers: getMockHeaders(),
      });
    }
    return Promise.reject(new Error(`Unhandled URL in fetch mock: ${url}`));
  }) as jest.Mock;

  // Set localStorage to simulate coming from context menu
  localStorage.setItem('playlistEdit', 'true');

  const component = await act(() => {
    return render(
      <MemoryRouter initialEntries={[`/playlist/${playlistDTOMockFetch.name}?edit=true`]}>
        <NowPlayingContextProvider>
          <Routes>
            <Route
              path="/playlist/:id"
              element={<Playlist refreshSidebarData={jest.fn()} />}
            />
          </Routes>
        </NowPlayingContextProvider>
      </MemoryRouter>,
    );
  });

  // Wait for the component to load and process the localStorage flag
  await act(async () => {
    // Give time for useEffect to run
    await new Promise(resolve => setTimeout(resolve, 100));
  });

  // Verify the edit modal is open by checking for edit modal content
  expect(component.getByText('playlist.edit-details')).toBeInTheDocument();
  expect(component.getByText('playlist.save')).toBeInTheDocument();
  
  // Verify localStorage was cleared
  expect(localStorage.getItem('playlistEdit')).toBe('false');
});
