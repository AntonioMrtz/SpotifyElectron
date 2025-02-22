import '@testing-library/jest-dom';
import { act, fireEvent, render, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { BrowserRouter } from 'react-router-dom';
import Global from 'global/global';
import UserType from 'utils/role';
import UploadSongPlaylistAccordion from 'components/Sidebar/ModalUploadSongPlaylist/Accordion/UploadSongPlaylistAccordion';
import getMockHeaders from 'utils/mockHeaders';

import { debug } from 'jest-preview';

import * as TokenModule from 'utils/token';
import { t } from 'i18next';

const userName = 'prueba';
const roleUser = UserType.ARTIST;

jest.spyOn(TokenModule, 'getTokenUsername').mockReturnValue(userName);
jest.spyOn(TokenModule, 'getTokenRole').mockReturnValue(roleUser);

test('render UploadSongPlaylistAccordion', async () => {
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
        <UploadSongPlaylistAccordion
          handleClose={handleCloseMock}
          refreshSidebarData={refreshSidebarDataMock}
          setIsCloseAllowed={setIsCloseAllowed}
        />
      </BrowserRouter>,
    );
  });

  expect(component).toBeTruthy();
});

test('UploadSongPlaylistAccordion submit playlist correct', async () => {
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
        <UploadSongPlaylistAccordion
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
    component.getByText(t('uploadSongPlaylistAccordion.create-playlist')),
  ).toBeInTheDocument();

  const inputName = component.getByPlaceholderText(
    t('uploadSongPlaylistAccordion.playlist-name'),
  );
  const inputPhoto = component.getByPlaceholderText(
    t('uploadSongPlaylistAccordion.playlist-thumbnail-url'),
  );
  const inputDescripcion = component.getByPlaceholderText(
    t('uploadSongPlaylistAccordion.playlist-description'),
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

  const submitPlaylistButton = component.getByTestId('sidebar-submit-playlist');

  await act(async () => {
    fireEvent.click(submitPlaylistButton);
  });

  expect(
    component.getByText(t('uploadSongPlaylistAccordion.playlist-added-title')),
  ).toBeInTheDocument();
});

test('UploadSongPlaylistAccordion submit valid song files', async () => {
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
        <UploadSongPlaylistAccordion
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

  expect(
    component.getByText(t('uploadSongPlaylistAccordion.create-song')),
  ).toBeInTheDocument();

  const inputName = component.getByPlaceholderText(
    t('uploadSongPlaylistAccordion.song-name'),
  );
  const inputPhoto = component.getByPlaceholderText(
    t('uploadSongPlaylistAccordion.song-thumbnail-url'),
  );
  const selectGenreOption = component.getByText(
    t('uploadSongPlaylistAccordion.choose-genre-default'),
  );
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

  const submitSongButton = component.getByTestId('sidebar-submit-song');

  await act(async () => {
    fireEvent.click(submitSongButton);
  });

  expect(
    component.getByText(t('uploadSongPlaylistAccordion.song-added-title')),
  ).toBeInTheDocument();
});

test('UploadSongPlaylistAccordion rejects invalid song files', async () => {
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
        <UploadSongPlaylistAccordion
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

  expect(
    component.getByText(t('uploadSongPlaylistAccordion.create-song')),
  ).toBeInTheDocument();

  const inputName = component.getByPlaceholderText(
    t('uploadSongPlaylistAccordion.song-name'),
  );
  const inputPhoto = component.getByPlaceholderText(
    t('uploadSongPlaylistAccordion.song-thumbnail-url'),
  );
  const selectGenreOption = component.getByText(
    t('uploadSongPlaylistAccordion.choose-genre-default'),
  );
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

  const submitSongButton = component.getByTestId('sidebar-submit-song');

  await act(async () => {
    fireEvent.click(submitSongButton);
  });

  debug();
  expect(submitSongButton).toBeDisabled();
});

