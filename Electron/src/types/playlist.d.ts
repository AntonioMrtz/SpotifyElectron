export interface PropsPlaylistCardSidebar {
  name: string;
  photo: string;
  owner: string;
  /* default || selected css class  */
  playlistStyle: string;
  handleUrlPlaylistClicked: Function;
  refreshSidebarData: () => void;
}

export interface PropsPlaylistCard {
  name: string;
  photo: string;
  description: string;
  owner: string;
  refreshSidebarData: () => void;
}
