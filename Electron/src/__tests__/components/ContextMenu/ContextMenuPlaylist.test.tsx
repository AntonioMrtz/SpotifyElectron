import '@testing-library/jest-dom';
import '@testing-library/jest-dom/extend-expect';
import { act, fireEvent, render } from '@testing-library/react';
import ContextMenuPlaylist from 'components/AdvancedUIComponents/ContextMenu/Playlist/ContextMenuPlaylist';
import Global from 'global/global';
import { BrowserRouter } from 'react-router-dom';
import UserType from 'utils/role';
import * as router from 'react-router';
import getMockHeaders from 'utils/mockHeaders';
import * as TokenModule from 'utils/token';
import { t } from 'i18next';

const playlistName = 'playlisttest';
const songName = 'songName';
const userName = 'prueba';
const roleUser = UserType.ARTIST;

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

const navigate = jest.fn();

jest.spyOn(router, 'useNavigate').mockImplementation(() => navigate);

jest.spyOn(TokenModule, 'getTokenUsername').mockReturnValue(userName);
jest.spyOn(TokenModule, 'getTokenRole').mockReturnValue(roleUser);

// Mock localStorage
const localStorageMock = {
  storage: {} as { [key: string]: string },
  getItem: jest.fn((key: string) => localStorageMock.storage[key] || null),
  setItem: jest.fn((key: string, value: string) => {
    localStorageMock.storage[key] = value;
  }),
  removeItem: jest.fn((key: string) => {
    delete localStorageMock.storage[key];
  }),
  clear: jest.fn(() => {
    localStorageMock.storage = {};
  }),
};

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

beforeEach(() => {
  jest.clearAllMocks();
  localStorageMock.clear();
});

global.fetch = jest.fn((url: string, options: any) => {
  if (
    url === `${Global.backendBaseUrl}/playlists/${playlistDTOMockFetch.name}`
  ) {
    return Promise.resolve({
      json: () => playlistDTOMockFetch,
      status: 200,
      ok: true,
      headers: getMockHeaders(),
    }).catch((error) => {
      console.log(error);
    });
  }
  if (
    url ===
    `${Global.backendBaseUrl}/users/${artistMockFetch.name}/playlist_names`
  ) {
    return Promise.resolve({
      json: () => [playlistName],
      status: 200,
      ok: true,
      headers: getMockHeaders(),
    }).catch((error) => {
      console.log(error);
    });
  }
  if (options && options.method) {
    if (options.method === 'DELETE') {
      return Promise.resolve({
        json: () => {},
        status: 202,
        ok: true,
      }).catch((error) => {
        console.log(error);
      });
    }
    if (options.method === 'PUT') {
      return Promise.resolve({
        json: () => {},
        status: 204,
        ok: true,
        headers: getMockHeaders(),
      }).catch((error) => {
        console.log(error);
      });
    }
    if (options.method === 'PATCH') {
      return Promise.resolve({
        json: () => {},
        status: 204,
        ok: true,
        headers: getMockHeaders(),
      }).catch((error) => {
        console.log(error);
      });
    }
    if (options.method === 'POST') {
      return Promise.resolve({
        json: () => artistMockFetch,
        status: 201,
        ok: true,
      }).catch((error) => {
        console.log(error);
      });
    }
  }
  // In case the URL doesn't match, return a rejected promise
  return Promise.reject(new Error(`Unhandled URL in fetch mock: ${url}`));
}) as jest.Mock;

test('Render ContextMenuPlaylist', async () => {
  const component = await act(() => {
    return render(
      <BrowserRouter>
        <ContextMenuPlaylist
          playlistName={playlistName}
          owner={artistMockFetch.name}
          handleCloseParent={jest.fn()}
          refreshPlaylistData={jest.fn()}
          refreshSidebarData={jest.fn()}
        />
      </BrowserRouter>,
    );
  });
  expect(component).toBeTruthy();
});

test('ContextMenuPlaylist delete Playlist success', async () => {
  const refreshSidebarDataMock = jest.fn();

  const component = await act(() => {
    return render(
      <BrowserRouter>
        <ContextMenuPlaylist
          playlistName={playlistName}
          owner={artistMockFetch.name}
          handleCloseParent={jest.fn()}
          refreshPlaylistData={jest.fn()}
          refreshSidebarData={refreshSidebarDataMock}
        />
      </BrowserRouter>,
    );
  });

  const deleteButton = component.getByText(t('contextMenuPlaylist.delete'));
  if (deleteButton) {
    await act(async () => {
      fireEvent.click(deleteButton);
    });
  }

  expect(refreshSidebarDataMock).toHaveBeenCalled();
});

test('ContextMenuPlaylist Add Playlist to Playlist', async () => {
  const refreshSidebarDataMock = jest.fn();

  const component = await act(() => {
    return render(
      <BrowserRouter>
        <ContextMenuPlaylist
          playlistName={playlistName}
          owner={artistMockFetch.name}
          handleCloseParent={jest.fn()}
          refreshPlaylistData={jest.fn()}
          refreshSidebarData={refreshSidebarDataMock}
        />
      </BrowserRouter>,
    );
  });

  const addToOtherPlaylistButton = component.getByText(
    t('contextMenuPlaylist.add-to-playlist'),
  );
  if (addToOtherPlaylistButton) {
    await act(async () => {
      fireEvent.click(addToOtherPlaylistButton);
    });
  }

  const playlistButton = component.getByText(playlistName);
  if (playlistButton) {
    await act(async () => {
      fireEvent.click(playlistButton);
    });
  }

  expect(
    component.queryByText(
      t('contextMenuPlaylist.confirmationMenu.add-success.title'),
    ),
  ).toBeInTheDocument();
});

test('ContextMenuPlaylist edit playlist navigates to correct route', async () => {
  const mockHandleClose = jest.fn();

  // Clear previous navigate calls
  navigate.mockClear();

  const component = await act(() => {
    return render(
      <BrowserRouter>
        <ContextMenuPlaylist
          playlistName={playlistName}
          owner={userName}
          handleCloseParent={mockHandleClose}
          refreshPlaylistData={jest.fn()}
          refreshSidebarData={jest.fn()}
        />
      </BrowserRouter>,
    );
  });

  // Find and click the edit button
  const editButton = component.getByText(t('contextMenuPlaylist.edit'));

  await act(async () => {
    fireEvent.click(editButton);
  });

  // Verify navigation was called with correct route (singular /playlist/, not /playlists/)
  expect(navigate).toHaveBeenCalledWith(`/playlist/${playlistName}?edit=true`, { replace: true });

  // Verify localStorage was set
  expect(localStorage.getItem('playlistEdit')).toBe('true');

  // Verify close handler was called
  expect(mockHandleClose).toHaveBeenCalled();
});
