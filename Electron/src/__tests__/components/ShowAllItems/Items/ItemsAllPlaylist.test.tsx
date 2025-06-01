import '@testing-library/jest-dom';
import { render } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Global from 'global/global';
import ItemsAllPlaylists from 'components/ShowAllItems/Items/ItemsAllPlaylists';
import getMockHeaders from 'utils/mockHeaders';
import { act } from 'react';

const playlistName = 'playlisttest';

const playlistDTOMockFetch = {
  name: playlistName,
  photo: 'playlist',
  description: 'des',
  upload_date: 'date',
  owner: 'owner',
  song_names: [],
};

test('Render itemsAllPlaylist', async () => {
  global.fetch = jest.fn((url: string) => {
    if (url === `${Global.backendBaseUrl}/playlists/`) {
      return Promise.resolve({
        json: () =>
          Promise.resolve({
            playlists: [
              {
                name: playlistName,
                photo: 'photo',
                description: 'description',
                upload_date: 'date',
                owner: 'owner',
                songs: [],
              },
            ],
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
  const component = await act(() => {
    return render(
      <BrowserRouter>
        <ItemsAllPlaylists
          refreshSidebarData={jest.fn()}
          id={playlistDTOMockFetch.name}
        />
      </BrowserRouter>,
    );
  });

  expect(component).toBeTruthy();

  const playlistCardName = component.queryByText(playlistDTOMockFetch.name);

  expect(playlistCardName).toBeInTheDocument();
});
