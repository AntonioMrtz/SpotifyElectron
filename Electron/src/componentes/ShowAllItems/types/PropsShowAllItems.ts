export enum ShowAllItemsTypes {
  ALL_PLAYLISTS = 'all-playlists',
  ALL_ARTISTS = 'all-artists',
  ALL_PLAYLIST_FROM_USER = 'all-playlists-from-user',
  SONG = 'song',
}

export interface PropsAllItems {
  refreshSidebarData: Function;
  type: ShowAllItemsTypes;
}
