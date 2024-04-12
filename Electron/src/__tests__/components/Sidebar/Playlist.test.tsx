import '@testing-library/jest-dom';
import { act, fireEvent, render } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { BrowserRouter } from 'react-router-dom';
import Global from 'global/global';
import Token from 'utils/token';
import { UserType } from 'utils/role';
import Playlist from 'components/Sidebar/Playlist/Playlist';

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

jest.spyOn(Token, 'getTokenUsername').mockReturnValue(userName);
jest.spyOn(Token, 'getTokenRole').mockReturnValue(roleUser);

test('render Sidebar Playlist', async () => {
  const handleUrlPlaylistClicked = () => jest.fn();
  const reloadSidebar = () => jest.fn();

  const component = await act(() => {
    return render(
      <BrowserRouter>
        <Playlist
          name={playlistDTOMockFetch.name}
          photo={playlistDTOMockFetch.photo}
          owner={artistMockFetch.name}
          playlistStyle=""
          handleUrlPlaylistClicked={handleUrlPlaylistClicked}
          reloadSidebar={reloadSidebar}
        />
      </BrowserRouter>,
    );
  });

  expect(component).toBeTruthy();
  expect(component.queryByText(playlistName)).toBeInTheDocument();
});

test('Sidebar Playlist handle open context menu', async () => {
  const handleUrlPlaylistClickedMock = jest.fn();
  const reloadSidebarMock = jest.fn();

  global.fetch = jest.fn(async (url: string) => {
    if (url === `${Global.backendBaseUrl}artistas/${artistMockFetch.name}`) {
      return Promise.resolve({
        json: () => artistMockFetch,
        status: 200,
      }).catch((error) => {
        console.log(error);
      });
    }
    if (url === `${Global.backendBaseUrl}playlists/multiple/${playlistName}`) {
      return Promise.resolve({
        json: () =>
          Promise.resolve({
            playlists: [playlistDTOMockFetch],
          }),
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
      <BrowserRouter>
        <Playlist
          name={playlistDTOMockFetch.name}
          photo={playlistDTOMockFetch.photo}
          owner={artistMockFetch.name}
          playlistStyle=""
          handleUrlPlaylistClicked={handleUrlPlaylistClickedMock}
          reloadSidebar={reloadSidebarMock}
        />
      </BrowserRouter>,
    );
  });

  const playlistItemClickable = component.getByTestId(
    'sidebar-playlist-wrapper',
  );

  await act(async () => {
    fireEvent.contextMenu(playlistItemClickable);
  });

  expect(component.getByText('Crear lista similar')).toBeInTheDocument();
});

test('Sidebar Playlist left-click', async () => {
  const handleUrlPlaylistClickedMock = jest.fn();
  const reloadSidebarMock = jest.fn();

  global.fetch = jest.fn(async (url: string) => {
    if (url === `${Global.backendBaseUrl}artistas/${artistMockFetch.name}`) {
      return Promise.resolve({
        json: () => artistMockFetch,
        status: 200,
      }).catch((error) => {
        console.log(error);
      });
    }
    if (url === `${Global.backendBaseUrl}playlists/multiple/${playlistName}`) {
      return Promise.resolve({
        json: () =>
          Promise.resolve({
            playlists: [playlistDTOMockFetch],
          }),
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
      <BrowserRouter>
        <Playlist
          name={playlistDTOMockFetch.name}
          photo={playlistDTOMockFetch.photo}
          owner={artistMockFetch.name}
          playlistStyle=""
          handleUrlPlaylistClicked={handleUrlPlaylistClickedMock}
          reloadSidebar={reloadSidebarMock}
        />
      </BrowserRouter>,
    );
  });

  const playlistItemClickable = component.getByTestId(
    'sidebar-playlist-wrapper',
  );

  await act(async () => {
    fireEvent.click(playlistItemClickable);
  });

  expect(handleUrlPlaylistClickedMock).toHaveBeenCalledWith(playlistName);
});
