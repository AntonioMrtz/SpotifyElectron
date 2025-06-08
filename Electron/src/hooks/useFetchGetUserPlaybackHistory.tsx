import { useState, useEffect } from 'react';
import { UsersService } from 'swagger/api/services/UsersService';
import { PropsSongCard } from 'types/song';

const useFetchGetUserRecentlyPlayed = (userName: string | undefined) => {
  const [recentlyPlayed, setRecentlyPlayed] = useState<PropsSongCard[]>();
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      if (!userName) return;
      setLoading(true);

      try {
        const recentlyPlayedData =
          await UsersService.getUserPlaybackHistoryUsersNamePlaybackHistoryGet(
            userName,
          );
        setRecentlyPlayed(recentlyPlayedData);
      } catch (err) {
        console.log(err);
        setError(`Unable to get recently played from user ${userName}`);
        setRecentlyPlayed([]);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [userName]);

  return { recentlyPlayed, loading, error };
};

export default useFetchGetUserRecentlyPlayed;
