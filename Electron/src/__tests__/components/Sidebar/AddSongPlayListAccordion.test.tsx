import '@testing-library/jest-dom';
import { act, fireEvent, render } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { BrowserRouter } from 'react-router-dom';
import Global from 'global/global';
import Token from 'utils/token';
import UserType from 'utils/role';
import AddSongPlayListAccordion from 'components/Sidebar/ModalAddSongPlaylist/Accordion/AddSongPlayListAccordion';

const userName = 'prueba';
const roleUser = UserType.ARTIST;

jest.spyOn(Token, 'getTokenUsername').mockReturnValue(userName);
jest.spyOn(Token, 'getTokenRole').mockReturnValue(roleUser);

test('render AddSongPlaylistAccordion', async () => {
  const handleCloseMock = jest.fn();
  const reloadSidebarMock = jest.fn();
  const setIsCloseAllowed = jest.fn();

  global.fetch = jest.fn(async (url: string) => {
    if (url === `${Global.backendBaseUrl}genres/`) {
      return Promise.resolve({
        json: () => JSON.stringify({ Rock: 'Rock', Pop: 'Pop' }),
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
        <AddSongPlayListAccordion
          handleClose={handleCloseMock}
          reloadSidebar={reloadSidebarMock}
          setIsCloseAllowed={setIsCloseAllowed}
        />
      </BrowserRouter>,
    );
  });

  expect(component).toBeTruthy();
});

test('AddSongPlaylistAccordion submit playlist correct', async () => {
  const handleCloseMock = jest.fn();
  const reloadSidebarMock = jest.fn();
  const setIsCloseAllowed = jest.fn();

  global.fetch = jest.fn(async (url: string) => {
    if (url === `${Global.backendBaseUrl}genres/`) {
      return Promise.resolve({
        json: () => JSON.stringify({ Rock: 'Rock', Pop: 'Pop' }),
        status: 200,
      }).catch((error) => {
        console.log(error);
      });
    }

    return Promise.resolve({
      json: () => {},
      status: 201,
    }).catch((error) => {
      console.log(error);
    });
  }) as jest.Mock;

  const component = await act(() => {
    return render(
      <BrowserRouter>
        <AddSongPlayListAccordion
          handleClose={handleCloseMock}
          reloadSidebar={reloadSidebarMock}
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
  const reloadSidebarMock = jest.fn();
  const setIsCloseAllowed = jest.fn();

  global.fetch = jest.fn(async (url: string) => {
    if (url === `${Global.backendBaseUrl}genres/`) {
      return Promise.resolve({
        json: () => JSON.stringify({ Rock: 'Rock', Pop: 'Pop' }),
        status: 200,
      }).catch((error) => {
        console.log(error);
      });
    }

    return Promise.resolve({
      json: () => {},
      status: 201,
    }).catch((error) => {
      console.log(error);
    });
  }) as jest.Mock;

  const component = await act(() => {
    return render(
      <BrowserRouter>
        <AddSongPlayListAccordion
          handleClose={handleCloseMock}
          reloadSidebar={reloadSidebarMock}
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
    'URL de la miniatura de la playlist',
  );
  const eligeUnGeneroOption = component.getByText('❗ Elige un género');

  // Find the file input element by its name or other suitable selector
  const fileInputElement = component.getByTestId('sidebar-file-input');

  // Create a sample file
  const file = new File(['(⌐□_□)'], 'sample.mp3', { type: 'audio/mp3' });

  fireEvent.change(inputName, {
    target: { value: 'testuser' },
  });
  fireEvent.change(inputPhoto, {
    target: { value: 'testpassword' },
  });

  // Simulate selecting an option
  fireEvent.change(eligeUnGeneroOption, {
    target: { value: 'Rock' },
  });

  fireEvent.change(fileInputElement, { target: { files: [file] } });

  const submitSongButton = component.getByTestId(
    'sidebar-addsongplaylistaccordion-submit-song',
  );

  await act(async () => {
    fireEvent.click(submitSongButton);
  });

  expect(component.getByText('Canción Añadida')).toBeInTheDocument();
});
