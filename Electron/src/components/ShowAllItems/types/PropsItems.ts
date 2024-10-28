export interface PropsItems {
  id: string | undefined;
}

export interface PropsItemsPlaylist extends PropsItems {
  refreshSidebarData: () => void;
}

export interface PropsItemsPlaylistsFromUser extends PropsItemsPlaylist {
  userName: string;
}

export interface PropsItemsSongsFromArtist extends PropsItems {
  artistName: string;
  refreshSidebarData: () => void;
  changeSongName?: (songName: string) => void;
}
