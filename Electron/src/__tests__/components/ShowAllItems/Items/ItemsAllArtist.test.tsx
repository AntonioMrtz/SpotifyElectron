import '@testing-library/jest-dom';
import { render } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { BrowserRouter } from 'react-router-dom';
import Global from 'global/global';
import ItemsAllArtist from 'components/ShowAllItems/Items/ItemsAllArtist';
import * as router from 'react-router';
import getMockHeaders from 'utils/mockHeaders';
import { act } from 'react';

const navigate = jest.fn();

jest.spyOn(router, 'useNavigate').mockImplementation(() => navigate);

test('Render ItemsAllArtist', async () => {
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
        <ItemsAllArtist />
      </BrowserRouter>,
    );
  });

  expect(component).toBeTruthy();

  const artistCardName = component.queryByText('name');
  expect(artistCardName).toBeInTheDocument();
});
