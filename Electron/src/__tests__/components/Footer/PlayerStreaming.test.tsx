import '@testing-library/jest-dom';
import '@testing-library/jest-dom/extend-expect';
import { render } from '@testing-library/react';
import PlayerStreaming from 'components/footer/Player/PlayerStreaming';
import Global from 'global/global';
import UserType from 'utils/role';
import { act } from 'react-test-renderer';
import getMockHeaders from 'utils/mockHeaders';

import * as TokenModule from 'utils/token';

const songName = 'songName';
const userName = 'prueba';
const roleUser = UserType.USER;

const songMockFetch = {
  name: songName,
  artist: userName,
  photo: 'photo',
  seconds_duration: '180',
  genre: 'Rock',
  streams: 2,
  url: 'https://5b44cf20b0388.streamlock.net:8443/vod/smil:bbb.smil/playlist.m3u8',
};

jest.spyOn(TokenModule, 'getTokenUsername').mockReturnValue(userName);
jest.spyOn(TokenModule, 'getTokenRole').mockReturnValue(roleUser);

global.fetch = jest.fn((url: string) => {
  if (url === `${Global.backendBaseUrl}/songs/${songName}`) {
    return Promise.resolve({
      json: () => songMockFetch,
      status: 200,
      ok: true,
      headers: getMockHeaders(),
    }).catch((error) => {
      console.log(error);
    });
  }
  if (url === `${Global.backendBaseUrl}/songs/metadata/${songName}`) {
    return Promise.resolve({
      json: () => songMockFetch,
      status: 200,
      ok: true,
      headers: getMockHeaders(),
    }).catch((error) => {
      console.log(error);
    });
  }
  if (url === `${Global.backendBaseUrl}/songs/${songName}/streams`) {
    return Promise.resolve({
      json: () => {},
      status: 204,
      ok: true,
      headers: getMockHeaders(),
    }).catch((error) => {
      console.log(error);
    });
  }
  if (
    url ===
    `${Global.backendBaseUrl}/users/${userName}/playback_history?song_name=${songName}`
  ) {
    return Promise.resolve({
      json: () => {},
      status: 204,
      ok: true,
      headers: getMockHeaders(),
    }).catch((error) => {
      console.log(error);
    });
  }

  // In case the URL doesn't match, return a rejected promise
  return Promise.reject(new Error(`Unhandled URL in fetch mock: ${url}`));
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
