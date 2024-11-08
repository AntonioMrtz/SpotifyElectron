import '@testing-library/jest-dom';
import { act, fireEvent, render, screen } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import Playlist from 'pages/Playlist/Playlist';
import Global from 'global/global';
import UserType from 'utils/role';
import getMockHeaders from 'utils/mockHeaders';
import * as TokenModule from 'utils/token';
import { SongNameChangeContextProvider } from 'hooks/useSongChangeContextApi';
import Footer from 'components/footer/Footer';
import UserProfile from 'pages/UserProfile/UserProfile';

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
        <SongNameChangeContextProvider>
          <Routes>
            <Route
              path="/playlist/:id"
              element={<Playlist refreshSidebarData={jest.fn()} />}
            />
          </Routes>
        </SongNameChangeContextProvider>
      </MemoryRouter>,
    );
  });
  expect(component).toBeTruthy();
  expect(component.container).toHaveTextContent(userName);
  expect(component.container).toHaveTextContent(playlistName);
  expect(component.container).toHaveTextContent(`0 h 3 min aproximadamente`);
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
        <SongNameChangeContextProvider>
          <Routes>
            <Route
              path="/playlist/:id"
              element={<Playlist refreshSidebarData={jest.fn()} />}
            />
          </Routes>
        </SongNameChangeContextProvider>
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
  expect(unlikeButton).toBeVisible();
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
        <SongNameChangeContextProvider>
          <Routes>
            <Route
              path="/playlist/:id"
              element={<Playlist refreshSidebarData={jest.fn()} />}
            />
          </Routes>
        </SongNameChangeContextProvider>
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
  expect(likeButton).toBeVisible();
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

    // In case the URL doesn't match, return a rejected promise
    return Promise.reject(new Error(`Unhandled URL in fetch mock: ${url}`));
  }) as jest.Mock;

  const refreshSidebarData = jest.fn();

  const component = await act(() => {
    return render(
      <MemoryRouter initialEntries={[`/playlist/${playlistDTOMockFetch.name}`]}>
        <SongNameChangeContextProvider>
          <Routes>
            <Route
              path="/playlist/:id"
              element={<Playlist refreshSidebarData={refreshSidebarData} />}
            />
          </Routes>
        </SongNameChangeContextProvider>
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
    'Añade opcionalmente una descripción',
  );

  await act(async () => {
    fireEvent.change(inputName, {
      target: { value: 'description' },
    });
  });

  expect(component.queryByText('Editar información')).toBeInTheDocument();

  await act(async () => {
    const submitUpdateButton = component.queryByText('Guardar');
    if (submitUpdateButton) {
      fireEvent.click(submitUpdateButton);
    }
  });

  expect(refreshSidebarData).toHaveBeenCalledTimes(1);
});

test('Playlist updates song name in context when a song is clicked', async () => {
  global.fetch = jest.fn((url: string) => {
    if (
      url === `${Global.backendBaseUrl}/artists/${artistMockFetch.name}/songs`
    ) {
      return Promise.resolve({
        json: () => artistMockFetch,
        status: 200,
        ok: true,
        headers: getMockHeaders(),
      }).catch((error) => {
        console.log(error);
      });
    }
    if (
      url ===
      `${Global.backendBaseUrl}/users/${userMockFetch.name}/playback_history`
    ) {
      return Promise.resolve({
        json: () => userMockFetch,
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
      <MemoryRouter initialEntries={[`/artist/${artistMockFetch.name}`]}>
        <SongNameChangeContextProvider>
          <Routes>
            <Route
              path="/artist/:id"
              element={
                <UserProfile
                  refreshSidebarData={jest.fn()}
                  userType={UserType.ARTIST}
                />
              }
            />
          </Routes>
          <Footer />
        </SongNameChangeContextProvider>
      </MemoryRouter>,
    );
  });

  const songCard = await screen.findByTestId(`song-card-${songMockFetch.name}`);
  await act(async () => {
    fireEvent.dblClick(songCard);
  });

  const songInfoButton = await component.findByTestId('songinfo-name');
  expect(songInfoButton).toHaveTextContent(songMockFetch.name);
});
