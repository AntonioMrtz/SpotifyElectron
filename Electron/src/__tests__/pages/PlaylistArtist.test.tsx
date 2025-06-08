import '@testing-library/jest-dom';
import { act, render, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { MemoryRouter } from 'react-router-dom';
import Global from 'global/global';
import Playlist from 'pages/Playlist/Playlist';
import getMockHeaders from 'utils/mockHeaders';
import { SidebarProvider } from 'providers/SidebarProvider';
import { NowPlayingContextProvider } from 'providers/NowPlayingProvider';
import UserType from 'utils/role';
import * as TokenModule from 'utils/token';
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

// Initialize i18next for testing
i18n.use(initReactI18next).init({
  lng: 'en',
  fallbackLng: 'en',
  ns: ['playlist', 'common'],
  defaultNS: 'playlist',
  resources: {
    en: {
      playlist: {
        'edit-details': 'Edit details',
        name: 'Name',
        description: 'Description',
        thumbnail: 'Thumbnail',
        save: 'Save',
        title: 'Title',
        songs: 'songs',
        plays: 'Plays',
      },
      common: {
        album: 'Album',
        playlist: 'Playlist',
      },
    },
  },
  interpolation: {
    escapeValue: false,
  },
});

// Wait for i18next to be ready
beforeAll(async () => {
  await i18n.isInitialized;
});

const playlistName = 'playlisttest';
const userName = 'prueba';
const songName = 'songName';
const roleUser = UserType.USER;

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
  seconds_duration: 180, // Changed to number to match expected type
  genre: 'Rock',
  streams: 2,
};

jest.spyOn(TokenModule, 'getTokenUsername').mockReturnValue(userName);
jest.spyOn(TokenModule, 'getTokenRole').mockReturnValue(roleUser);

test('Playlist user role get all info', async () => {
  global.fetch = jest.fn((url: string) => {
    if (url === `${Global.backendBaseUrl}/playlists/${playlistName}`) {
      return Promise.resolve({
        json: () => playlistDTOMockFetch,
        status: 200,
        ok: true,
        headers: getMockHeaders(),
      });
    }
    if (url === `${Global.backendBaseUrl}/songs/metadata/${songName}`) {
      return Promise.resolve({
        json: () => songMockFetch,
        status: 200,
        ok: true,
        headers: getMockHeaders(),
      });
    }
    if (url === `${Global.backendBaseUrl}/playlists/liked`) {
      return Promise.resolve({
        json: () => [],
        status: 200,
        ok: true,
        headers: getMockHeaders(),
      });
    }
    return Promise.reject(new Error(`Unhandled URL in fetch mock: ${url}`));
  }) as jest.Mock;

  const component = await act(async () => {
    return render(
      <MemoryRouter initialEntries={[`/playlist/${playlistName}`]}>
        <SidebarProvider>
          <NowPlayingContextProvider>
            <Playlist />
          </NowPlayingContextProvider>
        </SidebarProvider>
      </MemoryRouter>,
    );
  });

  expect(component).toBeTruthy();

  // Wait for the playlist name to appear
  await waitFor(
    () => {
      const playlistCardName = component.container.querySelector('h1');
      expect(playlistCardName).toBeInTheDocument();
      expect(playlistCardName?.textContent).toBe(playlistDTOMockFetch.name);
    },
    {
      timeout: 3000,
      interval: 100,
    },
  );

  // Wait for the song name to appear in the song list
  await waitFor(
    () => {
      const songNameElement = component.container.querySelector(
        '.songTitleTable.titleContainer',
      );
      expect(songNameElement).toBeInTheDocument();
      expect(songNameElement?.textContent).toBe(songMockFetch.name);
    },
    {
      timeout: 3000,
      interval: 100,
    },
  );
}, 10000); // Increase test timeout to 10 seconds
