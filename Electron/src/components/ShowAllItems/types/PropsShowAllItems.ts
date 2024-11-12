export enum ShowAllItemsTypes {
  ALL_PLAYLISTS = 'all-playlists',
  ALL_ARTISTS = 'all-artists',
  ALL_PLAYLIST_FROM_USER = 'all-playlists-from-user',
  ALL_STREAM_HISTORY_FROM_USER = 'all-stream-history-from-user',
  ALL_SONGS_FROM_ARTIST = 'all-songs-from-artist',
  SONG = 'song',
}

export interface PropsAllItems {
  refreshSidebarData: () => void;
  type: ShowAllItemsTypes;
  changeSongName: (songName: string) => void;
}
