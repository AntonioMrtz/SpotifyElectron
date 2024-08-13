import { useState, useEffect } from 'react';
import { getGenreFromString } from 'utils/genre';
import { SongsService } from '../swagger/api/services/SongsService';

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
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const data = await SongsService.getSongsByGenreSongsGenresGenreGet(
          getGenreFromString(genreName),
        );
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
        setSongs([]);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [genreName]);

  return { songs, loading, error };
};

export default useFetchSongsByGenre;
