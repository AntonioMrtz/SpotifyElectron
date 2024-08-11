import { useState, useEffect } from 'react';
import Global from 'global/global';

const useFetchGetUserPlaylistNames = (username: string) => {
  const [playlistNames, setPlaylistNames] = useState<string[]>();
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchUserPlaylistNames = async () => {
      try {
        const response = await fetch(
          `${Global.backendBaseUrl}users/${username}/playlist_names`,
          {
            credentials: 'include',
          },
        );
        if (!response.ok) {
          throw new Error(`Failed to fetch user playlist names`);
        }

        const data = await response.json();
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
    fetchUserPlaylistNames();
  }, [username]);

  return { playlistNames, loading, error };
};

export default useFetchGetUserPlaylistNames;
