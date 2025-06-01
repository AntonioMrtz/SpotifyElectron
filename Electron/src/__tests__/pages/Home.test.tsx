import '@testing-library/jest-dom';
import { render } from '@testing-library/react';
import Home from 'pages/Home/Home';
import Global from 'global/global';
import { BrowserRouter } from 'react-router-dom';
import { t } from 'i18next';
import { act } from 'react';

test('render Home', async () => {
  global.fetch = jest.fn(() =>
    Promise.resolve({
      json: () => Promise.resolve({}),
      status: 200,
      ok: true,
    }),
  ) as jest.Mock;

  const component = await act(() => {
    return render(
      <BrowserRouter>
        <Home refreshSidebarData={jest.fn()} />
      </BrowserRouter>,
    );
  });

  expect(component).toBeTruthy();
});

test('Home fields', async () => {
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

  const component = await act(() => {
    return render(
      <BrowserRouter>
        <Home refreshSidebarData={jest.fn()} />
      </BrowserRouter>,
    );
  });

  expect(component.queryByText(t('home.made-for'))).toBeInTheDocument();

  expect(component.queryByText(t('home.top-artists'))).toBeInTheDocument();
});
