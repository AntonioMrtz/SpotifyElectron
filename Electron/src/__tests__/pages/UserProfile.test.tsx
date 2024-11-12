import '@testing-library/jest-dom';
import { act, render } from '@testing-library/react';
import * as router from 'react-router';
import '@testing-library/jest-dom/extend-expect';
import UserProfile from 'pages/UserProfile/UserProfile';
import UserType from 'utils/role';
import Global from 'global/global';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import getMockHeaders from 'utils/mockHeaders';

/* afterEach(() => {
  jest.clearAllMocks();
}); */

const navigate = jest.fn();

beforeEach(() => {
  jest.spyOn(router, 'useNavigate').mockImplementation(() => navigate);
});

/* jest.mock('react-router', () => ({
  ...jest.requireActual('react-router'),
  useNavigate: jest.fn(),
})); */

test('UserProfile User load Stream history and his Playlists', async () => {
  const playlistName = 'playlisttest';
  const songName = 'songName';

  const userMockFetch = {
    name: 'name',
    photo: 'photo',
    register_date: 'date',
    password: 'hashpassword',
    stream_history: [songName],
    playlists: [playlistName],
    saved_playlists: [playlistName],
  };

  const playlistDTOMockFetch = {
    name: playlistName,
    photo: 'playlist',
    description: 'des',
    upload_date: 'date',
    owner: 'owner',
    song_names: [songName],
  };

  const songMockFetch = {
    name: songName,
    artist: 'artist',
    photo: 'photo',
    seconds_duration: '3',
    genre: 'Rock',
    streams: 2,
  };

  jest.mock('react-router-dom', () => ({
    ...jest.requireActual('react-router-dom'),
    useParams: () => ({
      id: userMockFetch.name,
    }),
  }));

  global.fetch = jest.fn((url: string) => {
    if (
      url === `${Global.backendBaseUrl}/users/${userMockFetch.name}/playlists`
    ) {
      return Promise.resolve({
        json: () => [playlistDTOMockFetch],
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
    if (
      url ===
      `${Global.backendBaseUrl}/users/${userMockFetch.name}/stream_history`
    ) {
      return Promise.resolve({
        json: () => [songMockFetch],
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
      <MemoryRouter initialEntries={[`/user/${userMockFetch.name}`]}>
        <Routes>
          <Route
            path="/user/:id"
            element={
              <UserProfile
                refreshSidebarData={jest.fn()}
                changeSongName={jest.fn()}
                userType={UserType.USER}
              />
            }
          />
        </Routes>
      </MemoryRouter>,
    );
  });

  const elementsWithUserName = component.getAllByText(userMockFetch.name);

  expect(elementsWithUserName.length).toBeGreaterThan(0);

  expect(component.queryByText(songName)).toBeInTheDocument();
  expect(component.queryByText(playlistName)).toBeInTheDocument();
});

test('UserProfile Artist load Songs and total streams', async () => {
  const playlistName = 'playlisttest';
  const songName = 'songName';

  const artistMockFetch = {
    name: 'name',
    photo: 'photo',
    register_date: 'date',
    password: 'hashpassword',
    stream_history: [songName],
    playlists: [playlistName],
    saved_playlists: [playlistName],
    uploaded_songs: [songName],
    total_streams: 190,
  };

  const playlistDTOMockFetch = {
    name: playlistName,
    photo: 'playlist',
    description: 'des',
    upload_date: 'date',
    owner: 'owner',
    song_names: [songName],
  };

  const songMockFetch = {
    name: songName,
    artist: 'artist',
    photo: 'photo',
    seconds_duration: '3',
    genre: 'Rock',
    streams: artistMockFetch.total_streams,
  };

  jest.mock('react-router-dom', () => ({
    ...jest.requireActual('react-router-dom'),
    useParams: () => ({
      id: artistMockFetch.name,
    }),
  }));

  global.fetch = jest.fn((url: string) => {
    if (url === `${Global.backendBaseUrl}/users/${artistMockFetch.name}`) {
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
      url === `${Global.backendBaseUrl}/artists/${artistMockFetch.name}/songs`
    ) {
      return Promise.resolve({
        json: () => [songMockFetch],
        status: 200,
        ok: true,
        headers: getMockHeaders(),
      }).catch((error) => {
        console.log(error);
      });
    }
    if (
      url === `${Global.backendBaseUrl}/users/${artistMockFetch.name}/playlists`
    ) {
      return Promise.resolve({
        json: () => [playlistDTOMockFetch],
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
        <Routes>
          <Route
            path="/artist/:id"
            element={
              <UserProfile
                refreshSidebarData={jest.fn()}
                changeSongName={jest.fn()}
                userType={UserType.ARTIST}
              />
            }
          />
        </Routes>
      </MemoryRouter>,
    );
  });

  const elementsWithUserName = component.getAllByText(artistMockFetch.name);

  expect(elementsWithUserName.length).toBeGreaterThan(0);

  expect(component.queryByText(songName)).toBeInTheDocument();
  expect(component.queryByText(playlistName)).toBeInTheDocument();
  expect(
    component.queryByText(`${songMockFetch.streams} reproducciones totales`),
  ).toBeInTheDocument();
});
