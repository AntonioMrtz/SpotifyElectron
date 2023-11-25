namespace Global {
  export const backendBaseUrl: string =
    'https://backend-api-qsyq.onrender.com/';
  export const repositoryUrl: string =
    'https://github.com/AntonioMrtz/SpotifyElectron/';

  export const noSong = 'NOSONGPLAYING';

  export interface HandleUrlChangeResponse {
    canGoBack: boolean | undefined;
    canGoForward: boolean | undefined;
  }
}

export default Global;
