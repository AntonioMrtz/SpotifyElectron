import '@testing-library/jest-dom';
import { act, render } from '@testing-library/react';
import * as router from 'react-router';
import '@testing-library/jest-dom/extend-expect';
import UserProfile from 'pages/UserProfile/UserProfile';
import UserType from 'utils/role';
import Global from 'global/global';
import { MemoryRouter, Route, Routes } from 'react-router-dom';

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

const artistMock = {
  photo: '',
  name: '',
  playlists: [],
  playback_history: [],
  uploaded_songs: [],
  play_count: [],
};

const userMock = {
  photo: '',
  name: '',
  playlists: [],
  playback_history: [],
};

test('render UserProfile with User', async () => {
  global.fetch = jest.fn(() =>
    Promise.resolve({
      json: () => Promise.resolve(userMock),
      status: 200,
    }),
  ) as jest.Mock;

  const component = await act(() => {
    return render(
      <UserProfile
        changeSongName={jest.fn()}
        refreshSidebarData={jest.fn()}
        userType={UserType.USER}
      />,
    );
  });

  expect(component).toBeTruthy();
});

test('render UserProfile with Artist', async () => {
  global.fetch = jest.fn(() =>
    Promise.resolve({
      json: () => Promise.resolve(artistMock),
      status: 200,
    }),
  ) as jest.Mock;

  const component = await act(() => {
    return render(
      <UserProfile
        changeSongName={jest.fn()}
        refreshSidebarData={jest.fn()}
        userType={UserType.USER}
      />,
    );
  });

  expect(component).toBeTruthy();
});

test('UserProfile User Fields', async () => {
  global.fetch = jest.fn(() =>
    Promise.resolve({
      json: () => Promise.resolve(userMock),
      status: 200,
    }),
  ) as jest.Mock;

  const component = await act(() => {
    return render(
      <UserProfile
        changeSongName={jest.fn()}
        refreshSidebarData={jest.fn()}
        userType={UserType.USER}
      />,
    );
  });

  expect(
    component.queryByText('Historial de reproducción'),
  ).toBeInTheDocument();

  expect(component.queryByText('Playlists del usuario')).toBeInTheDocument();
});

test('UserProfile Artist Fields', async () => {
  global.fetch = jest.fn(() =>
    Promise.resolve({
      json: () => Promise.resolve(artistMock),
      status: 200,
    }),
  ) as jest.Mock;

  const component = await act(() => {
    return render(
      <UserProfile
        changeSongName={jest.fn()}
        refreshSidebarData={jest.fn()}
        userType={UserType.ARTIST}
      />,
    );
  });

  expect(component.queryByText('Canciones del artista')).toBeInTheDocument();

  expect(component.queryByText('Playlists del usuario')).toBeInTheDocument();

  expect(component.queryByText('reproducciones totales')).toBeInTheDocument();
});

test('UserProfile User load Playback history and his Playlists', async () => {
  const playlistName = 'playlisttest';
  const songName = 'songName';

  const userMockFetch = {
    name: 'name',
    photo: 'photo',
    register_date: 'date',
    password: 'hashpassword',
    playback_history: [songName],
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
    number_of_plays: 2,
  };

  jest.mock('react-router-dom', () => ({
    ...jest.requireActual('react-router-dom'),
    useParams: () => ({
      id: userMockFetch.name,
    }),
  }));

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
    if (url === `${Global.backendBaseUrl}playlists/`) {
      return Promise.resolve({
        json: () => playlistDTOMockFetch,
        status: 200,
      }).catch((error) => {
        console.log(error);
      });
    }
    if (url === `${Global.backendBaseUrl}users/${userMockFetch.name}`) {
      return Promise.resolve({
        json: () => userMockFetch,
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

test('UserProfile Artist load Songs and Playcount', async () => {
  const playlistName = 'playlisttest';
  const songName = 'songName';
  const numPlayCount = 2;

  const artistMockFetch = {
    name: 'name',
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
    owner: 'owner',
    song_names: [songName],
  };

  const songMockFetch = {
    name: songName,
    artist: 'artist',
    photo: 'photo',
    seconds_duration: '3',
    genre: 'Rock',
    number_of_plays: 2,
  };

  jest.mock('react-router-dom', () => ({
    ...jest.requireActual('react-router-dom'),
    useParams: () => ({
      id: artistMockFetch.name,
    }),
  }));

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
    if (url === `${Global.backendBaseUrl}playlists/`) {
      return Promise.resolve({
        json: () => playlistDTOMockFetch,
        status: 200,
      }).catch((error) => {
        console.log(error);
      });
    }
    if (url === `${Global.backendBaseUrl}users/${artistMockFetch.name}`) {
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
    if (
      url ===
      `${Global.backendBaseUrl}artists/${artistMockFetch.name}/playbacks`
    ) {
      return Promise.resolve({
        json: () => ({
          play_count: numPlayCount,
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
    component.queryByText(`${numPlayCount} reproducciones totales`),
  ).toBeInTheDocument();
});
