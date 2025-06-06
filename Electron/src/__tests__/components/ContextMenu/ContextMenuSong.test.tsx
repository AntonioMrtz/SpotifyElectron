import '@testing-library/jest-dom';
import '@testing-library/jest-dom/extend-expect';
import { act, fireEvent, render, waitFor } from '@testing-library/react';
import ContextMenuSong from 'components/AdvancedUIComponents/ContextMenu/Song/ContextMenuSong';
import Global from 'global/global';
import UserType from 'utils/role';
import * as router from 'react-router';
import { BrowserRouter } from 'react-router-dom';
import getMockHeaders from 'utils/mockHeaders';
import * as TokenModule from 'utils/token';
import { t } from 'i18next';
import { SidebarProvider } from 'providers/SidebarProvider';
import * as SidebarModule from 'providers/SidebarProvider';

const playlistName = 'playlisttest';
const songName = 'songName';
const artistName = 'artistName';
const userName = 'prueba';
const roleUser = UserType.ARTIST;

const artistMockFetch = {
  name: userName,
  photo: 'photo',
  register_date: 'date',
  password: 'hashpassword',
  playback_history: [songName],
  playlists: [playlistName],
  saved_playlists: [playlistName],
  uploaded_songs: [songName],
};

const playlistDTOMockFetch = {
  name: playlistName,
  photo: 'playlist',
  description: 'des',
  upload_date: 'date',
  owner: userName,
  song_names: [],
};

const navigate = jest.fn();

jest.spyOn(router, 'useNavigate').mockImplementation(() => navigate);

jest.spyOn(TokenModule, 'getTokenUsername').mockReturnValue(userName);
jest.spyOn(TokenModule, 'getTokenRole').mockReturnValue(roleUser);

global.fetch = jest.fn((url: string, options: any) => {
  if (
    url === `${Global.backendBaseUrl}/playlists/${playlistDTOMockFetch.name}`
  ) {
    return Promise.resolve({
      json: () => playlistDTOMockFetch,
      status: 200,
      ok: true,
      headers: getMockHeaders(),
    }).catch((error) => {
      console.log(error);
    });
  }
  if (
    url ===
    `${Global.backendBaseUrl}/users/${artistMockFetch.name}/playlist_names`
  ) {
    return Promise.resolve({
      json: () => [playlistName],
      status: 200,
      ok: true,
      headers: getMockHeaders(),
    }).catch((error) => {
      console.log(error);
    });
  }

  if (options.method === 'DELETE') {
    return Promise.resolve({
      json: () => artistMockFetch,
      status: 202,
      ok: true,
    }).catch((error) => {
      console.log(error);
    });
  }
  if (options.method === 'PUT') {
    return Promise.resolve({
      json: () => artistMockFetch,
      status: 204,
      ok: true,
    }).catch((error) => {
      console.log(error);
    });
  }

  if (options.method === 'POST') {
    return Promise.resolve({
      json: () => artistMockFetch,
      status: 201,
      ok: true,
    }).catch((error) => {
      console.log(error);
    });
  }

  // In case the URL doesn't match, return a rejected promise
  return Promise.reject(new Error(`Unhandled URL in fetch mock: ${url}`));
}) as jest.Mock;

test('Render ContextMenuSong', async () => {
  const component = await act(() => {
    return render(
      <BrowserRouter>
        <SidebarProvider>
          <ContextMenuSong
            playlistName={playlistName}
            songName={songName}
            artistName={artistName}
            handleCloseParent={jest.fn()}
            refreshPlaylistData={jest.fn()}
          />
        </SidebarProvider>
      </BrowserRouter>,
    );
  });
  expect(component).toBeTruthy();
});

test('ContextMenuSong remove from playlist', async () => {
  const refreshPlaylistDataMock = jest.fn();

  const component = await act(() => {
    return render(
      <BrowserRouter>
        <SidebarProvider>
          <ContextMenuSong
            playlistName={playlistName}
            songName={songName}
            artistName={artistName}
            handleCloseParent={jest.fn()}
            refreshPlaylistData={refreshPlaylistDataMock}
          />
        </SidebarProvider>
      </BrowserRouter>,
    );
  });

  try {
    const quitarListaButton = component.getByText(
      t('contextMenuSong.remove-from-playlist'),
    );

    await act(async () => {
      fireEvent.click(quitarListaButton);
    });

    expect(refreshPlaylistDataMock).toHaveBeenCalled();
  } catch (error) {
    // eslint-disable-next-line jest/no-conditional-expect
    expect(error).toBeUndefined();
  }
});

test('ContextMenuSong create playlist', async () => {
  const refreshSidebarMock = jest.fn();

  // Mock the useSidebar hook
  jest.spyOn(SidebarModule, 'useSidebar').mockReturnValue({
    refreshSidebarData: refreshSidebarMock,
  });

  const component = await act(() => {
    return render(
      <BrowserRouter>
        <SidebarProvider>
          <ContextMenuSong
            playlistName={playlistName}
            songName={songName}
            artistName={artistName}
            handleCloseParent={jest.fn()}
            refreshPlaylistData={jest.fn()}
          />
        </SidebarProvider>
      </BrowserRouter>,
    );
  });

  try {
    const addToListButton = component.getByText(
      t('contextMenuSong.add-to-playlist'),
    );

    await act(async () => {
      fireEvent.click(addToListButton);
    });

    const crearListaButton = component.getByText(
      t('contextMenuSong.create-playlist'),
    );

    await act(async () => {
      fireEvent.click(crearListaButton);
    });

    // Wait for the refreshSidebarMock to be called
    await waitFor(
      () => {
        expect(refreshSidebarMock).toHaveBeenCalled();
      },
      {
        timeout: 3000,
        interval: 100,
      },
    );
  } catch (error) {
    // eslint-disable-next-line jest/no-conditional-expect
    expect(error).toBeUndefined();
  }
});

test('ContextMenuSong add to playlist', async () => {
  const component = await act(() => {
    return render(
      <BrowserRouter>
        <SidebarProvider>
          <ContextMenuSong
            playlistName={playlistName}
            songName={songName}
            artistName={artistName}
            handleCloseParent={jest.fn()}
            refreshPlaylistData={jest.fn()}
          />
        </SidebarProvider>
      </BrowserRouter>,
    );
  });

  try {
    const addToListButton = component.getByText(
      t('contextMenuSong.add-to-playlist'),
    );

    await act(async () => {
      fireEvent.click(addToListButton);
    });

    const playlistButton = component.getByText(playlistName);

    await act(async () => {
      fireEvent.click(playlistButton);
    });
  } catch (error) {
    // eslint-disable-next-line jest/no-conditional-expect
    expect(error).toBeUndefined();
  }
});
