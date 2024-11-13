export interface PropsSongCard {
  name: string;
  artist: string;
  photo: string;
  refreshSidebarData: () => void;
}

interface SongMetadata {
  name: string;
  artist: string;
  photo: string;
  duration: string;
  genre: string;
  streams: string;
}
