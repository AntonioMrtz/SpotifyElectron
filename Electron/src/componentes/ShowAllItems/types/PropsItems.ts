export interface PropsItems {
  id: string | undefined;
}

export interface PropsItemsPlaylist extends PropsItems {
  refreshSidebarData: Function;
}
