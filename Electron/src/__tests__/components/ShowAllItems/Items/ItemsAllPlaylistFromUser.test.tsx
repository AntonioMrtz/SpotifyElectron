import '@testing-library/jest-dom';
import { act, fireEvent, render, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { BrowserRouter } from 'react-router-dom';
import Global from 'global/global';
import ItemsAllPlaylistsFromUser from 'components/ShowAllItems/Items/ItemsAllPlaylistFromUser';
import getMockHeaders from 'utils/mockHeaders';
import { SidebarProvider } from 'providers/SidebarProvider';

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

test('Render itemsAllPlaylistFromUser', async () => {
  global.fetch = jest.fn((url: string) => {
    if (url === `${Global.backendBaseUrl}/users/${userName}/playlists`) {
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

  const component = await act(async () => {
    return render(
      <BrowserRouter>
        <SidebarProvider>
          <ItemsAllPlaylistsFromUser
            userName={userName}
            refreshSidebarData={jest.fn()}
            id={userName}
          />
        </SidebarProvider>
      </BrowserRouter>,
    );
  });

  expect(component).toBeTruthy();

  // Wait for the playlist name to appear in the document
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
