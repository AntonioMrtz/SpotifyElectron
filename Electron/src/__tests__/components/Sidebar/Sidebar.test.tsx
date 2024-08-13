import '@testing-library/jest-dom';
import { act, render } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { BrowserRouter } from 'react-router-dom';
import Global from 'global/global';
import Sidebar from 'components/Sidebar/Sidebar';
import Token from 'utils/token';
import UserType from 'utils/role';

const playlistName = 'playlisttest';
const songName = 'songName';
const username = 'prueba';
const roleUser = UserType.ARTIST;

const artistMockFetch = {
  name: username,
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
  song_names: [],
};

jest.spyOn(Token, 'getTokenUsername').mockReturnValue(username);
jest.spyOn(Token, 'getTokenRole').mockReturnValue(roleUser);

test('render Sidebar', async () => {
  global.fetch = jest.fn(async (url: string) => {
    if (url === `${Global.backendBaseUrl}/artists/${artistMockFetch.name}`) {
      return Promise.resolve({
        json: () => artistMockFetch,
        status: 200,
        ok: true,
      }).catch((error) => {
        console.log(error);
      });
    }
    if (
      url === `${Global.backendBaseUrl}/users/${username}/relevant_playlists`
    ) {
      return Promise.resolve({
        json: () => Promise.resolve([playlistDTOMockFetch]),
        status: 200,
        ok: true,
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
        <Sidebar refreshSidebarData />
      </BrowserRouter>,
    );
  });

  expect(component).toBeTruthy();
});
