import '@testing-library/jest-dom';
import { act, fireEvent, render } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { BrowserRouter } from 'react-router-dom';
import Global from 'global/global';
import UserType from 'utils/role';
import AddSongPlayListAccordion from 'components/Sidebar/ModalAddSongPlaylist/Accordion/AddSongPlayListAccordion';
import getMockHeaders from 'utils/mockHeaders';

import * as TokenModule from 'utils/token';

const userName = 'prueba';
const roleUser = UserType.ARTIST;

jest.spyOn(TokenModule, 'getTokenUsername').mockReturnValue(userName);
jest.spyOn(TokenModule, 'getTokenRole').mockReturnValue(roleUser);

test('render AddSongPlaylistAccordion', async () => {
  const handleCloseMock = jest.fn();
  const refreshSidebarDataMock = jest.fn();
  const setIsCloseAllowed = jest.fn();

  global.fetch = jest.fn(async (url: string) => {
    if (url === `${Global.backendBaseUrl}/genres/`) {
      return Promise.resolve({
        json: () => JSON.stringify({ Rock: 'Rock', Pop: 'Pop' }),
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
        <AddSongPlayListAccordion
          handleClose={handleCloseMock}
          refreshSidebarData={refreshSidebarDataMock}
          setIsCloseAllowed={setIsCloseAllowed}
        />
      </BrowserRouter>,
    );
  });

  expect(component).toBeTruthy();
});

test('AddSongPlaylistAccordion submit playlist correct', async () => {
  const handleCloseMock = jest.fn();
  const refreshSidebarDataMock = jest.fn();
  const setIsCloseAllowed = jest.fn();

  global.fetch = jest.fn(async (url: string) => {
    if (url === `${Global.backendBaseUrl}/genres/`) {
      return Promise.resolve({
        json: () => JSON.stringify({ Rock: 'Rock', Pop: 'Pop' }),
        status: 200,
        ok: true,
        headers: getMockHeaders(),
      }).catch((error) => {
        console.log(error);
      });
    }

    return Promise.resolve({
      json: () => {},
      status: 201,
      ok: true,
      headers: getMockHeaders(),
    }).catch((error) => {
      console.log(error);
    });
  }) as jest.Mock;

  const component = await act(() => {
    return render(
      <BrowserRouter>
        <AddSongPlayListAccordion
          handleClose={handleCloseMock}
          refreshSidebarData={refreshSidebarDataMock}
          setIsCloseAllowed={setIsCloseAllowed}
        />
      </BrowserRouter>,
    );
  });

  const accordionExpandPlaylist = component.getByTestId(
    'accordion-expand-submit-playlist',
  );

  await act(async () => {
    fireEvent.click(accordionExpandPlaylist);
  });

  expect(
    component.getByText('Crear lista de reproducción'),
  ).toBeInTheDocument();

  const inputName = component.getByPlaceholderText('Nombre de la playlist');
  const inputPhoto = component.getByPlaceholderText(
    'URL de la miniatura de la playlist',
  );
  const inputDescripcion = component.getByPlaceholderText(
    'Descripción de la playlist',
  );

  fireEvent.change(inputName, {
    target: { value: 'testuser' },
  });
  fireEvent.change(inputPhoto, {
    target: { value: 'testpassword' },
  });
  fireEvent.change(inputDescripcion, {
    target: { value: 'testfoto' },
  });

  const submitPlaylistButton = component.getByTestId(
    'sidebar-addsongplaylistaccordion-submit-playlist',
  );

  await act(async () => {
    fireEvent.click(submitPlaylistButton);
  });

  expect(component.getByText('Playlist Añadida')).toBeInTheDocument();
});

test('AddSongPlaylistAccordion submit song correct', async () => {
  const handleCloseMock = jest.fn();
  const refreshSidebarDataMock = jest.fn();
  const setIsCloseAllowed = jest.fn();

  global.fetch = jest.fn(async (url: string) => {
    if (url === `${Global.backendBaseUrl}/genres/`) {
      return Promise.resolve({
        json: () => JSON.stringify({ Rock: 'Rock', Pop: 'Pop' }),
        status: 200,
        ok: true,
        headers: getMockHeaders(),
      }).catch((error) => {
        console.log(error);
      });
    }

    return Promise.resolve({
      json: () => {},
      status: 201,
      ok: true,
      headers: getMockHeaders(),
    }).catch((error) => {
      console.log(error);
    });
  }) as jest.Mock;

  const component = await act(() => {
    return render(
      <BrowserRouter>
        <AddSongPlayListAccordion
          handleClose={handleCloseMock}
          refreshSidebarData={refreshSidebarDataMock}
          setIsCloseAllowed={setIsCloseAllowed}
        />
      </BrowserRouter>,
    );
  });

  const accordionExpandSong = component.getByTestId(
    'accordion-expand-submit-song',
  );

  await act(async () => {
    fireEvent.click(accordionExpandSong);
  });

  expect(component.getByText('Subir canción')).toBeInTheDocument();

  const inputName = component.getByPlaceholderText('Nombre de la canción');
  const inputPhoto = component.getByPlaceholderText(
    'URL de la miniatura de la canción',
  );
  const selectGenreOption = component.getByText('❗ Elige un género');
  const dropdown = component.getByTestId('select-genre');

  // Find the file input element by it's name or other suitable selector
  const fileInputElement = component.getByTestId('sidebar-file-input');

  // Create a sample file
  const file = new File(['(⌐□_□)'], 'sample.mp3', { type: 'audio/mp3' });

  await act(async () => {
    fireEvent.change(inputName, {
      target: { value: 'testuser' },
    });
    fireEvent.change(inputPhoto, {
      target: { value: 'testpassword' },
    });
    /* ! TODO For some both fireEvent are necessary and without one
    the genre selected is empty causing the test to fail
     */
    fireEvent.change(selectGenreOption, {
      target: { value: 'Rock' },
    });
    fireEvent.change(dropdown, { target: { value: 'Rock' } });
    fireEvent.change(fileInputElement, { target: { files: [file] } });
  });

  const submitSongButton = component.getByTestId(
    'sidebar-addsongplaylistaccordion-submit-song',
  );

  await act(async () => {
    fireEvent.click(submitSongButton);
  });

  expect(component.getByText('Canción Añadida')).toBeInTheDocument();
});
