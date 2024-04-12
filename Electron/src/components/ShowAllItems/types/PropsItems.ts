export interface PropsItems {
  id: string | undefined;
}

export interface PropsItemsPlaylist extends PropsItems {
  refreshSidebarData: Function;
}

export interface PropsItemsPlaylistsFromUser extends PropsItemsPlaylist {
  userName: string;
  userType: string;
}

export interface PropsItemsSongsFromArtist extends PropsItems {
  artistName: string;
  refreshSidebarData: Function;
  changeSongName: Function;
}
