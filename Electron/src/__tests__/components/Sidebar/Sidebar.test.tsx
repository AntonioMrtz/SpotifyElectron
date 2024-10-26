import '@testing-library/jest-dom';
import { act, render } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { BrowserRouter } from 'react-router-dom';
import Global from 'global/global';
import Sidebar from 'components/Sidebar/Sidebar';
import UserType from 'utils/role';
import getMockHeaders from 'utils/mockHeaders';
import * as TokenModule from 'utils/token';
import { SidebarProvider } from 'components/Sidebar/SidebarContext'; // Adjust the path as necessary

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
  owner: 'owner',
  song_names: [],
};

// Mocking Token Module
jest.spyOn(TokenModule, 'getTokenUsername').mockReturnValue(userName);
jest.spyOn(TokenModule, 'getTokenRole').mockReturnValue(roleUser);

test('render Sidebar', async () => {
  global.fetch = jest.fn(async (url: string) => {
    if (url === `${Global.backendBaseUrl}/artists/${artistMockFetch.name}`) {
      return Promise.resolve({
        json: () => artistMockFetch,
        status: 200,
        ok: true,
        headers: getMockHeaders(),
      });
    }
    if (
      url === `${Global.backendBaseUrl}/users/${userName}/relevant_playlists`
    ) {
      return Promise.resolve({
        json: () => Promise.resolve([playlistDTOMockFetch]),
        status: 200,
        ok: true,
        headers: getMockHeaders(),
      });
    }

    // In case the URL doesn't match, return a rejected promise
    return Promise.reject(new Error(`Unhandled URL in fetch mock: ${url}`));
  }) as jest.Mock;

  const component = await act(() => {
    return render(
      <BrowserRouter>
        <SidebarProvider>
          {' '}
          {/* Wrap Sidebar in SidebarProvider */}
          <Sidebar />
        </SidebarProvider>
      </BrowserRouter>,
    );
  });

  expect(component).toBeTruthy();
});
