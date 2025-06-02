import '@testing-library/jest-dom';
import { act, fireEvent, render } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import Playlist from 'pages/Playlist/Playlist';
import Global from 'global/global';
import UserType from 'utils/role';
import getMockHeaders from 'utils/mockHeaders';
import * as TokenModule from 'utils/token';
import { NowPlayingContextProvider } from 'providers/NowPlayingProvider';
import { t } from 'i18next';

const userName = 'prueba';
const roleUser = UserType.USER;

const playlistName = 'playlisttest';
const songName = 'songName';

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
    if (url === `${Global.backendBaseUrl}/users/${userMockFetch.name}`) {
      return Promise.resolve({
        json: () => userMockFetch,
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
      <MemoryRouter initialEntries={[`/playlist/${playlistDTOMockFetch.name}`]}>
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
  expect(component).toBeTruthy();
  expect(component.container).toHaveTextContent(userName);
  expect(component.container).toHaveTextContent(playlistName);
  expect(component.container).toHaveTextContent(`0 h 3 min`);
  expect(component.container).toHaveTextContent(songMockFetch.name);
});

test('Playlist user role hit like button', async () => {
  const currentUser = 'differentUser';
  jest.spyOn(TokenModule, 'getTokenUsername').mockReturnValue(currentUser);

  const mockPlaylist: PlaylistDTO = {
    name: playlistName,
    photo: 'playlist',
    description: 'des',
    upload_date: 'date',
    owner: 'originalOwner',
    song_names: [songName],
  };

  const mockUser: UserMock = {
    name: currentUser,
    photo: 'photo',
    register_date: 'date',
    password: 'hashpassword',
    playback_history: [songName],
    playlists: [],
    saved_playlists: [],
  };

  global.fetch = jest.fn((url: string, options: any) => {
    if (url === `${Global.backendBaseUrl}/playlists/${mockPlaylist.name}`) {
      return Promise.resolve({
        json: () => mockPlaylist,
        status: 200,
        ok: true,
        headers: getMockHeaders(),
      });
    }
    if (url === `${Global.backendBaseUrl}/users/${currentUser}`) {
      return Promise.resolve({
        json: () => mockUser,
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
    if (url === `${Global.backendBaseUrl}/playlists/${playlistName}`) {
      return Promise.resolve({
        json: () => {},
        status: 204,
        ok: true,
        headers: getMockHeaders(),
      }).catch((error) => {
        console.log(error);
      });
    }

    if (
      url ===
        `${Global.backendBaseUrl}/users/${currentUser}/saved_playlists?playlist_name=${playlistName}` &&
      options.method === 'PATCH'
    ) {
      return Promise.resolve({
        json: () => {},
        status: 204,
        ok: true,
        headers: getMockHeaders(),
      }).catch((error) => {
        console.log(error);
      });
    }

    if (
      url ===
        `${Global.backendBaseUrl}/users/${currentUser}/saved_playlists?playlist_name=${playlistName}` &&
      options.method === 'DELETE'
    ) {
      return Promise.resolve({
        json: () => {},
        status: 202,
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
      <MemoryRouter initialEntries={[`/playlist/${mockPlaylist.name}`]}>
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

  // Wait for the component to load and state to update
  await act(async () => {
    await new Promise<void>((resolve) => {
      setTimeout(() => {
        resolve();
      }, 0);
    });
  });

  // First verify the like button is present
  const likeButton = component.container.querySelector('#playlist-like-button');
  expect(likeButton).toBeInTheDocument();

  // Click the like button
  await act(async () => {
    if (likeButton) {
      fireEvent.click(likeButton);
    }
  });

  // Wait for the state to update after clicking
  await act(async () => {
    await new Promise<void>((resolve) => {
      setTimeout(() => {
        resolve();
      }, 0);
    });
  });

  // Verify the unlike button is present after liking
  const unlikeButton = component.container.querySelector(
    '#playlist-unlike-button',
  );
  expect(unlikeButton).toBeInTheDocument();
});

test('Playlist user role get unlike button', async () => {
  const currentUser = 'differentUser';
  jest.spyOn(TokenModule, 'getTokenUsername').mockReturnValue(currentUser);

  const mockPlaylist: PlaylistDTO = {
    name: playlistName,
    photo: 'playlist',
    description: 'des',
    upload_date: 'date',
    owner: 'originalOwner',
    song_names: [songName],
  };

  const mockUser: UserMock = {
    name: currentUser,
    photo: 'photo',
    register_date: 'date',
    password: 'hashpassword',
    playback_history: [songName],
    playlists: [],
    saved_playlists: [playlistName],
  };

  global.fetch = jest.fn((url: string, options: any) => {
    if (url === `${Global.backendBaseUrl}/playlists/${mockPlaylist.name}`) {
      return Promise.resolve({
        json: () => mockPlaylist,
        status: 200,
        ok: true,
        headers: getMockHeaders(),
      });
    }
    if (url === `${Global.backendBaseUrl}/users/${currentUser}`) {
      return Promise.resolve({
        json: () => mockUser,
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
    if (url === `${Global.backendBaseUrl}/playlists/${playlistName}`) {
      return Promise.resolve({
        json: () => {},
        status: 204,
        ok: true,
        headers: getMockHeaders(),
      }).catch((error) => {
        console.log(error);
      });
    }

    if (
      url ===
        `${Global.backendBaseUrl}/users/${currentUser}/saved_playlists?playlist_name=${playlistName}` &&
      options.method === 'PATCH'
    ) {
      return Promise.resolve({
        json: () => {},
        status: 204,
        ok: true,
        headers: getMockHeaders(),
      }).catch((error) => {
        console.log(error);
      });
    }

    if (
      url ===
        `${Global.backendBaseUrl}/users/${currentUser}/saved_playlists?playlist_name=${playlistName}` &&
      options.method === 'DELETE'
    ) {
      return Promise.resolve({
        json: () => {},
        status: 202,
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
      <MemoryRouter initialEntries={[`/playlist/${mockPlaylist.name}`]}>
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

  // Wait for the component to load and state to update
  await act(async () => {
    await new Promise<void>((resolve) => {
      setTimeout(() => {
        resolve();
      }, 0);
    });
  });

  // First verify the unlike button is present (since playlist is already liked)
  const unlikeButton = component.container.querySelector(
    '#playlist-unlike-button',
  );
  expect(unlikeButton).toBeInTheDocument();

  // Click the unlike button
  await act(async () => {
    if (unlikeButton) {
      fireEvent.click(unlikeButton);
    }
  });

  // Wait for the state to update after clicking
  await act(async () => {
    await new Promise<void>((resolve) => {
      setTimeout(() => {
        resolve();
      }, 0);
    });
  });

  // Verify the like button is present after unliking
  const likeButton = component.container.querySelector('#playlist-like-button');
  expect(likeButton).toBeInTheDocument();
});

test('Playlist user role update playlist', async () => {
  // Mock a different user than the playlist owner
  const currentUser = 'differentUser';
  jest.spyOn(TokenModule, 'getTokenUsername').mockReturnValue(currentUser);

  // Mock playlist data with different owner
  const mockPlaylist: PlaylistDTO = {
    name: playlistName,
    photo: 'playlist',
    description: 'des',
    upload_date: 'date',
    owner: currentUser, // Set owner to be the current user
    song_names: [songName],
  };

  // Mock user data
  const mockUser: UserMock = {
    name: currentUser,
    photo: 'photo',
    register_date: 'date',
    password: 'hashpassword',
    playback_history: [songName],
    playlists: [],
    saved_playlists: [],
  };

  global.fetch = jest.fn((url: string) => {
    if (url === `${Global.backendBaseUrl}/playlists/${mockPlaylist.name}`) {
      return Promise.resolve({
        json: () => mockPlaylist,
        status: 200,
        ok: true,
        headers: getMockHeaders(),
      });
    }
    if (url === `${Global.backendBaseUrl}/users/${currentUser}`) {
      return Promise.resolve({
        json: () => mockUser,
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
    if (url === `${Global.backendBaseUrl}/playlists/${playlistName}`) {
      return Promise.resolve({
        json: () => {},
        status: 204,
        ok: true,
        headers: getMockHeaders(),
      });
    }
    if (
      url ===
      `${Global.backendBaseUrl}/playlists/${playlistName}?photo=&description=description`
    ) {
      return Promise.resolve({
        json: () => {},
        status: 204,
        ok: true,
        headers: getMockHeaders(),
      });
    }
    return Promise.reject(new Error(`Unhandled URL in fetch mock: ${url}`));
  }) as jest.Mock;

  const refreshSidebarData = jest.fn();

  const component = await act(() => {
    return render(
      <MemoryRouter initialEntries={[`/playlist/${mockPlaylist.name}`]}>
        <NowPlayingContextProvider>
          <Routes>
            <Route
              path="/playlist/:id"
              element={<Playlist refreshSidebarData={refreshSidebarData} />}
            />
          </Routes>
        </NowPlayingContextProvider>
      </MemoryRouter>,
    );
  });

  // Wait for the component to load
  await act(async () => {
    await new Promise<void>((resolve) => {
      setTimeout(() => {
        resolve();
      }, 0);
    });
  });

  // Click the thumbnail to open the edit modal
  await act(async () => {
    const thumbnailPlaylist = component.getByAltText('thumbnail-playlist');
    if (thumbnailPlaylist) {
      fireEvent.click(thumbnailPlaylist);
    }
  });

  // Wait for the modal to open
  await act(async () => {
    await new Promise<void>((resolve) => {
      setTimeout(() => {
        resolve();
      }, 0);
    });
  });

  // Find the description input using the correct placeholder text
  const inputDescription = component.getByPlaceholderText(
    t('playlist.description-placeholder'),
  );

  // Update the description
  await act(async () => {
    fireEvent.change(inputDescription, {
      target: { value: 'description' },
    });
  });

  // Verify the modal is open
  expect(component.queryByText(t('playlist.edit-details'))).toBeInTheDocument();

  // Click the save button
  await act(async () => {
    const submitUpdateButton = component.queryByText(t('playlist.save'));
    if (submitUpdateButton) {
      fireEvent.click(submitUpdateButton);
    }
  });

  // Verify the sidebar was refreshed
  expect(refreshSidebarData).toHaveBeenCalledTimes(1);
});

test('Playlist owner should not see like buttons', async () => {
  // Mock the playlist owner as the current user
  const ownerName = 'ownerUser';
  jest.spyOn(TokenModule, 'getTokenUsername').mockReturnValue(ownerName);

  const mockPlaylist: PlaylistDTO = {
    name: playlistName,
    photo: 'playlist',
    description: 'des',
    upload_date: 'date',
    owner: ownerName, // Set owner to be the same as current user
    song_names: [songName],
  };

  global.fetch = jest.fn((url: string) => {
    if (url === `${Global.backendBaseUrl}/playlists/${mockPlaylist.name}`) {
      return Promise.resolve({
        json: () => mockPlaylist,
        status: 200,
        ok: true,
        headers: getMockHeaders(),
      });
    }
    // ... other fetch mocks ...
    return Promise.reject(new Error(`Unhandled URL in fetch mock: ${url}`));
  }) as jest.Mock;

  const component = await act(() => {
    return render(
      <MemoryRouter initialEntries={[`/playlist/${mockPlaylist.name}`]}>
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

  // Verify that like buttons are not present
  const likeButton = component.container.querySelector('#playlist-like-button');
  const unlikeButton = component.container.querySelector(
    '#playlist-unlike-button',
  );
  expect(likeButton).not.toBeInTheDocument();
  expect(unlikeButton).not.toBeInTheDocument();
});
