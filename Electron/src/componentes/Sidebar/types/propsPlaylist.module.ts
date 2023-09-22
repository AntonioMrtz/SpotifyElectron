export interface PropsPlaylist {
  name: string;
  photo: string;
  owner : string;
  /* default || selected css class  */
  playlistStyle: string;
  handleUrlPlaylistClicked: Function;
  reloadSidebar: Function;
}
