import { useState, useEffect } from 'react';
import Global from 'global/global';

interface SongProps {
  name: string;
  artist: string;
  photo: string;
  duration: string;
  genre: string;
  streams: string;
}

const useFetchSongsByGenre = (genreName: string) => {
  const [songs, setSongs] = useState<SongProps[]>();

  useEffect(() => {
    const fetchData = async () => {
      const getSongsByGenreUrl = `${Global.backendBaseUrl}songs/genres/${genreName}`;

      try {
        const response = await fetch(getSongsByGenreUrl);
        if (!response.ok) {
          throw new Error(`Failed to fetch Songs by Genre ${genreName}`);
        }

        const resGetSongsByGenreUrlJson = await response.json();
        const songsFromFetch: SongProps[] = resGetSongsByGenreUrlJson.songs.map(
          (song: any) => ({
            name: song.name,
            artist: song.artist,
            photo: song.photo,
            duration: song.seconds_duration,
            genre: song.genre,
            streams: song.streams,
          }),
        );

        setSongs(songsFromFetch);
      } catch (err) {
        console.log(`Failed to get Songs by Genre ${genreName}: ${err}`);
      }
    };

    fetchData();
  }, [genreName]);

  return { songs };
};

export default useFetchSongsByGenre;
