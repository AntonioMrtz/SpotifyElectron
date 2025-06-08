import SongCard from 'components/Cards/SongCard/SongCard';
import useFetchGetArtistSongs from 'hooks/useFetchGetArtistSongs';
import { sanitizeUserName } from 'utils/sanitizeParameters';
import { useSidebar } from 'providers/SidebarProvider';
import { PropsItemsSongsFromArtist } from '../types/PropsItems';

export default function ItemsAllSongsFromArtist({
  artistName, // refreshSidebarData,
}: PropsItemsSongsFromArtist) {
  const { songs } = useFetchGetArtistSongs(sanitizeUserName(artistName));
  const { refreshSidebarData } = useSidebar();

  return (
    // eslint-disable-next-line react/jsx-no-useless-fragment
    <>
      {songs &&
        songs.map((songItem, index) => {
          return (
            <SongCard
              // eslint-disable-next-line react/no-array-index-key
              key={`${songItem.name}${index}`}
              name={songItem.name}
              photo={songItem.photo}
              artist={songItem.artist}
              refreshSidebarData={refreshSidebarData}
            />
          );
        })}
    </>
  );
}
