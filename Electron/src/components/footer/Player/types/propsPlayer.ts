import { PropsSongInfo } from 'components/footer/SongInfo/types/propsSongInfo';

export interface PropsPlayer {
  volume: number;
  songName: string;
  changeSongInfo: (data: PropsSongInfo) => void;
}
