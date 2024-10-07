import '@testing-library/jest-dom';
import { act, fireEvent, render, waitFor } from '@testing-library/react';
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

test('AddSongPlaylistAccordion submit valid song files', async () => {
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
  const fileInputElement = component.getByTestId(
    'sidebar-file-input',
  ) as HTMLInputElement;

  // Create valid sample files
  const mp3File = new File(['(⌐□_□)'], 'sample.mp3', { type: 'audio/mp3' });
  const wavFile = new File(['(⌐□_□)'], 'sample.wav', { type: 'audio/wav' });
  const flacFile = new File(['(⌐□_□)'], 'sample.flac', { type: 'audio/flac' });
  const aacFile = new File(['(⌐□_□)'], 'sample.aac', { type: 'audio/aac' });

  await act(async () => {
    fireEvent.change(inputName, {
      target: { value: 'testuser' },
    });
    fireEvent.change(inputPhoto, {
      target: { value: 'testpassword' },
    });
    /* ! TODO For some reasion both fireEvent are necessary . Without one
    the genre selected is empty causing the test to fail
     */
    fireEvent.change(selectGenreOption, {
      target: { value: 'Rock' },
    });
    fireEvent.change(dropdown, { target: { value: 'Rock' } });
  });

  // Test valid file formats
  await act(async () => {
    fireEvent.change(fileInputElement, { target: { files: [mp3File] } });
  });
  expect(fileInputElement.files?.[0]).toBe(mp3File);

  await act(async () => {
    fireEvent.change(fileInputElement, { target: { files: [wavFile] } });
  });
  expect(fileInputElement.files?.[0]).toBe(wavFile);

  await act(async () => {
    fireEvent.change(fileInputElement, { target: { files: [flacFile] } });
  });
  expect(fileInputElement.files?.[0]).toBe(flacFile);

  await act(async () => {
    fireEvent.change(fileInputElement, { target: { files: [aacFile] } });
  });
  expect(fileInputElement.files?.[0]).toBe(aacFile);

  const submitSongButton = component.getByTestId(
    'sidebar-addsongplaylistaccordion-submit-song',
  );

  await act(async () => {
    fireEvent.click(submitSongButton);
  });

  expect(component.getByText('Canción Añadida')).toBeInTheDocument();
});

test('AddSongPlaylistAccordion rejects invalid song files', async () => {
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
  const fileInputElement = component.getByTestId(
    'sidebar-file-input',
  ) as HTMLInputElement;

  // Create an invalid sample file
  const invalidFile = new File(['a'], 'sample.txt', { type: 'text/plain' });

  await act(async () => {
    fireEvent.change(inputName, {
      target: { value: 'testuser' },
    });
    fireEvent.change(inputPhoto, {
      target: { value: 'testpassword' },
    });
    /* ! TODO For some reasion both fireEvent are necessary . Without one
    the genre selected is empty causing the test to fail
     */
    fireEvent.change(selectGenreOption, {
      target: { value: 'Rock' },
    });
    fireEvent.change(dropdown, { target: { value: 'Rock' } });
  });

  // Test invalid file format
  await act(async () => {
    fireEvent.change(fileInputElement, { target: { files: [invalidFile] } });
  });
  expect(fileInputElement.value).toBe('');

  const submitSongButton = component.getByTestId(
    'sidebar-addsongplaylistaccordion-submit-song',
  );

  await act(async () => {
    fireEvent.click(submitSongButton);
  });

  expect(component.queryByText('Canción Añadida')).not.toBeInTheDocument();
});

test('AddSongPlaylistAccordion disables the upload button while song is uploading', async () => {
  const handleCloseMock = jest.fn();
  const refreshSidebarDataMock = jest.fn();
  const setIsCloseAllowed = jest.fn();

   // Mocking the fetch API globally
  global.fetch = jest.fn(async (url: string) => {
      if (url === `${Global.backendBaseUrl}/genres/`) {
          return Promise.resolve({
              json: () => JSON.stringify({ Rock: 'Rock', Pop: 'Pop' }),
              status: 200,
              ok: true,
              headers: getMockHeaders(),
          });
      }

      // Delay for loading simulation
      await new Promise((resolve) => setTimeout(resolve, 1000));

      // Mock response for song upload request
      return Promise.resolve({
          json: () => {},
          status: 201,
          ok: true,
          headers: getMockHeaders(),
      });
  }) as jest.Mock;

  const component = await act(async () => {
      return render(
          <BrowserRouter>
              <AddSongPlayListAccordion
                  handleClose={handleCloseMock}
                  refreshSidebarData={refreshSidebarDataMock}
                  setIsCloseAllowed={setIsCloseAllowed}
              />
          </BrowserRouter>
      );
  });

  const accordionExpandSong = component.getByTestId('accordion-expand-submit-song');

  await act(async () => {
      fireEvent.click(accordionExpandSong);
  });

  expect(component.getByText('Subir canción')).toBeInTheDocument();

  const inputName = component.getByPlaceholderText('Nombre de la canción');
  const inputPhoto = component.getByPlaceholderText('URL de la miniatura de la canción');
  const selectGenreOption = component.getByText('❗ Elige un género');
  const dropdown = component.getByTestId('select-genre');

  const fileInputElement = component.getByTestId('sidebar-file-input') as HTMLInputElement;

  const validFile = new File([''], 'test.mp3', { type: 'audio/mpeg' });

  await act(async () => {
      fireEvent.change(inputName, { target: { value: 'Test Song' } });
      fireEvent.change(inputPhoto, { target: { value: 'http://example.com/image.jpg' } });
      fireEvent.change(selectGenreOption, { target: { value: 'Rock' } });
      fireEvent.change(dropdown, { target: { value: 'Rock' } });
      fireEvent.change(fileInputElement, { target: { files: [validFile] } });
  });

  const uploadSongButton = component.getByTestId('sidebar-addsongplaylistaccordion-submit-song');

  // Verify that the upload button is enabled
  await waitFor(() => {
      expect(uploadSongButton).toBeEnabled();
  });

  await act(async () => {
      fireEvent.click(uploadSongButton);
  });

  // Verify that the upload button is disabled while uploading
  await waitFor(() => {
      expect(uploadSongButton).toBeDisabled();
  });

  
});