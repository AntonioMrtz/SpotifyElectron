import '@testing-library/jest-dom';
import { act, render } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { BrowserRouter } from 'react-router-dom';
import Global from 'global/global';
import ItemsAllSongsFromArtist from 'components/ShowAllItems/Items/ItemsAllSongsFromArtist';
import getMockHeaders from 'utils/mockHeaders';
import { NowPlayingContextProvider } from 'providers/NowPlayingProvider';

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
  seconds_duration: '3',
  genre: 'Rock',
  streams: 2,
};

test('Render items All Songs from Artist', async () => {
  global.fetch = jest.fn((url: string) => {
    if (
      url === `${Global.backendBaseUrl}/artists/${artistMockFetch.name}/songs`
    ) {
      return Promise.resolve({
        json: () => [songMockFetch],
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
        <NowPlayingContextProvider>
          <ItemsAllSongsFromArtist
            artistName={artistMockFetch.name}
            refreshSidebarData={jest.fn()}
            id={artistMockFetch.name}
          />
        </NowPlayingContextProvider>
      </BrowserRouter>,
    );
  });

  expect(component).toBeTruthy();

  const songCardName = component.queryByText(songMockFetch.name);

  expect(songCardName).toBeInTheDocument();
});
