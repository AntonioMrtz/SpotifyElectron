import React, { useState } from 'react';
import Global from 'global/global';
import { useLocation } from 'react-router-dom';
import styles from './genre.module.css';
import Song from './Song/Song';

interface PropsGenre {
  changeSongName: Function;
}

export default function Genre({ changeSongName }: PropsGenre) {
  /* Get current Playlist Name */
  const location = useLocation();
  const genreName = decodeURIComponent(
    location.pathname.split('/').slice(-1)[0]
  );

  type SongProps = {
    name: string;
    artist: string;
    photo: string;
  };

  const [songs, setSongs] = useState<SongProps[]>();

  const handleSongsFromGenre = async () => {};

  return (
    <div className="d-flex flex-column container-fluid p-0">
      <div
        className={`d-flex align-items-end container-fluid ${styles.headerGenre}`}
        style={{
          backgroundColor: `${Global.genreColors[genreName]}`,
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
              <Song
                key={`${song.name} ${genreName}`}
                name={song.name}
                artist={song.artist}
                photo={song.photo}
                changeSongName={changeSongName}
              />
            );
          })}
      </div>
    </div>
  );
}
