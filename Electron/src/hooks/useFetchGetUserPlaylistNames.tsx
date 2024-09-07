import { useState, useEffect } from 'react';
import { UsersService } from '../swagger/api/services/UsersService';

const useFetchGetUserPlaylistNames = (username: string) => {
  const [playlistNames, setPlaylistNames] = useState<string[]>();
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const data =
          await UsersService.getUserPlaylistsNamesUsersNamePlaylistNamesGet(
            username,
          );
        setPlaylistNames(data);
        setLoading(false);
      } catch (err) {
        console.log(err);
        setError('Unable to get user playlist names');
        setPlaylistNames([]);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [username]);

  return { playlistNames, loading, error };
};

export default useFetchGetUserPlaylistNames;
