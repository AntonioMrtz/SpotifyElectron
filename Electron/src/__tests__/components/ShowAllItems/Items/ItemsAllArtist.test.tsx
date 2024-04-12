import '@testing-library/jest-dom';
import { act, render } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { BrowserRouter } from 'react-router-dom';
import Global from 'global/global';
import ItemsAllArtist from 'components/ShowAllItems/Items/ItemsAllArtist';
import * as router from 'react-router';

const navigate = jest.fn();

jest.spyOn(router, 'useNavigate').mockImplementation(() => navigate);

test('Render ItemsAllArtist', async () => {
  global.fetch = jest.fn((url: string) => {
    if (url === `${Global.backendBaseUrl}artistas/`) {
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
        <ItemsAllArtist />
      </BrowserRouter>,
    );
  });

  expect(component).toBeTruthy();

  const artistCardName = component.queryByText('name');
  expect(artistCardName).toBeInTheDocument();
});
