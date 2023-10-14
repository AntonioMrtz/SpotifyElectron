import '@testing-library/jest-dom';
import { act, render } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { BrowserRouter } from 'react-router-dom';
import Global from 'global/global';
import * as router from 'react-router';
import ItemsAllPlaylists from 'components/ShowAllItems/Items/ItemsAllPlaylists';

const navigate = jest.fn();
jest.spyOn(router, 'useNavigate').mockImplementation(() => navigate);

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
    if (url === `${Global.backendBaseUrl}playlists/`) {
      return Promise.resolve({
        json: () =>
          Promise.resolve({
            playlists: [
              JSON.stringify({
                name: playlistName,
                photo: 'photo',
                description: 'description',
                upload_date: 'date',
                owner: 'owner',
                songs: [],
              }),
            ],
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
      <BrowserRouter>
        <ItemsAllPlaylists
          refreshSidebarData={jest.fn()}
          id={playlistDTOMockFetch.name}
        />
      </BrowserRouter>
    );
  });

  expect(component).toBeTruthy();

  const playlistCardName = component.queryByText(playlistDTOMockFetch.name);

  expect(playlistCardName).toBeInTheDocument();
});
