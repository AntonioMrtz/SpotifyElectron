export interface PropsSongs {
  name: string;
  playlistName : string;
  index: number;
  handleSongCliked: Function
  /* Refresh data on playlist menu after a modification */
  refreshPlaylistData: Function
}
