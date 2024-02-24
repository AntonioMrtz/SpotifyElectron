import '@testing-library/jest-dom';
import '@testing-library/jest-dom/extend-expect';
import { act, fireEvent, render } from '@testing-library/react';
import ContextMenuSong from 'components/AdvancedUIComponents/ContextMenu/Song/ContextMenuSong';
import Global from 'global/global';
import { UserType } from 'utils/role';
import Token from 'utils/token';

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

/* const songMockFetch = {
  name: songName,
  artist: userName,
  photo: 'photo',
  duration: '180',
  genre: 'Rock',
  number_of_plays: 2,
}; */

jest.spyOn(Token, 'getTokenUsername').mockReturnValue(userName);
jest.spyOn(Token, 'getTokenRole').mockReturnValue(roleUser);

global.fetch = jest.fn((url: string, options: any) => {
  if (
    url === `${Global.backendBaseUrl}playlists/dto/${playlistDTOMockFetch.name}`
  ) {
    return Promise.resolve({
      json: () => playlistDTOMockFetch,
      status: 200,
    }).catch((error) => {
      console.log(error);
    });
  }
  if (url === `${Global.backendBaseUrl}playlists/multiple/${playlistName}`) {
    return Promise.resolve({
      json: () =>
        Promise.resolve({
          playlists: [JSON.stringify(playlistDTOMockFetch)],
        }),
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

  if (options.method === 'DELETE') {
    return Promise.resolve({
      json: () => artistMockFetch,
      status: 202,
    }).catch((error) => {
      console.log(error);
    });
  }
  if (options.method === 'PUT') {
    return Promise.resolve({
      json: () => artistMockFetch,
      status: 204,
    }).catch((error) => {
      console.log(error);
    });
  }

  if (options.method === 'POST') {
    return Promise.resolve({
      json: () => artistMockFetch,
      status: 201,
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
      <ContextMenuSong
        playlistName={playlistName}
        songName={songName}
        handleCloseParent={jest.fn()}
        refreshPlaylistData={jest.fn()}
        refreshSidebarData={jest.fn()}
      />,
    );
  });
  expect(component).toBeTruthy();
});

test('ContextMenuSong quitar de esta lista', async () => {
  const refreshPlaylistDataMock = jest.fn();

  const component = await act(() => {
    return render(
      <ContextMenuSong
        playlistName={playlistName}
        songName={songName}
        handleCloseParent={jest.fn()}
        refreshPlaylistData={refreshPlaylistDataMock}
        refreshSidebarData={jest.fn()}
      />,
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
      <ContextMenuSong
        playlistName={playlistName}
        songName={songName}
        handleCloseParent={jest.fn()}
        refreshPlaylistData={jest.fn()}
        refreshSidebarData={refreshSidebarMock}
      />,
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
      <ContextMenuSong
        playlistName={playlistName}
        songName={songName}
        handleCloseParent={jest.fn()}
        refreshPlaylistData={jest.fn()}
        refreshSidebarData={jest.fn()}
      />,
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