test('UploadSongPlaylistAccordion disables the upload button while song is uploading', async () => {
  const handleCloseMock = jest.fn();
  const refreshSidebarDataMock = jest.fn();
  const setIsCloseAllowed = jest.fn();

  // Mocking the fetch API globally
  global.fetch = jest.fn((url: string) => {
    return new Promise((resolve) => {
      if (url === `${Global.backendBaseUrl}/genres/`) {
        resolve({
          json: async () => ({ Rock: 'Rock', Pop: 'Pop' }),
          status: 200,
          ok: true,
          headers: getMockHeaders(),
        });
      } else {
        setTimeout(() => {
          resolve({
            json: async () => ({}),
            status: 201,
            ok: true,
            headers: getMockHeaders(),
          });
        }, 1000);
      }
    });
  }) as jest.Mock;

  const component = await act(async () => {
    return render(
      <BrowserRouter>
        <UploadSongPlaylistAccordion
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

  expect(
    component.getByText(t('uploadSongPlaylistAccordion.create-song')),
  ).toBeInTheDocument();

  const inputName = component.getByPlaceholderText(
    t('uploadSongPlaylistAccordion.song-name'),
  );
  const inputPhoto = component.getByPlaceholderText(
    t('uploadSongPlaylistAccordion.song-thumbnail-url'),
  );
  const selectGenreOption = component.getByText(
    t('uploadSongPlaylistAccordion.choose-genre-default'),
  );
  const dropdown = component.getByTestId('select-genre');

  const fileInputElement = component.getByTestId(
    'sidebar-file-input',
  ) as HTMLInputElement;

  const validFile = new File([''], 'test.mp3', { type: 'audio/mpeg' });

  await act(async () => {
    fireEvent.change(inputName, { target: { value: 'Test Song' } });
    fireEvent.change(inputPhoto, {
      target: { value: 'http://example.com/image.jpg' },
    });
    fireEvent.change(selectGenreOption, { target: { value: 'Rock' } });
    fireEvent.change(dropdown, { target: { value: 'Rock' } });
    fireEvent.change(fileInputElement, { target: { files: [validFile] } });
  });

  const uploadSongButton = component.getByTestId('sidebar-submit-song');

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

test('Upload song form button disabled and enabled depending on filled fields', async () => {
  const handleCloseMock = jest.fn();
  const refreshSidebarDataMock = jest.fn();
  const setIsCloseAllowed = jest.fn();

  // Mocking the fetch API globally
  global.fetch = jest.fn((url: string) => {
    return new Promise((resolve) => {
      if (url === `${Global.backendBaseUrl}/genres/`) {
        resolve({
          json: async () => ({ Rock: 'Rock', Pop: 'Pop' }),
          status: 200,
          ok: true,
          headers: getMockHeaders(),
        });
      } else {
        setTimeout(() => {
          resolve({
            json: async () => ({}),
            status: 201,
            ok: true,
            headers: getMockHeaders(),
          });
        }, 1000);
      }
    });
  }) as jest.Mock;

  const component = await act(async () => {
    return render(
      <BrowserRouter>
        <UploadSongPlaylistAccordion
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
  // Find elements
  expect(
    component.getByText(t('uploadSongPlaylistAccordion.create-song')),
  ).toBeInTheDocument();

  const inputName = component.getByPlaceholderText(
    t('uploadSongPlaylistAccordion.song-name'),
  );

  const dropdown = component.getByTestId('select-genre');
  const fileInputElement = component.getByTestId(
    'sidebar-file-input',
  ) as HTMLInputElement;

  const validFile = new File([''], 'test.mp3', { type: 'audio/mpeg' });

  const submitButton = component.getByTestId('sidebar-submit-song'); // Submit button

  // Initially, the submit button should be disabled
  expect(submitButton).toBeDisabled();

  // Fill in all required fields
  await act(async () => {
    fireEvent.change(inputName, { target: { value: 'Test Song' } });
    fireEvent.change(dropdown, { target: { value: 'Rock' } });
    fireEvent.change(fileInputElement, { target: { files: [validFile] } });
  });

  // Verify submit button is enabled after filling all required fields
  await waitFor(() => {
    expect(submitButton).toBeEnabled();
  });
});

test('Add playlist form button disabled and enabled depending on filled fields', async () => {
  const handleCloseMock = jest.fn();
  const refreshSidebarDataMock = jest.fn();
  const setIsCloseAllowed = jest.fn();

  // Mocking the fetch API globally
  global.fetch = jest.fn((url: string) => {
    return new Promise((resolve) => {
      if (url === `${Global.backendBaseUrl}/genres/`) {
        resolve({
          json: async () => ({ Rock: 'Rock', Pop: 'Pop' }),
          status: 200,
          ok: true,
          headers: getMockHeaders(),
        });
      } else {
        setTimeout(() => {
          resolve({
            json: async () => ({}),
            status: 201,
            ok: true,
            headers: getMockHeaders(),
          });
        }, 1000);
      }
    });
  }) as jest.Mock;

  const component = await act(async () => {
    return render(
      <BrowserRouter>
        <UploadSongPlaylistAccordion
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
  // Find elements
  const inputName = component.getByPlaceholderText(
    t('uploadSongPlaylistAccordion.playlist-name'),
  );

  const submitButton = component.getByTestId('sidebar-submit-playlist'); // Submit button

  // Initially, the submit button should be disabled
  expect(submitButton).toBeDisabled();

  // Fill in all required fields
  await act(async () => {
    fireEvent.change(inputName, { target: { value: 'Test Song' } });
  });

  // Verify submit button is enabled after filling all required fields
  await waitFor(() => {
    expect(submitButton).toBeEnabled();
  });
});
