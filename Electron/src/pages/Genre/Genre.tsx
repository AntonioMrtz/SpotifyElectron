import { useLocation } from 'react-router-dom';
import { genreColorsMapping } from 'utils/genre';
import useFetchSongsByGenre from 'hooks/useFetchGetSongsbyGenre';
import styles from './genre.module.css';
import SongCard from '../../components/Cards/SongCard/SongCard';

interface PropsGenre {
  refreshSidebarData: () => void;
  changeSongName: (songName: string) => void;
}

export default function Genre({
  refreshSidebarData,
  changeSongName,
}: PropsGenre) {
  /* Get current Playlist Name */
  const location = useLocation();
  const genreName = decodeURIComponent(
    location.pathname.split('/').slice(-1)[0],
  );

  const { songs } = useFetchSongsByGenre(genreName);

  return (
    <div className="d-flex flex-column container-fluid p-0">
      <div
        className={`d-flex align-items-end container-fluid ${styles.headerGenre}`}
        style={{
          backgroundColor: `${genreColorsMapping[genreName]}`,
          paddingTop: 'var(--pading-top-sticky-header)',
        }}
      >
        <div className="ms-3" style={{ zIndex: 2 }}>
          <h1>{genreName}</h1>
        </div>
      </div>
      <div
        className={`d-flex container-fluid flex-column ${styles.subheaderGenre}`}
      >
        Canciones del género
      </div>
      <div
        className={`d-flex container-fluid flex-wrap ${styles.songWrapperGenre}`}
      >
        {songs &&
          songs.map((song) => {
            return (
              <SongCard
                key={`${song.name} ${genreName}`}
                name={song.name}
                artist={song.artist}
                photo={song.photo}
                changeSongName={changeSongName}
                refreshSidebarData={refreshSidebarData}
              />
            );
          })}
      </div>
    </div>
  );
}
