import '@testing-library/jest-dom';
import { act, render } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import Playlist from 'pages/Playlist/Playlist';
import Global from 'global/global';
import UserType from 'utils/role';
import getMockHeaders from 'utils/mockHeaders';

import * as TokenModule from 'utils/token';
import { NowPlayingContextProvider } from 'providers/NowPlayingProvider';

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
  seconds_duration: '180',
  genre: 'Rock',
  streams: 2,
};

jest.spyOn(TokenModule, 'getTokenUsername').mockReturnValue(userName);
jest.spyOn(TokenModule, 'getTokenRole').mockReturnValue(roleArtist);

test('Playlist artist role get all info', async () => {
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
    if (url === `${Global.backendBaseUrl}/artists/${userName}`) {
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
