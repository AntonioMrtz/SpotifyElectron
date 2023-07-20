namespace Global {
  export let backendBaseUrl: string = "http://127.0.0.1:8000/";
  export let repositoryUrl : string = "https://github.com/AntonioMrtz/SpotifyElectron/"

  export interface HandleUrlChangeResponse {

    canGoBack : boolean | undefined,
    canGoForward : boolean | undefined
  }
}

export default Global;
