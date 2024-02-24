namespace Global {
  export const backendBaseUrl: string = 'http://127.0.0.1:8000/';

  export const repositoryUrl: string =
    'https://github.com/AntonioMrtz/SpotifyElectron/';

  export const noSongPlaying = 'NOSONGPLAYING';

  export interface HandleUrlChangeResponse {
    canGoBack: boolean | undefined;
    canGoForward: boolean | undefined;
  }
}
export default Global;
