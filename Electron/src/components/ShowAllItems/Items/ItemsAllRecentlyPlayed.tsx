import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { PropsSongCard } from 'types/song';
import SongCard from 'components/Cards/SongCard/SongCard';
import { UsersService } from 'swagger/api/services/UsersService';
import { PropsItemsPlaylist } from '../types/PropsItems';

export default function ItemsAllRecentlyPlayed({
  refreshSidebarData,
}: PropsItemsPlaylist) {
  const { id } = useParams();
  const [recentlyPlayed, setRecentlyPlayed] = useState<PropsSongCard[]>([]);

  useEffect(() => {
    const loadRecentlyPlayed = async () => {
      if (!id) return;

      try {
        const recentlyPlayedData =
          await UsersService.getUserPlaybackHistoryUsersNamePlaybackHistoryGet(
            id,
          );
        setRecentlyPlayed(recentlyPlayedData);
      } catch (error) {
        console.log(`Unable to get recently played from user ${id}`);
        setRecentlyPlayed([]);
      }
    };

    loadRecentlyPlayed();
  }, [id]);

  return (
    <div className="d-flex flex-row flex-wrap" style={{ gap: '14px' }}>
      {recentlyPlayed &&
        recentlyPlayed.map((songItem, index) => (
          <SongCard
            key={`${songItem.name}-${index}`}
            name={songItem.name}
            photo={songItem.photo}
            artist={songItem.artist}
            refreshSidebarData={refreshSidebarData}
          />
        ))}
    </div>
  );
}
