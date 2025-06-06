import SongArchitecture from './SongArchitecture';

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



  let APP_VERSION = "v1.0.0";
try {
  // Try different paths depending on the environment
  if (typeof window !== 'undefined') {
   const pkg = require('../../package.json');
      APP_VERSION = pkg.version;

      // Set your actual version here
      // please do that
  } else {
   
    try {
      const pkg = require('../../package.json');
      APP_VERSION = pkg.version;
    } catch {
      // If package.json not found, try from project root
      try {
        const pkg = require('../../package.json');
        APP_VERSION = pkg.version;
      } catch {
        // Final fallback
        APP_VERSION = "v1.0.0";
      }
    }
  }
} catch (error) {
  console.warn('Could not load version from package.json, using fallback');
  APP_VERSION = "v1.0.0";
}

export const  APPVERSION = APP_VERSION;
export const GITHUB_REPO = 'https://github.com/AntonioMrtz/SpotifyElectron';
export const APP_WEBSITE = 'https://your-website.com'; // Update
export const DOCS_URL = 'https://your-docs.com'; // Update
}
export default Global;
