import '@testing-library/jest-dom';
import { act, render } from '@testing-library/react';
import * as router from 'react-router';
import '@testing-library/jest-dom/extend-expect';
import UserProfile from 'pages/UserProfile/UserProfile';
import { UserType } from 'utils/role';

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
    })
  ) as jest.Mock;

  const component = await act(() => {
    return render(
      <UserProfile
        changeSongName={jest.fn()}
        refreshSidebarData={jest.fn()}
        userType={UserType.USER}
      />
    );
  });

  expect(component).toBeTruthy();
});

test('render UserProfile with Artist', async () => {
  global.fetch = jest.fn(() =>
    Promise.resolve({
      json: () => Promise.resolve(artistMock),
      status: 200,
    })
  ) as jest.Mock;

  const component = await act(() => {
    return render(
      <UserProfile
        changeSongName={jest.fn()}
        refreshSidebarData={jest.fn()}
        userType={UserType.USER}
      />
    );
  });

  expect(component).toBeTruthy();
});

test('UserProfile User Fields', async () => {
  global.fetch = jest.fn(() =>
    Promise.resolve({
      json: () => Promise.resolve(userMock),
      status: 200,
    })
  ) as jest.Mock;

  const component = await act(() => {
    return render(
      <UserProfile
        changeSongName={jest.fn()}
        refreshSidebarData={jest.fn()}
        userType={UserType.USER}
      />
    );
  });

  expect(
    component.queryByText('Historial de reproducción')
  ).toBeInTheDocument();

  expect(component.queryByText('Playlists del usuario')).toBeInTheDocument();
});

test('UserProfile Artist Fields', async () => {
  global.fetch = jest.fn(() =>
    Promise.resolve({
      json: () => Promise.resolve(artistMock),
      status: 200,
    })
  ) as jest.Mock;

  const component = await act(() => {
    return render(
      <UserProfile
        changeSongName={jest.fn()}
        refreshSidebarData={jest.fn()}
        userType={UserType.ARTIST}
      />
    );
  });

  expect(component.queryByText('Canciones del artista')).toBeInTheDocument();

  expect(component.queryByText('Playlists del usuario')).toBeInTheDocument();

  expect(component.queryByText('reproducciones totales')).toBeInTheDocument();
});
