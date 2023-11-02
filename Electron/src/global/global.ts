namespace Global {
  export const backendBaseUrl: string =
    'https://spotifyelectron-dev-kzhm.2.ie-1.fl0.io/';
  export const repositoryUrl: string =
    'https://github.com/AntonioMrtz/SpotifyElectron/';

  export const noSong = 'NOSONGPLAYING';

  export interface HandleUrlChangeResponse {
    canGoBack: boolean | undefined;
    canGoForward: boolean | undefined;
  }
}

export default Global;
