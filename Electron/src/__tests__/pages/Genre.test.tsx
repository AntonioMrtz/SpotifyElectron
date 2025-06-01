import '@testing-library/jest-dom';
import { render } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import Genre from 'pages/Genre/Genre';
import { act } from 'react';

const genreName = 'Rock';

const songMockFetch = {
  name: 'cancion',
  artist: 'artist',
  photo: 'photo',
  seconds_duration: '3',
  genre: 'Rock',
  streams: 2,
};

global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () =>
      Promise.resolve({
        songs: [JSON.stringify(songMockFetch)],
      }),
    status: 200,
    ok: true,
  }),
) as jest.Mock;

test('Render Genre with one song', async () => {
  const component = await act(() => {
    return render(
      <MemoryRouter initialEntries={[`/artist/${genreName}`]}>
        <Routes>
          <Route
            path="/artist/:id"
            element={<Genre refreshSidebarData={jest.fn()} />}
          />
        </Routes>
      </MemoryRouter>,
    );
  });

  expect(component).toBeTruthy();
});
