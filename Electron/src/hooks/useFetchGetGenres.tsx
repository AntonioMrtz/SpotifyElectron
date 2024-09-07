import { useState, useEffect } from 'react';
import { GenresService } from '../swagger/api/services/GenresService';

const useFetchGetGenres = () => {
  const [genres, setGenres] = useState<{}>();
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);

      try {
        const data = await GenresService.getGenresGenresGet();
        setGenres(data);
      } catch (err) {
        console.log(err);
        setError('Failed to get Genres');
        setGenres([]);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return { genres, loading, error };
};

export default useFetchGetGenres;
