import '@testing-library/jest-dom';
import { act, render } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import Playlist from 'pages/Playlist/Playlist';
import Token from 'utils/token';
import Global from 'global/global';
import { UserType } from 'utils/role';

const userName = 'prueba';
const roleArtist = UserType.ARTIST;

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
  duration: '180',
  genre: 'Rock',
  number_of_plays: 2,
};

jest.spyOn(Token, 'getTokenUsername').mockReturnValue(userName);
jest.spyOn(Token, 'getTokenRole').mockReturnValue(roleArtist);

test('Playlist artist role get all info', async () => {
  global.fetch = jest.fn((url: string) => {
    if (
      url ===
      `${Global.backendBaseUrl}playlists/dto/${playlistDTOMockFetch.name}`
    ) {
      return Promise.resolve({
        json: () => playlistDTOMockFetch,
        status: 200,
      }).catch((error) => {
        console.log(error);
      });
    }
    if (url === `${Global.backendBaseUrl}artistas/${userName}`) {
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
