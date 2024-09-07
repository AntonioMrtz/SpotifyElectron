import { useState, useEffect } from 'react';
import { UsersService } from 'swagger/api/services/UsersService';
import { PropsSongCard } from 'types/song';

const useFetchGetUserPlaybackHistory = (userName: string | undefined) => {
  const [playbackHistory, setPlaybackHistory] = useState<PropsSongCard[]>();
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      if (!userName) return;
      setLoading(true);

      try {
        const playbackHistoryData =
          await UsersService.getUserPlaybackHistoryUsersNamePlaybackHistoryGet(
            userName,
          );
        setPlaybackHistory(playbackHistoryData);
      } catch (err) {
        console.log(err);
        setError(`Unable to get playback history from user ${userName}`);
        setPlaybackHistory([]);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [userName]);

  return { playbackHistory, loading, error };
};

export default useFetchGetUserPlaybackHistory;
