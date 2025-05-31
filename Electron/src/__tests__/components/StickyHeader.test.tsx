import '@testing-library/jest-dom';
import { fireEvent, render } from '@testing-library/react';
import { act } from 'react';
import '@testing-library/jest-dom/extend-expect';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import StickyHeader from 'components/StickyHeader/StickyHeader';
import * as TokenModule from 'utils/token';
import UserType from 'utils/role';
import Global from 'global/global';
import getMockHeaders from 'utils/mockHeaders';
import { NowPlayingContextProvider } from 'providers/NowPlayingProvider';
import { t } from 'i18next';

const userName = 'prueba';
const roleUser = UserType.USER;

jest.spyOn(TokenModule, 'getTokenUsername').mockReturnValue(userName);
jest.spyOn(TokenModule, 'getTokenRole').mockReturnValue(roleUser);

const userMockFetch = {
  name: userName,
  photo: 'photo',
  register_date: 'date',
  password: 'hashpassword',
  playback_history: [],
  playlists: [],
  saved_playlists: [],
};

global.fetch = jest.fn((url: string) => {
  if (url === `${Global.backendBaseUrl}/users/${userMockFetch.name}`) {
    return Promise.resolve({
      json: () => userMockFetch,
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

test('Render StickyHeader and get User data', async () => {
  const component = await act(() => {
    return render(
      <MemoryRouter initialEntries={[`/location`]}>
        <NowPlayingContextProvider>
          <Routes>
            <Route
              path="/location"
              element={<StickyHeader handleLogout={jest.fn()} />}
            />
          </Routes>
        </NowPlayingContextProvider>
      </MemoryRouter>,
    );
  });

  expect(component).toBeTruthy();
});

test('StickyHeader open ContextMenuProfile', async () => {
  const component = await act(() => {
    return render(
      <MemoryRouter initialEntries={[`/location`]}>
        <NowPlayingContextProvider>
          <Routes>
            <Route
              path="/location"
              element={<StickyHeader handleLogout={jest.fn()} />}
            />
          </Routes>
        </NowPlayingContextProvider>
      </MemoryRouter>,
    );
  });

  const imageIconProfile = component.getByAltText('profile-icon');

  await act(async () => {
    fireEvent.click(imageIconProfile);
  });

  expect(
    component.queryByText(t('contextMenuProfile.log-out')),
  ).toBeInTheDocument();

  expect(
    component.queryByText(t('contextMenuProfile.profile')),
  ).toBeInTheDocument();
});
