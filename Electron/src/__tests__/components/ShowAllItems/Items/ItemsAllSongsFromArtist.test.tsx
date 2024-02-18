import '@testing-library/jest-dom';
import { act, render } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { BrowserRouter } from 'react-router-dom';
import Global from 'global/global';
import ItemsAllSongsFromArtist from 'components/ShowAllItems/Items/ItemsAllSongsFromArtist';

const playlistName = 'playlisttest';
const songName = 'songName';

const artistMockFetch = {
  name: 'name',
  photo: 'photo',
  register_date: 'date',
  password: 'hashpassword',
  playback_history: [songName],
  playlists: [playlistName],
  saved_playlists: [playlistName],
  uploaded_songs: [songName],
};

const songMockFetch = {
  name: songName,
  artist: 'artist',
  photo: 'photo',
  duration: '3',
  genre: 'Rock',
  number_of_plays: 2,
};

test('Render items All Songs from Artist', async () => {
  global.fetch = jest.fn((url: string) => {
    if (url === `${Global.backendBaseUrl}artistas/${artistMockFetch.name}`) {
      return Promise.resolve({
        json: () => artistMockFetch,
        status: 200,
      }).catch((error) => {
        console.log(error);
      });
    }
    if (url === `${Global.backendBaseUrl}canciones/dto/${songName}`) {
      return Promise.resolve({
        json: () => songMockFetch,
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
        <ItemsAllSongsFromArtist
          artistName={artistMockFetch.name}
          refreshSidebarData={jest.fn()}
          changeSongName={jest.fn()}
          id={artistMockFetch.name}
        />
      </BrowserRouter>,
    );
  });

  expect(component).toBeTruthy();

  const songCardName = component.queryByText(songMockFetch.name);

  expect(songCardName).toBeInTheDocument();
});
