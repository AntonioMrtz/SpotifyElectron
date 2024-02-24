import { useEffect, useState } from 'react';
import Global from 'global/global';
import { useLocation } from 'react-router-dom';
import genreColorsMap from 'utils/genre';
import styles from './genre.module.css';
import SongCard from '../../components/Cards/SongCard/SongCard';

interface PropsGenre {
  refreshSidebarData: Function;
  changeSongName: Function;
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

  type SongProps = {
    name: string;
    artist: string;
    photo: string;
    duration: string;
    genre: string;
    number_of_plays: string;
  };

  const [songs, setSongs] = useState<SongProps[]>();

  const handleSongsFromGenre = () => {
    const getSongsByGenreUrl = `${Global.backendBaseUrl}canciones/generos/${genreName}`;

    fetch(getSongsByGenreUrl)
      .then((resGetSongsByGenreUrl) => {
        return resGetSongsByGenreUrl.json();
      })
      .then((resGetSongsByGenreUrlJson) => {
        const songsFromFetch: SongProps[] = [];
        resGetSongsByGenreUrlJson.songs.forEach((song: any) => {
          const songParsed = JSON.parse(song);

          const songProp: SongProps = {
            name: songParsed.name,
            artist: songParsed.artist,
            photo: songParsed.photo,
            duration: songParsed.duration,
            genre: songParsed.genre,
            number_of_plays: songParsed.number_of_plays,
          };

          songsFromFetch.push(songProp);
        });

        setSongs(songsFromFetch);
        return null;
      })
      .catch(() => {
        console.log('Couldnt get Songs by Genre');
      });
  };

  useEffect(() => {
    handleSongsFromGenre();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="d-flex flex-column container-fluid p-0">
      <div
        className={`d-flex align-items-end container-fluid ${styles.headerGenre}`}
        style={{
          backgroundColor: `${genreColorsMap[genreName]}`,
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
