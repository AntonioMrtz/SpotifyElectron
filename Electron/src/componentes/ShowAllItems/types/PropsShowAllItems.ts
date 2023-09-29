export enum ShowAllItemsTypes {
  PLAYLIST = 'playlist',
  ARTIST = 'artist',
  SONG = 'song',
}

export interface PropsAllItems {
  refreshSidebarData: Function;
  type: ShowAllItemsTypes;
}
