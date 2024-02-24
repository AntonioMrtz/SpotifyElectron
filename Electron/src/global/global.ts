namespace Global {
  export const backendBaseUrl: string =
    process.env.BACKEND_URL || 'no-backend-provided';

  export const repositoryUrl: string =
    'https://github.com/AntonioMrtz/SpotifyElectron/';

  export const noSong = 'NOSONGPLAYING';

  export interface HandleUrlChangeResponse {
    canGoBack: boolean | undefined;
    canGoForward: boolean | undefined;
  }
}

export default Global;
