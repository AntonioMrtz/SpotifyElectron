import '@testing-library/jest-dom';
import { act, fireEvent, render, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { BrowserRouter } from 'react-router-dom';
import Global from 'global/global';
import Home from 'pages/Home/Home';
import getMockHeaders from 'utils/mockHeaders';
import { SidebarProvider } from 'providers/SidebarProvider';
import { t } from 'i18next';

const playlistName = 'playlisttest';
const userName = 'prueba';

const playlistDTOMockFetch = {
  name: playlistName,
  photo: 'playlist',
  description: 'des',
  upload_date: 'date',
  owner: userName,
  song_names: [],
};

test('Home should display playlist', async () => {
  global.fetch = jest.fn((url: string) => {
    if (url === `${Global.backendBaseUrl}/playlists/`) {
      return Promise.resolve({
        json: () =>
          Promise.resolve({
            playlists: [playlistDTOMockFetch],
          }),
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
          <Home />
        </SidebarProvider>
      </BrowserRouter>,
    );
  });

  expect(component).toBeTruthy();

  // Wait for the playlist name to appear
  await waitFor(
    () => {
      const playlistCardName =
        component.container.querySelector('h5.tituloLista');
      expect(playlistCardName).toBeInTheDocument();
      expect(playlistCardName?.textContent).toBe(playlistDTOMockFetch.name);
    },
    {
      timeout: 3000,
      interval: 100,
    },
  );
});

test('Home should display section titles', async () => {
  global.fetch = jest.fn((url: string) => {
    if (url === `${Global.backendBaseUrl}/artists/`) {
      return Promise.resolve({
        json: () =>
          Promise.resolve({
            artists: [
              {
                name: 'name',
                photo: 'photo',
                register_date: 'date',
                password: 'pass',
                playback_history: [],
                playlists: [],
                saved_playlists: [],
              },
            ],
          }),
        status: 200,
        ok: true,
      }).catch((error) => {
        console.log(error);
      });
    }
    if (url === `${Global.backendBaseUrl}/playlists/`) {
      return Promise.resolve({
        json: () =>
          Promise.resolve({
            playlists: [
              JSON.stringify({
                name: 'name',
                photo: 'photo',
                description: 'description',
                upload_date: 'date',
                owner: 'owner',
                songs: [],
              }),
            ],
          }),
        status: 200,
        ok: true,
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
          <Home />
        </SidebarProvider>
      </BrowserRouter>,
    );
  });

  // Wait for the section titles to appear
  await waitFor(
    () => {
      expect(component.getByText(t('home.made-for'))).toBeInTheDocument();
      expect(component.getByText(t('home.top-artists'))).toBeInTheDocument();
    },
    {
      timeout: 3000,
      interval: 100,
    },
  );
});
