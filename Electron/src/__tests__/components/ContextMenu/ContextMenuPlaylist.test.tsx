import '@testing-library/jest-dom';
import '@testing-library/jest-dom/extend-expect';
import { act, fireEvent, render, waitFor } from '@testing-library/react';
import ContextMenuPlaylist from 'components/AdvancedUIComponents/ContextMenu/Playlist/ContextMenuPlaylist';
import Global from 'global/global';
import { BrowserRouter } from 'react-router-dom';
import UserType from 'utils/role';
import * as router from 'react-router';
import getMockHeaders from 'utils/mockHeaders';
import * as TokenModule from 'utils/token';
import i18n, { t } from 'i18next';
import { SidebarProvider } from 'providers/SidebarProvider';
import { NowPlayingContextProvider } from 'providers/NowPlayingProvider';
import { initReactI18next } from 'react-i18next';

// Initialize i18next for testing
i18n.use(initReactI18next).init({
  lng: 'en',
  fallbackLng: 'en',
  ns: ['contextMenuPlaylist'],
  defaultNS: 'contextMenuPlaylist',
  resources: {
    en: {
      contextMenuPlaylist: {
        'add-to-queue': 'Add to queue',
        edit: 'Edit',
        'create-similar-playlist': 'Create similar playlist',
        delete: 'Delete',
        download: 'Download',
        'add-to-playlist': 'Add to playlist',
        share: 'Share',
        'search-playlist': 'Search playlist',
        'create-playlist': 'Create playlist',
        'confirmationMenu.delete-success.title': 'Playlist deleted',
        'confirmationMenu.delete-success.description':
          'The playlist has been deleted successfully',
        'confirmationMenu.add-success.title': 'Songs added',
        'confirmationMenu.add-success.description':
          'The songs have been added successfully',
        'confirmationMenu.add-error.title': 'Error adding songs',
        'confirmationMenu.add-error.description':
          'Unable to add songs to playlist',
        'confirmationMenu.delete-error.title': 'Error deleting playlist',
        'confirmationMenu.delete-error.description':
          'Unable to delete playlist',
        'confirmationMenu.clipboard.title': 'Copied to clipboard',
        'confirmationMenu.clipboard.description':
          'The link has been copied to clipboard',
        'confirmationMenu.error.title': 'Error',
        'confirmationMenu.error.description': 'An error occurred',
      },
    },
  },
  interpolation: {
    escapeValue: false,
  },
});

// Wait for i18next to be ready
beforeAll(async () => {
  await new Promise((resolve) => {
    if (i18n.isInitialized) {
      resolve(true);
    } else {
      i18n.on('initialized', () => resolve(true));
    }
  });
});

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
        <SidebarProvider>
          <NowPlayingContextProvider>
            <ContextMenuPlaylist
              playlistName={playlistName}
              owner={artistMockFetch.name}
              handleCloseParent={jest.fn()}
              refreshPlaylistData={jest.fn()}
            />
          </NowPlayingContextProvider>
        </SidebarProvider>
      </BrowserRouter>,
    );
  });
  expect(component).toBeTruthy();
});

test('ContextMenuPlaylist delete Playlist success', async () => {
  const component = await act(async () => {
    return render(
      <BrowserRouter>
        <SidebarProvider>
          <NowPlayingContextProvider>
            <ContextMenuPlaylist
              playlistName={playlistName}
              owner={artistMockFetch.name}
              handleCloseParent={jest.fn()}
              refreshPlaylistData={jest.fn()}
            />
          </NowPlayingContextProvider>
        </SidebarProvider>
      </BrowserRouter>,
    );
  });

  // Wait for the delete button to appear
  await waitFor(
    () => {
      const deleteButton = component.getByText('contextMenuPlaylist.delete');
      expect(deleteButton).toBeInTheDocument();
    },
    {
      timeout: 3000,
      interval: 100,
    },
  );

  const deleteButton = component.getByText('contextMenuPlaylist.delete');
  await act(async () => {
    fireEvent.click(deleteButton);
  });

  // Wait for navigation to home page
  await waitFor(
    () => {
      expect(navigate).toHaveBeenCalledWith('/home');
    },
    {
      timeout: 3000,
      interval: 100,
    },
  );
});

test('ContextMenuPlaylist Add Playlist to Playlist', async () => {
  const refreshSidebarDataMock = jest.fn();

  const component = await act(async () => {
    return render(
      <BrowserRouter>
        <SidebarProvider>
          <NowPlayingContextProvider>
            <ContextMenuPlaylist
              playlistName={playlistName}
              owner={artistMockFetch.name}
              handleCloseParent={jest.fn()}
              refreshPlaylistData={jest.fn()}
            />
          </NowPlayingContextProvider>
        </SidebarProvider>
      </BrowserRouter>,
    );
  });

  // Wait for the add to playlist button to appear
  await waitFor(
    () => {
      const addToOtherPlaylistButton = component.getByText(
        'contextMenuPlaylist.add-to-playlist',
      );
      expect(addToOtherPlaylistButton).toBeInTheDocument();
    },
    {
      timeout: 3000,
      interval: 100,
    },
  );

  const addToOtherPlaylistButton = component.getByText(
    'contextMenuPlaylist.add-to-playlist',
  );
  await act(async () => {
    fireEvent.click(addToOtherPlaylistButton);
  });

  // Wait for the playlist button to appear
  await waitFor(
    () => {
      const playlistButton = component.getByText(playlistName);
      expect(playlistButton).toBeInTheDocument();
    },
    {
      timeout: 3000,
      interval: 100,
    },
  );

  const playlistButton = component.getByText(playlistName);
  await act(async () => {
    fireEvent.click(playlistButton);
  });

  // Wait for the success message to appear
  await waitFor(
    () => {
      const successMessage = component.getByText(
        'contextMenuPlaylist.confirmationMenu.add-success.title',
      );
      expect(successMessage).toBeInTheDocument();
    },
    {
      timeout: 3000,
      interval: 100,
    },
  );
});
