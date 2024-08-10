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
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const getSongsByGenreURL = `${Global.backendBaseUrl}songs/genres/${genreName}`;
        const response = await fetch(getSongsByGenreURL, {
          credentials: 'include',
        });
        if (!response.ok) {
          throw new Error(`Failed to fetch Songs by Genre ${genreName}`);
        }

        const data = await response.json();
        const songsFromFetch: SongProps[] = data.songs.map((song: any) => ({
          name: song.name,
          artist: song.artist,
          photo: song.photo,
          duration: song.seconds_duration,
          genre: song.genre,
          streams: song.streams,
        }));

        setSongs(songsFromFetch);
      } catch (err) {
        console.log(err);
        setError(`Failed to get Songs by Genre ${genreName}`);
      }
    };

    fetchData();
  }, [genreName]);

  return { songs, error };
};

export default useFetchSongsByGenre;
