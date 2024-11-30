import '@testing-library/jest-dom';
import { act, render } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { BrowserRouter } from 'react-router-dom';
import Global from 'global/global';
import ItemsAllPlaylistsFromUser from 'components/ShowAllItems/Items/ItemsAllPlaylistFromUser';
import getMockHeaders from 'utils/mockHeaders';

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
};

const playlistDTOMockFetch = {
  name: playlistName,
  photo: 'playlist',
  description: 'des',
  upload_date: 'date',
  owner: 'owner',
  song_names: [],
};

test('Render itemsAllPlaylistFromUser', async () => {
  global.fetch = jest.fn(async (url: string) => {
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
      url === `${Global.backendBaseUrl}/users/${artistMockFetch.name}/playlists`
    ) {
      return Promise.resolve({
        json: () => Promise.resolve([playlistDTOMockFetch]),
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
        <ItemsAllPlaylistsFromUser
          userName={artistMockFetch.name}
          refreshSidebarData={jest.fn()}
          id={artistMockFetch.name}
        />
      </BrowserRouter>,
    );
  });

  expect(component).toBeTruthy();

  const playlistCardName = component.queryByText(playlistDTOMockFetch.name);

  expect(playlistCardName).toBeInTheDocument();
});
