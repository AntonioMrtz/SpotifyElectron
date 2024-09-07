import { useState, useEffect } from 'react';
import { getGenreFromString } from 'utils/genre';
import { PropsSongCard } from 'types/song';
import { SongsService } from '../swagger/api/services/SongsService';

const useFetchSongsByGenre = (genreName: string) => {
  const [songs, setSongs] = useState<PropsSongCard[]>();
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const data = await SongsService.getSongsByGenreSongsGenresGenreGet(
          getGenreFromString(genreName),
        );
        const songsFromFetch: PropsSongCard[] = data.songs.map((song: any) => ({
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
