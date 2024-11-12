import SongCard from 'components/Cards/SongCard/SongCard';
import useFetchGetUserStreamHistory from 'hooks/useFetchGetUserPlaybackHistory';
import { saniticeUserName } from 'utils/saniticeParameters';
import { PropsItemsSongsStreamHistory } from '../types/PropsItems';

export default function ItemsAllSongsFromStreamHistory({
  refreshSidebarData,
  changeSongName,
  userName,
}: PropsItemsSongsStreamHistory) {
  const { streamHistory } = useFetchGetUserStreamHistory(
    saniticeUserName(userName),
  );

  return (
    // eslint-disable-next-line react/jsx-no-useless-fragment
    <>
      {streamHistory &&
        streamHistory.map((songItem, index) => {
          return (
            <SongCard
              // eslint-disable-next-line react/no-array-index-key
              key={`${songItem.name}-${index}`}
              name={songItem.name}
              photo={songItem.photo}
              artist={songItem.artist}
              changeSongName={changeSongName}
              refreshSidebarData={refreshSidebarData}
            />
          );
        })}
    </>
  );
}
