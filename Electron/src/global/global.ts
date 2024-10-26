import SongArchitecture from './SongArchitecture';

namespace Global {
  export const backendBaseUrl: string = 'https://backend-api-qsyq.onrender.com';

  export const repositoryUrl: string =
    'https://github.com/AntonioMrtz/SpotifyElectron/';

  export const noSongPlaying = 'NOSONGPLAYING';
  export const songArchitecture: SongArchitecture =
    SongArchitecture.BLOB_ARCHITECTURE;

  export const coldStartRequestTimeout = 5000;

  export interface HandleUrlChangeResponse {
    canGoBack: boolean | undefined;
    canGoForward: boolean | undefined;
  }
}
export default Global;
