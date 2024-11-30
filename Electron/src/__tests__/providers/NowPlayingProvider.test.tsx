import '@testing-library/jest-dom';
import { act, fireEvent, render, screen } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import Playlist from 'pages/Playlist/Playlist';
import Global from 'global/global';
import UserType from 'utils/role';
import getMockHeaders from 'utils/mockHeaders';
import * as TokenModule from 'utils/token';
import { NowPlayingContextProvider } from 'providers/NowPlayingProvider';
import Footer from 'components/footer/Footer';

const userName = 'prueba';
const roleUser = UserType.USER;

const playlistName = 'playlisttest';
const songName = 'songName';

const artistMockFetch = {
  name: userName,
  photo: 'photo',
  register_date: 'date',
  password: 'hashpassword',
  stream_history: [songName],
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
  stream_history: [songName],
  playlists: [playlistName],
  saved_playlists: [playlistName],
};

jest.spyOn(TokenModule, 'getTokenUsername').mockReturnValue(userName);
jest.spyOn(TokenModule, 'getTokenRole').mockReturnValue(roleUser);

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
      `${Global.backendBaseUrl}/users/${userMockFetch.name}/stream_history`
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
    if (url === `${Global.backendBaseUrl}/songs/${songMockFetch.name}`) {
      return Promise.resolve({
        json: () => songMockFetch,
        status: 200,
        ok: true,
        headers: getMockHeaders(),
      }).catch((error) => {
        console.log(error);
      });
    }
    if (
      url === `${Global.backendBaseUrl}/songs/metadata/${songMockFetch.name}`
    ) {
      return Promise.resolve({
        json: () => songMockFetch,
        status: 200,
        ok: true,
        headers: getMockHeaders(),
      }).catch((error) => {
        console.log(error);
      });
    }
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
    if (url === `${Global.backendBaseUrl}/songs/${songName}/streams`) {
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
      `${Global.backendBaseUrl}/users/${userName}/stream_history?song_name=${songName}`
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

  jest
    .spyOn(window.HTMLMediaElement.prototype, 'play')
    .mockImplementation(jest.fn());

  jest
    .spyOn(window.HTMLMediaElement.prototype, 'pause')
    .mockImplementation(jest.fn());
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
          <Footer />
        </NowPlayingContextProvider>
      </MemoryRouter>,
    );
  });

  const songCard = await screen.getByText(`${songMockFetch.name}`);
  await act(async () => {
    fireEvent.dblClick(songCard);
  });

  const songInfoButton = await component.findByTestId('songinfo-name');
  expect(songInfoButton).toHaveTextContent(songMockFetch.name);
});
