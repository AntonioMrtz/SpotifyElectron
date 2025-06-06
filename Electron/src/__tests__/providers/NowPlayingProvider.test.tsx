import '@testing-library/jest-dom';
import { act, fireEvent, render, screen } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { BrowserRouter, MemoryRouter, Route, Routes } from 'react-router-dom';
import Playlist from 'pages/Playlist/Playlist';
import Global from 'global/global';
import UserType from 'utils/role';
import getMockHeaders from 'utils/mockHeaders';
import * as TokenModule from 'utils/token';
import { NowPlayingContextProvider } from 'providers/NowPlayingProvider';
import Footer from 'components/footer/Footer';
import { useNowPlayingContext } from 'hooks/useNowPlayingContext';
import { SidebarProvider } from 'providers/SidebarProvider';

const userName = 'prueba';
const roleUser = UserType.USER;

const playlistName = 'playlisttest';
const songName = 'songName';
const artistName = 'artistName';
const songPhoto = 'songPhoto';
const songDuration = '180';

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

const songDTOMockFetch = {
  name: songName,
  artist: artistName,
  photo: songPhoto,
  seconds_duration: songDuration,
  genre: 'Rock',
  streams: 2,
};

const userMockFetch = {
  name: userName,
  photo: 'photo',
  register_date: 'date',
  password: 'hashpassword',
  playback_history: [songName],
  playlists: [playlistName],
  saved_playlists: [playlistName],
};

jest.spyOn(TokenModule, 'getTokenUsername').mockReturnValue(userName);
jest.spyOn(TokenModule, 'getTokenRole').mockReturnValue(roleUser);

function TestComponent() {
  const { songName: currentSongName, changeSongName } = useNowPlayingContext();
  return (
    <div>
      <div data-testid="now-playing-name">{currentSongName}</div>
      <button
        data-testid="change-song-button"
        onClick={() => changeSongName(songName)}
      >
        Change Song
      </button>
    </div>
  );
}

test('Playlist updates song name in context when a song is clicked', async () => {
  global.fetch = jest.fn((url: string) => {
    if (url === `${Global.backendBaseUrl}/songs/metadata/${songName}`) {
      return Promise.resolve({
        json: () => songDTOMockFetch,
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

  const component = await act(async () => {
    return render(
      <BrowserRouter>
        <SidebarProvider>
          <NowPlayingContextProvider>
            <TestComponent />
          </NowPlayingContextProvider>
        </SidebarProvider>
      </BrowserRouter>,
    );
  });

  expect(component).toBeTruthy();

  // Initially, no song should be playing
  const nowPlayingName = component.getByTestId('now-playing-name');
  expect(nowPlayingName).toHaveTextContent(Global.noSongPlaying);

  // Click the button to change the song
  const changeSongButton = component.getByTestId('change-song-button');
  await act(async () => {
    fireEvent.click(changeSongButton);
  });

  // After clicking, the song name should be updated
  expect(nowPlayingName).toHaveTextContent(songName);
});
