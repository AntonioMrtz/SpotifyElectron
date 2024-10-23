// Import React if you're using JSX syntax

export enum ShowAllItemsTypes {
  ALL_PLAYLISTS = 'ALL_PLAYLISTS',
  ALL_ARTISTS = 'ALL_ARTISTS',
  ALL_PLAYLIST_FROM_USER = 'ALL_PLAYLIST_FROM_USER',
  ALL_SONGS_FROM_ARTIST = 'ALL_SONGS_FROM_ARTIST',
  SONG = 'SONG', // Added SONG type
}

export interface PropsAllItems {
  refreshSidebarData: () => void;
  type: ShowAllItemsTypes;
  changeSongName: (songName: string) => void;
}
