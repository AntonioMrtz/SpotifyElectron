export interface PropsContextMenu {
  /* Close the first ContextMenu */
  handleCloseParent: Function;
  /* Refresh data on playlist menu after a modification */
  refreshPlaylistData: Function;
  refreshSidebarData: Function;
}

export interface PropsContextMenuPlaylist extends PropsContextMenu {
  playlistName: string;
  owner: string;
}

export interface PropsContextMenuSong extends PropsContextMenu {
  playlistName: string;
  songName: string;
  artistName: string;
}
