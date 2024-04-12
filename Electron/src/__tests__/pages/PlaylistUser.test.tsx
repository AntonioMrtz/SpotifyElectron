import '@testing-library/jest-dom';
import { act, fireEvent, render } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import Playlist from 'pages/Playlist/Playlist';
import Token from 'utils/token';
import Global from 'global/global';
import { UserType } from 'utils/role';

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
  number_of_plays: 2,
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

jest.spyOn(Token, 'getTokenUsername').mockReturnValue(userName);
jest.spyOn(Token, 'getTokenRole').mockReturnValue(roleUser);

test('Playlist user role get all info', async () => {
  global.fetch = jest.fn((url: string) => {
    if (
      url === `${Global.backendBaseUrl}playlists/${playlistDTOMockFetch.name}`
    ) {
      return Promise.resolve({
        json: () => playlistDTOMockFetch,
        status: 200,
      }).catch((error) => {
        console.log(error);
      });
    }
    if (url === `${Global.backendBaseUrl}artistas/${artistMockFetch.name}`) {
      return Promise.resolve({
        json: () => artistMockFetch,
        status: 200,
      }).catch((error) => {
        console.log(error);
      });
    }
    if (url === `${Global.backendBaseUrl}canciones/dto/${songName}`) {
      return Promise.resolve({
        json: () => songMockFetch,
        status: 200,
      }).catch((error) => {
        console.log(error);
      });
    }
    if (url === `${Global.backendBaseUrl}usuarios/${userMockFetch.name}`) {
      return Promise.resolve({
        json: () => userMockFetch,
        status: 200,
      }).catch((error) => {
        console.log(error);
      });
    }

    // In case the URL doesn't match, return a rejected promise
    return Promise.reject(new Error('Unhandled URL in fetch mock'));
  }) as jest.Mock;

  const component = await act(() => {
    return render(
      <MemoryRouter initialEntries={[`/playlist/${playlistDTOMockFetch.name}`]}>
        <Routes>
          <Route
            path="/playlist/:id"
            element={
              <Playlist
                changeSongName={jest.fn()}
                triggerReloadSidebar={jest.fn()}
              />
            }
          />
        </Routes>
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
      url === `${Global.backendBaseUrl}playlists/${playlistDTOMockFetch.name}`
    ) {
      return Promise.resolve({
        json: () => playlistDTOMockFetch,
        status: 200,
      }).catch((error) => {
        console.log(error);
      });
    }
    if (url === `${Global.backendBaseUrl}artistas/${artistMockFetch.name}`) {
      return Promise.resolve({
        json: () => artistMockFetch,
        status: 200,
      }).catch((error) => {
        console.log(error);
      });
    }
    if (url === `${Global.backendBaseUrl}canciones/dto/${songName}`) {
      return Promise.resolve({
        json: () => songMockFetch,
        status: 200,
      }).catch((error) => {
        console.log(error);
      });
    }
    if (url === `${Global.backendBaseUrl}usuarios/${userMockFetch.name}`) {
      return Promise.resolve({
        json: () => userMockFetch,
        status: 200,
      }).catch((error) => {
        console.log(error);
      });
    }
    if (url === `${Global.backendBaseUrl}playlists/${playlistName}`) {
      return Promise.resolve({
        json: () => {},
        status: 204,
      }).catch((error) => {
        console.log(error);
      });
    }

    if (
      url ===
        `${Global.backendBaseUrl}usuarios/${userMockFetch.name}/playlists_guardadas?nombre_playlist=${playlistName}` &&
      options.method === 'PATCH'
    ) {
      return Promise.resolve({
        json: () => {},
        status: 204,
      }).catch((error) => {
        console.log(error);
      });
    }

    if (
      url ===
        `${Global.backendBaseUrl}usuarios/${userMockFetch.name}/playlists_guardadas?nombre_playlist=${playlistName}` &&
      options.method === 'DELETE'
    ) {
      return Promise.resolve({
        json: () => {},
        status: 202,
      }).catch((error) => {
        console.log(error);
      });
    }

    // In case the URL doesn't match, return a rejected promise
    return Promise.reject(new Error('Unhandled URL in fetch mock'));
  }) as jest.Mock;

  const component = await act(() => {
    return render(
      <MemoryRouter initialEntries={[`/playlist/${playlistDTOMockFetch.name}`]}>
        <Routes>
          <Route
            path="/playlist/:id"
            element={
              <Playlist
                changeSongName={jest.fn()}
                triggerReloadSidebar={jest.fn()}
              />
            }
          />
        </Routes>
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
      url === `${Global.backendBaseUrl}playlists/${playlistDTOMockFetch.name}`
    ) {
      return Promise.resolve({
        json: () => playlistDTOMockFetch,
        status: 200,
      }).catch((error) => {
        console.log(error);
      });
    }
    if (url === `${Global.backendBaseUrl}artistas/${artistMockFetch.name}`) {
      return Promise.resolve({
        json: () => artistMockFetch,
        status: 200,
      }).catch((error) => {
        console.log(error);
      });
    }
    if (url === `${Global.backendBaseUrl}canciones/dto/${songName}`) {
      return Promise.resolve({
        json: () => songMockFetch,
        status: 200,
      }).catch((error) => {
        console.log(error);
      });
    }
    if (url === `${Global.backendBaseUrl}usuarios/${userMockFetch.name}`) {
      return Promise.resolve({
        json: () => userMockFetch,
        status: 200,
      }).catch((error) => {
        console.log(error);
      });
    }
    if (url === `${Global.backendBaseUrl}playlists/${playlistName}`) {
      return Promise.resolve({
        json: () => {},
        status: 204,
      }).catch((error) => {
        console.log(error);
      });
    }

    if (
      url ===
        `${Global.backendBaseUrl}usuarios/${userMockFetch.name}/playlists_guardadas?nombre_playlist=${playlistName}` &&
      options.method === 'PATCH'
    ) {
      return Promise.resolve({
        json: () => {},
        status: 204,
      }).catch((error) => {
        console.log(error);
      });
    }

    if (
      url ===
        `${Global.backendBaseUrl}usuarios/${userMockFetch.name}/playlists_guardadas?nombre_playlist=${playlistName}` &&
      options.method === 'DELETE'
    ) {
      return Promise.resolve({
        json: () => {},
        status: 202,
      }).catch((error) => {
        console.log(error);
      });
    }

    // In case the URL doesn't match, return a rejected promise
    return Promise.reject(new Error('Unhandled URL in fetch mock'));
  }) as jest.Mock;

  const component = await act(() => {
    return render(
      <MemoryRouter initialEntries={[`/playlist/${playlistDTOMockFetch.name}`]}>
        <Routes>
          <Route
            path="/playlist/:id"
            element={
              <Playlist
                changeSongName={jest.fn()}
                triggerReloadSidebar={jest.fn()}
              />
            }
          />
        </Routes>
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
      url === `${Global.backendBaseUrl}playlists/${playlistDTOMockFetch.name}`
    ) {
      return Promise.resolve({
        json: () => playlistDTOMockFetch,
        status: 200,
      }).catch((error) => {
        console.log(error);
      });
    }
    if (url === `${Global.backendBaseUrl}artistas/${artistMockFetch.name}`) {
      return Promise.resolve({
        json: () => artistMockFetch,
        status: 200,
      }).catch((error) => {
        console.log(error);
      });
    }
    if (url === `${Global.backendBaseUrl}canciones/dto/${songName}`) {
      return Promise.resolve({
        json: () => songMockFetch,
        status: 200,
      }).catch((error) => {
        console.log(error);
      });
    }
    if (url === `${Global.backendBaseUrl}usuarios/${userMockFetch.name}`) {
      return Promise.resolve({
        json: () => userMockFetch,
        status: 200,
      }).catch((error) => {
        console.log(error);
      });
    }
    if (url === `${Global.backendBaseUrl}playlists/${playlistName}`) {
      return Promise.resolve({
        json: () => {},
        status: 204,
      }).catch((error) => {
        console.log(error);
      });
    }

    if (
      url ===
        `${Global.backendBaseUrl}usuarios/${userMockFetch.name}/playlists_guardadas?nombre_playlist=${playlistName}` &&
      options.method === 'PATCH'
    ) {
      return Promise.resolve({
        json: () => {},
        status: 204,
      }).catch((error) => {
        console.log(error);
      });
    }

    if (
      url ===
        `${Global.backendBaseUrl}usuarios/${userMockFetch.name}/playlists_guardadas?nombre_playlist=${playlistName}` &&
      options.method === 'DELETE'
    ) {
      return Promise.resolve({
        json: () => {},
        status: 202,
      }).catch((error) => {
        console.log(error);
      });
    }

    if (
      url ===
      `${Global.backendBaseUrl}playlists/${playlistName}?foto=&descripcion=descripcion`
    ) {
      return Promise.resolve({
        json: () => {},
        status: 204,
      }).catch((error) => {
        console.log(error);
      });
    }

    // In case the URL doesn't match, return a rejected promise
    return Promise.reject(new Error('Unhandled URL in fetch mock'));
  }) as jest.Mock;

  const triggerReloadSidebarMock = jest.fn();

  const component = await act(() => {
    return render(
      <MemoryRouter initialEntries={[`/playlist/${playlistDTOMockFetch.name}`]}>
        <Routes>
          <Route
            path="/playlist/:id"
            element={
              <Playlist
                changeSongName={jest.fn()}
                triggerReloadSidebar={triggerReloadSidebarMock}
              />
            }
          />
        </Routes>
      </MemoryRouter>,
    );
  });

  await act(async () => {
    const thumbnailPlaylist = component.getByAltText('thumbnail-playlist');
    if (thumbnailPlaylist) {
      fireEvent.click(thumbnailPlaylist);
    }
  });

  const inputName = component.getByPlaceholderText('Añade una descripción');

  fireEvent.change(inputName, {
    target: { value: 'descripcion' },
  });

  expect(component.queryByText('Editar información')).toBeInTheDocument();

  await act(async () => {
    const submitUpdateButton = component.queryByText('Guardar');
    if (submitUpdateButton) {
      fireEvent.click(submitUpdateButton);
    }
  });

  expect(triggerReloadSidebarMock).toHaveBeenCalledTimes(1); // Adjust the number based on your actual use case
});
