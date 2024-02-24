import '@testing-library/jest-dom';
import { act, render } from '@testing-library/react';
import * as router from 'react-router';
import '@testing-library/jest-dom/extend-expect';
import Home from 'pages/Home/Home';
import Global from 'global/global';
import { BrowserRouter } from 'react-router-dom';

const navigate = jest.fn();

beforeEach(() => {
  jest.spyOn(router, 'useNavigate').mockImplementation(() => navigate);
});

test('render Home', async () => {
  global.fetch = jest.fn(() =>
    Promise.resolve({
      json: () => Promise.resolve({}),
      status: 200,
    }),
  ) as jest.Mock;

  const component = await act(() => {
    return render(<Home refreshSidebarData={jest.fn()} />);
  });

  expect(component).toBeTruthy();
});

test('Home fields', async () => {
  global.fetch = jest.fn(() =>
    Promise.resolve({
      json: () => Promise.resolve({}),
      status: 200,
    }),
  ) as jest.Mock;

  const component = await act(() => {
    return render(<Home refreshSidebarData={jest.fn()} />);
  });

  expect(component.queryByText('Especialmente para ti')).toBeInTheDocument();

  expect(component.queryByText('Artistas destacados')).toBeInTheDocument();
});

test('prueba', async () => {
  global.fetch = jest.fn((url: string) => {
    if (url === `${Global.backendBaseUrl}artistas/`) {
      return Promise.resolve({
        json: () =>
          Promise.resolve({
            artists: [
              JSON.stringify({
                name: 'name',
                photo: 'photo',
                register_date: 'date',
                password: 'pass',
                playback_history: [],
                playlists: [],
                saved_playlists: [],
              }),
            ],
          }),
        status: 200,
      }).catch((error) => {
        console.log(error);
      });
    }
    if (url === `${Global.backendBaseUrl}playlists/`) {
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
        <Home refreshSidebarData={jest.fn()} />
      </BrowserRouter>,
    );
  });

  expect(component.queryByText('Especialmente para ti')).toBeInTheDocument();
  expect(component.queryByText('Artistas destacados')).toBeInTheDocument();
});
