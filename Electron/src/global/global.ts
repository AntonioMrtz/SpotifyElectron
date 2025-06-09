import SongArchitecture from './SongArchitecture';
// Import package.json using ES6 import
import packageJson from '../../package.json';

namespace Global {
  export const backendBaseUrl: string = 'http://127.0.0.1:8000'; // ! no trailing slash

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

  // Get version from package.json or use fallback
  const APP_VERSION = packageJson?.version
    ? `v${packageJson.version}`
    : 'v1.0.0';

  export const APPVERSION = APP_VERSION;
  export const GITHUB_REPO = 'https://github.com/AntonioMrtz/SpotifyElectron';
  export const APP_WEBSITE = 'https://your-website.com'; // Update
  export const DOCS_URL = 'https://your-docs.com'; // Update
}

export default Global;
