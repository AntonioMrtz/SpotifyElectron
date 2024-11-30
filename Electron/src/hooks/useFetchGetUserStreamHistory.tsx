import { useState, useEffect } from 'react';
import { UsersService } from 'swagger/api/services/UsersService';
import { PropsSongCard } from 'types/song';

const useFetchGetUserStreamHistory = (userName: string | undefined) => {
  const [streamHistory, setStreamHistory] = useState<PropsSongCard[]>();
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      if (!userName) return;
      setLoading(true);

      try {
        const streamHistoryData =
          await UsersService.getUserStreamHistoryUsersNameStreamHistoryGet(
            userName,
          );
        setStreamHistory(streamHistoryData);
      } catch (err) {
        console.log(err);
        setError(`Unable to get stream history from user ${userName}`);
        setStreamHistory([]);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [userName]);

  return { streamHistory, loading, error };
};

export default useFetchGetUserStreamHistory;
