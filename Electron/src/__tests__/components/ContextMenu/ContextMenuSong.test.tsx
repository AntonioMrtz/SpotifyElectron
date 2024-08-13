import '@testing-library/jest-dom';
import '@testing-library/jest-dom/extend-expect';
import { act, fireEvent, render } from '@testing-library/react';
import ContextMenuSong from 'components/AdvancedUIComponents/ContextMenu/Song/ContextMenuSong';
import Global from 'global/global';
import UserType from 'utils/role';
import Token from 'utils/token';
import * as router from 'react-router';
import { BrowserRouter } from 'react-router-dom';

const playlistName = 'playlisttest';
const songName = 'songName';
const artistName = 'artistName';
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
jest.spyOn(Token, 'getTokenUsername').mockReturnValue(userName);
jest.spyOn(Token, 'getTokenRole').mockReturnValue(roleUser);

global.fetch = jest.fn((url: string, options: any) => {
  if (
    url === `${Global.backendBaseUrl}/playlists/${playlistDTOMockFetch.name}`
  ) {
    return Promise.resolve({
      json: () => playlistDTOMockFetch,
      status: 200,
      ok: true,
      headers: {
        get: (header: any) => {
          if (header.toLowerCase() === 'content-type') {
            return 'application/json';
          }
          return null;
        },
      },
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
      headers: {
        get: (header: any) => {
          if (header.toLowerCase() === 'content-type') {
            return 'application/json';
          }
          return null;
        },
      },
    }).catch((error) => {
      console.log(error);
    });
  }

  if (options.method === 'DELETE') {
    return Promise.resolve({
      json: () => artistMockFetch,
      status: 202,
      ok: true,
    }).catch((error) => {
      console.log(error);
    });
  }
  if (options.method === 'PUT') {
    return Promise.resolve({
      json: () => artistMockFetch,
      status: 204,
      ok: true,
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

  // In case the URL doesn't match, return a rejected promise
  return Promise.reject(new Error('Unhandled URL in fetch mock'));
}) as jest.Mock;

test('Render ContextMenuSong', async () => {
  const component = await act(() => {
    return render(
      <BrowserRouter>
        <ContextMenuSong
          playlistName={playlistName}
          songName={songName}
          artistName={artistName}
          handleCloseParent={jest.fn()}
          refreshPlaylistData={jest.fn()}
          refreshSidebarData={jest.fn()}
        />
      </BrowserRouter>,
    );
  });
  expect(component).toBeTruthy();
});

test('ContextMenuSong quitar de esta lista', async () => {
  const refreshPlaylistDataMock = jest.fn();

  const component = await act(() => {
    return render(
      <BrowserRouter>
        <ContextMenuSong
          playlistName={playlistName}
          songName={songName}
          artistName={artistName}
          handleCloseParent={jest.fn()}
          refreshPlaylistData={refreshPlaylistDataMock}
          refreshSidebarData={jest.fn()}
        />
      </BrowserRouter>,
    );
  });

  try {
    const quitarListaButton = component.getByText('Quitar de esta lista');

    await act(async () => {
      fireEvent.click(quitarListaButton);
    });

    expect(refreshPlaylistDataMock).toHaveBeenCalled();
  } catch (error) {
    // If an error occurs during rendering, fail the test
    // eslint-disable-next-line jest/no-conditional-expect
    expect(error).toBeUndefined();
  }
});

test('ContextMenuSong crear lista', async () => {
  const refreshSidebarMock = jest.fn();

  const component = await act(() => {
    return render(
      <BrowserRouter>
        <ContextMenuSong
          playlistName={playlistName}
          songName={songName}
          artistName={artistName}
          handleCloseParent={jest.fn()}
          refreshPlaylistData={jest.fn()}
          refreshSidebarData={refreshSidebarMock}
        />
      </BrowserRouter>,
    );
  });

  try {
    const addToListButton = component.getByText('Añadir a la playlist');

    await act(async () => {
      fireEvent.click(addToListButton);
    });

    const crearListaButton = component.getByText('Crear lista');

    await act(async () => {
      fireEvent.click(crearListaButton);
    });

    await act(async () => {
      fireEvent.click(addToListButton);
    });
    expect(refreshSidebarMock).toHaveBeenCalled();
  } catch (error) {
    // If an error occurs during rendering, fail the test
    // eslint-disable-next-line jest/no-conditional-expect
    expect(error).toBeUndefined();
  }
});

test('ContextMenuSong add to playlist', async () => {
  const component = await act(() => {
    return render(
      <BrowserRouter>
        <ContextMenuSong
          playlistName={playlistName}
          songName={songName}
          artistName={artistName}
          handleCloseParent={jest.fn()}
          refreshPlaylistData={jest.fn()}
          refreshSidebarData={jest.fn()}
        />
      </BrowserRouter>,
    );
  });

  try {
    const addToListButton = component.getByText('Añadir a la playlist');

    await act(async () => {
      fireEvent.click(addToListButton);
    });

    const playlistButton = component.getByText(playlistName);

    await act(async () => {
      fireEvent.click(playlistButton);
    });
  } catch (error) {
    // If an error occurs during rendering, fail the test
    // eslint-disable-next-line jest/no-conditional-expect
    expect(error).toBeUndefined();
  }
});
