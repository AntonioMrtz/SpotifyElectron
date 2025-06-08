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
  recently_played: [songName],
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
  recently_played: [songName],
  playlists: [playlistName],
  saved_playlists: [playlistName],
};

jest.spyOn(TokenModule, 'getTokenUsername').mockReturnValue(userName);
jest.spyOn(TokenModule, 'getTokenRole').mockReturnValue(roleUser);

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
        `${Global.backendBaseUrl}/users/${userMockFetch.name}/saved_playlists?playlist_name=${playlistName}` &&
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
        `${Global.backendBaseUrl}/users/${userMockFetch.name}/saved_playlists?playlist_name=${playlistName}` &&
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

  await act(async () => {
    const likeButton = component.container.querySelector(
      '#playlist-like-button',
    );
    if (likeButton) {
      fireEvent.click(likeButton);
    }
  });

  const unlikeButton = component.container.querySelector(
    '#playlist-unlike-button',
  );
  expect(unlikeButton).toBeInTheDocument();
});

test('Playlist user role get unlike button', async () => {
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
        `${Global.backendBaseUrl}/users/${userMockFetch.name}/saved_playlists?playlist_name=${playlistName}` &&
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
        `${Global.backendBaseUrl}/users/${userMockFetch.name}/saved_playlists?playlist_name=${playlistName}` &&
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

  await act(async () => {
    const unlikeButton = component.container.querySelector(
      '#playlist-unlike-button',
    );
    if (unlikeButton) {
      fireEvent.click(unlikeButton);
    }
  });

  const likeButton = component.container.querySelector('#playlist-like-button');
  expect(likeButton).toBeInTheDocument();
});

test('Playlist user role update playlist', async () => {
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
    if (url === `${Global.backendBaseUrl}/playlists/${playlistName}`) {
      return Promise.resolve({
        json: () => {},
        status: 204,
        ok: true,
        headers: getMockHeaders(),
      }).catch((error) => {
        console.log(`${error}`);
      });
    }

    if (
      url ===
        `${Global.backendBaseUrl}/users/${userMockFetch.name}/saved_playlists?playlist_name=${playlistName}` &&
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
        `${Global.backendBaseUrl}/users/${userMockFetch.name}/saved_playlists?playlist_name=${playlistName}` &&
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

    if (
      url ===
      `${Global.backendBaseUrl}/playlists/${playlistName}?photo=&description=description`
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
    return Promise.reject(new Error(`Unhandled URL in fetch mock: ${url}`));
  }) as jest.Mock;

  const refreshSidebarData = jest.fn();

  const component = await act(() => {
    return render(
      <MemoryRouter initialEntries={[`/playlist/${playlistDTOMockFetch.name}`]}>
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

  await act(async () => {
    const thumbnailPlaylist = component.getByAltText('thumbnail-playlist');
    if (thumbnailPlaylist) {
      fireEvent.click(thumbnailPlaylist);
    }
  });

  const inputName = component.getByPlaceholderText(
    t('playlist.description-placeholder'),
  );

  await act(async () => {
    fireEvent.change(inputName, {
      target: { value: 'description' },
    });
  });

  expect(component.queryByText(t('playlist.edit-details'))).toBeInTheDocument();

  await act(async () => {
    const submitUpdateButton = component.queryByText(t('playlist.save'));
    if (submitUpdateButton) {
      fireEvent.click(submitUpdateButton);
    }
  });

  expect(refreshSidebarData).toHaveBeenCalledTimes(1);
});
