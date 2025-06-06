import '@testing-library/jest-dom';
import { act, fireEvent, render, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { MemoryRouter } from 'react-router-dom';
import Global from 'global/global';
import Playlist from 'pages/Playlist/Playlist';
import getMockHeaders from 'utils/mockHeaders';
import { SidebarProvider } from 'providers/SidebarProvider';
import { NowPlayingContextProvider } from 'providers/NowPlayingProvider';
import i18n, { t } from 'i18next';
import UserType from 'utils/role';
import * as TokenModule from 'utils/token';
import { initReactI18next } from 'react-i18next';
import { debug } from 'jest-preview';

// Initialize i18next for testing
i18n.use(initReactI18next).init({
  lng: 'en',
  fallbackLng: 'en',
  ns: ['playlist', 'common'],
  defaultNS: 'playlist',
  resources: {
    en: {
      playlist: {
        'edit-details': 'Edit details',
        name: 'Name',
        description: 'Description',
        thumbnail: 'Thumbnail',
        save: 'Save',
        title: 'Title',
        songs: 'songs',
        plays: 'Plays',
      },
      common: {
        album: 'Album',
        playlist: 'Playlist',
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
const userName = 'prueba';
const songName = 'songName';
const roleUser = UserType.USER;

const playlistDTOMockFetch = {
  name: playlistName,
  photo: 'playlist',
  description: 'des',
  upload_date: 'date',
  owner: userName,
  song_names: [songName],
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

const songMockFetch = {
  name: songName,
  artist: 'artist',
  photo: 'photo',
  seconds_duration: '180',
  genre: 'Rock',
  streams: 2,
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

// First, let's declare the mock data types at the top level
interface PlaylistDTO {
  name: string;
  photo: string;
  description: string;
  upload_date: string;
  owner: string;
  song_names: string[];
}

interface UserMock {
  name: string;
  photo: string;
  register_date: string;
  password: string;
  playback_history: string[];
  playlists: string[];
  saved_playlists: string[];
}

test('Playlist user role get all info', async () => {
  global.fetch = jest.fn((url: string) => {
    if (url === `${Global.backendBaseUrl}/playlists/${playlistName}`) {
      return Promise.resolve({
        json: () => playlistDTOMockFetch,
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
    if (url === `${Global.backendBaseUrl}/playlists/liked`) {
      return Promise.resolve({
        json: () => [],
        status: 200,
        ok: true,
        headers: getMockHeaders(),
      });
    }
    return Promise.reject(new Error(`Unhandled URL in fetch mock: ${url}`));
  }) as jest.Mock;

  const component = await act(async () => {
    return render(
      <MemoryRouter initialEntries={[`/playlist/${playlistName}`]}>
        <SidebarProvider>
          <NowPlayingContextProvider>
            <Playlist />
          </NowPlayingContextProvider>
        </SidebarProvider>
      </MemoryRouter>,
    );
  });

  expect(component).toBeTruthy();

  // Wait for the playlist name to appear
  await waitFor(
    () => {
      const playlistCardName = component.container.querySelector('h1');
      expect(playlistCardName).toBeInTheDocument();
      expect(playlistCardName?.textContent).toBe(playlistDTOMockFetch.name);
    },
    {
      timeout: 3000,
      interval: 100,
    },
  );

  // Wait for the song name to appear in the song list
  await waitFor(
    () => {
      const songNameElement = component.container.querySelector(
        '.songTitleTable.titleContainer',
      );
      expect(songNameElement).toBeInTheDocument();
      expect(songNameElement?.textContent).toBe(songMockFetch.name);
    },
    {
      timeout: 3000,
      interval: 100,
    },
  );
});

test('Playlist user role hit like button', async () => {
  global.fetch = jest.fn((url: string) => {
    if (url === `${Global.backendBaseUrl}/playlists/selected/${playlistName}`) {
      return Promise.resolve({
        json: () => [playlistDTOMockFetch],
        status: 200,
        ok: true,
        headers: getMockHeaders(),
      }).catch((error) => {
        console.log(error);
      });
    }
    if (url === `${Global.backendBaseUrl}/songs/metadata/${songName}`) {
      return Promise.resolve({
        json: () => songMockFetch,
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

  const component = await act(async () => {
    return render(
      <MemoryRouter initialEntries={[`/playlist/${playlistName}`]}>
        <SidebarProvider>
          <NowPlayingContextProvider>
            <Playlist />
          </NowPlayingContextProvider>
        </SidebarProvider>
      </MemoryRouter>,
    );
  });

  expect(component).toBeTruthy();

  // Wait for the like button to appear
  await waitFor(() => {
    const likeButton = component.container.querySelector(
      '#playlist-like-button',
    );
    expect(likeButton).toBeInTheDocument();
  });

  const likeButton = component.container.querySelector('#playlist-like-button');

  await act(async () => {
    fireEvent.click(likeButton!);
  });

  // Wait for the unlike button to appear after clicking like
  await waitFor(() => {
    const unlikeButton = component.container.querySelector(
      '#playlist-unlike-button',
    );
    expect(unlikeButton).toBeInTheDocument();
  });
});

test('Playlist user role get unlike button', async () => {
  global.fetch = jest.fn((url: string) => {
    if (url === `${Global.backendBaseUrl}/playlists/selected/${playlistName}`) {
      return Promise.resolve({
        json: () => [playlistDTOMockFetch],
        status: 200,
        ok: true,
        headers: getMockHeaders(),
      }).catch((error) => {
        console.log(error);
      });
    }
    if (url === `${Global.backendBaseUrl}/songs/metadata/${songName}`) {
      return Promise.resolve({
        json: () => songMockFetch,
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

  const component = await act(async () => {
    return render(
      <MemoryRouter initialEntries={[`/playlist/${playlistName}`]}>
        <SidebarProvider>
          <NowPlayingContextProvider>
            <Playlist />
          </NowPlayingContextProvider>
        </SidebarProvider>
      </MemoryRouter>,
    );
  });

  expect(component).toBeTruthy();

  // Wait for the unlike button to appear
  await waitFor(() => {
    const unlikeButton = component.container.querySelector(
      '#playlist-unlike-button',
    );
    expect(unlikeButton).toBeInTheDocument();
  });

  const unlikeButton = component.container.querySelector(
    '#playlist-unlike-button',
  );

  await act(async () => {
    fireEvent.click(unlikeButton!);
  });

  // Wait for the like button to appear after clicking unlike
  await waitFor(() => {
    const likeButton = component.container.querySelector(
      '#playlist-like-button',
    );
    expect(likeButton).toBeInTheDocument();
  });
});

test('Playlist user role update playlist', async () => {
  let currentPlaylistData = { ...playlistDTOMockFetch };

  global.fetch = jest.fn((url: string, options?: RequestInit) => {
    // Handle GET requests for playlist
    if (
      url.startsWith(`${Global.backendBaseUrl}/playlists/${playlistName}`) &&
      (!options || options.method === 'GET')
    ) {
      return Promise.resolve({
        json: () => currentPlaylistData,
        status: 200,
        ok: true,
        headers: getMockHeaders(),
      });
    }
    // Handle PUT request for updating playlist
    if (
      url.startsWith(`${Global.backendBaseUrl}/playlists/${playlistName}`) &&
      options?.method === 'PUT'
    ) {
      const urlObj = new URL(url);
      const params = new URLSearchParams(urlObj.search);
      const updatedData = {
        ...currentPlaylistData,
        name: params.get('new_name') || currentPlaylistData.name,
        description:
          params.get('description') || currentPlaylistData.description,
        photo: params.get('photo') || currentPlaylistData.photo,
      };
      currentPlaylistData = updatedData;
      return Promise.resolve({
        json: () => updatedData,
        status: 200,
        ok: true,
        headers: getMockHeaders(),
      });
    }
    // Handle GET request for song metadata
    if (url === `${Global.backendBaseUrl}/songs/metadata/${songName}`) {
      return Promise.resolve({
        json: () => ({
          ...songMockFetch,
          seconds_duration: 180, // Ensure number type
        }),
        status: 200,
        ok: true,
        headers: getMockHeaders(),
      });
    }
    // Handle GET request for liked playlists
    if (url === `${Global.backendBaseUrl}/playlists/liked`) {
      return Promise.resolve({
        json: () => [],
        status: 200,
        ok: true,
        headers: getMockHeaders(),
      });
    }
    // Handle GET request for user data
    if (url === `${Global.backendBaseUrl}/users/${userName}`) {
      return Promise.resolve({
        json: () => userMockFetch,
        status: 200,
        ok: true,
        headers: getMockHeaders(),
      });
    }
    // Handle POST request for liking playlist
    if (
      url ===
        `${Global.backendBaseUrl}/users/${userName}/saved_playlists/${playlistName}` &&
      options?.method === 'POST'
    ) {
      return Promise.resolve({
        json: () => ({ message: 'Playlist liked successfully' }),
        status: 200,
        ok: true,
        headers: getMockHeaders(),
      });
    }
    // Handle DELETE request for unliking playlist
    if (
      url ===
        `${Global.backendBaseUrl}/users/${userName}/saved_playlists/${playlistName}` &&
      options?.method === 'DELETE'
    ) {
      return Promise.resolve({
        json: () => ({ message: 'Playlist unliked successfully' }),
        status: 200,
        ok: true,
        headers: getMockHeaders(),
      });
    }
    return Promise.reject(new Error(`Unhandled URL in fetch mock: ${url}`));
  }) as jest.Mock;

  const component = await act(async () => {
    await new Promise((resolve) => setTimeout(resolve, 100)); // Wait for i18n
    return render(
      <MemoryRouter initialEntries={[`/playlist/${playlistName}`]}>
        <SidebarProvider>
          <NowPlayingContextProvider>
            <Playlist />
          </NowPlayingContextProvider>
        </SidebarProvider>
      </MemoryRouter>,
    );
  });

  expect(component).toBeTruthy();

  // Wait for the playlist name to appear
  await waitFor(
    () => {
      const playlistCardName = component.container.querySelector('h1');
      expect(playlistCardName).toBeInTheDocument();
      expect(playlistCardName?.textContent).toBe(playlistDTOMockFetch.name);
    },
    {
      timeout: 3000,
      interval: 100,
    },
  );

  // Find and click the update button
  const updateButton = component.container.querySelector('.wrapperThumbnail');
  expect(updateButton).toBeInTheDocument();

  await act(async () => {
    fireEvent.click(updateButton!);
  });

  // Wait for the modal to appear and check its content
  await waitFor(
    () => {
      const modalTitle = component.getByText(t('playlist.edit-details'));
      expect(modalTitle).toBeInTheDocument();
    },
    {
      timeout: 3000,
      interval: 100,
    },
  );

  // Find and fill the form fields
  const nameInput = component.getByLabelText(t('playlist.name'));
  const descriptionInput = component.getByLabelText(t('playlist.description'));
  const photoInput = component.getByLabelText(t('playlist.thumbnail'));

  await act(async () => {
    fireEvent.change(nameInput, { target: { value: 'Updated Playlist' } });
    fireEvent.change(descriptionInput, {
      target: { value: 'Updated Description' },
    });
    fireEvent.change(photoInput, {
      target: { value: 'https://example.com/photo.jpg' },
    });
  });

  // Find and click the save button
  const saveButton = component.getByText(t('playlist.save'));
  await act(async () => {
    fireEvent.click(saveButton);
  });

  // Wait for the modal to close and playlist to be updated
  await waitFor(
    () => {
      const modalTitle = component.queryByText(t('playlist.edit-details'));
      expect(modalTitle).not.toBeInTheDocument();
      const updatedPlaylistName = component.container.querySelector('h1');
      expect(updatedPlaylistName?.textContent).toBe('Updated Playlist');
    },
    {
      timeout: 3000,
      interval: 100,
    },
  );
});

test('Playlist owner should not see like buttons', async () => {
  global.fetch = jest.fn((url: string) => {
    if (url === `${Global.backendBaseUrl}/playlists/selected/${playlistName}`) {
      return Promise.resolve({
        json: () => [playlistDTOMockFetch],
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
      <MemoryRouter initialEntries={[`/playlist/${playlistName}`]}>
        <SidebarProvider>
          <NowPlayingContextProvider>
            <Playlist />
          </NowPlayingContextProvider>
        </SidebarProvider>
      </MemoryRouter>,
    );
  });

  expect(component).toBeTruthy();

  // Wait for the component to render and check that like buttons are not present
  await waitFor(() => {
    const likeButton = component.queryByTestId('playlist-like-button');
    const unlikeButton = component.queryByTestId('playlist-unlike-button');
    expect(likeButton).not.toBeInTheDocument();
    expect(unlikeButton).not.toBeInTheDocument();
  });
});
