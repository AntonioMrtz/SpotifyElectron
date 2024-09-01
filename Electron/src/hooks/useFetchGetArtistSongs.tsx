import { useState, useEffect } from 'react';
import { ArtistsService } from 'swagger/api/services/ArtistsService';
import { PropsSongCard } from 'types/song';

const useFetchGetArtistSongs = (artistName: string) => {
  const [songs, setSongs] = useState<PropsSongCard[]>();
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);

      try {
        const data =
          await ArtistsService.getArtistSongsArtistsNameSongsGet(artistName);
        setSongs(data);
      } catch (err) {
        console.log(err);
        setError('Failed to get Artist songs');
        setSongs([]);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [artistName]);

  return { songs, loading, error };
};

export default useFetchGetArtistSongs;
