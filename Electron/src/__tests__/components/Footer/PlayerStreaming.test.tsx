import '@testing-library/jest-dom';
import '@testing-library/jest-dom/extend-expect';
import { render } from '@testing-library/react';
import PlayerStreaming from 'components/footer/Player/PlayerStreaming';
import Global from 'global/global';
import Token from 'utils/token';
import { UserType } from 'utils/role';
import { act } from 'react-test-renderer';

const songName = 'songName';
const userName = 'prueba';
const roleUser = UserType.USER;

const songMockFetch = {
  name: songName,
  artist: userName,
  photo: 'photo',
  seconds_duration: '180',
  genre: 'Rock',
  number_of_plays: 2,
  url: 'https://5b44cf20b0388.streamlock.net:8443/vod/smil:bbb.smil/playlist.m3u8',
};

jest.spyOn(Token, 'getTokenUsername').mockReturnValue(userName);
jest.spyOn(Token, 'getTokenRole').mockReturnValue(roleUser);

global.fetch = jest.fn((url: string) => {
  if (url === `${Global.backendBaseUrl}canciones/${songName}`) {
    return Promise.resolve({
      json: () => songMockFetch,
      status: 200,
    }).catch((error) => {
      console.log(error);
    });
  }
  if (url === `${Global.backendBaseUrl}canciones/dto/${songName}`) {
    return Promise.resolve({
      json: () => songMockFetch,
      status: 200,
    }).catch((error) => {
      console.log(error);
    });
  }
  if (url === `${Global.backendBaseUrl}canciones/${songName}/numberOfPlays`) {
    return Promise.resolve({
      json: () => {},
      status: 204,
    }).catch((error) => {
      console.log(error);
    });
  }
  if (
    url ===
    `${Global.backendBaseUrl}usuarios/${userName}/historial?nombre_cancion=${songName}`
  ) {
    return Promise.resolve({
      json: () => {},
      status: 204,
    }).catch((error) => {
      console.log(error);
    });
  }

  // In case the URL doesn't match, return a rejected promise
  return Promise.reject(new Error('Unhandled URL in fetch mock'));
}) as jest.Mock;

jest
  .spyOn(window.HTMLMediaElement.prototype, 'play')
  .mockImplementation(jest.fn());

jest
  .spyOn(window.HTMLMediaElement.prototype, 'pause')
  .mockImplementation(jest.fn());

/* const mockAudioPlay = jest
  .spyOn(window.HTMLMediaElement.prototype, 'play')
  .mockImplementation(jest.fn());

const mockAudioPause = jest
  .spyOn(window.HTMLMediaElement.prototype, 'pause')
  .mockImplementation(jest.fn()); */

test('Render Player', async () => {
  let component;

  await act(async () => {
    component = render(
      <PlayerStreaming
        volume={0}
        songName={songName}
        changeSongInfo={jest.fn()}
      />,
    );
  });

  expect(component).toBeTruthy();
});
