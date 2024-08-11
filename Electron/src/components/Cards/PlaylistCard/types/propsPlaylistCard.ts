export interface PropsPlaylistCard {
  name: string;
  photo: string;
  description: string;
  owner: string;
  refreshSidebarData: () => void;
}
