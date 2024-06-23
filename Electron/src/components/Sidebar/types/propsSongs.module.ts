export interface PropsSongs {
  name: string;
  playlistName: string;
  artistName: string;
  index: number;
  duration: number;
  streams: number;
  handleSongCliked: Function;
  /* Refresh data on playlist menu after a modification */
  refreshPlaylistData: Function;
  refreshSidebarData: Function;
}
