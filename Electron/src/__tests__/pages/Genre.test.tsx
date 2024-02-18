import '@testing-library/jest-dom';
import { act, render } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import Genre from 'pages/Genre/Genre';

const genreName = 'Rock';

const songMockFetch = {
  name: 'cancion',
  artist: 'artist',
  photo: 'photo',
  duration: '3',
  genre: 'Rock',
  number_of_plays: 2,
};

global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () =>
      Promise.resolve({
        songs: [JSON.stringify(songMockFetch)],
      }),
    status: 200,
  }),
) as jest.Mock;

test('Render Genre with one song', async () => {
  const component = await act(() => {
    return render(
      <MemoryRouter initialEntries={[`/artist/${genreName}`]}>
        <Routes>
          <Route
            path="/artist/:id"
            element={
              <Genre
                refreshSidebarData={jest.fn()}
                changeSongName={jest.fn()}
              />
            }
          />
        </Routes>
      </MemoryRouter>,
    );
  });

  expect(component).toBeTruthy();
});
