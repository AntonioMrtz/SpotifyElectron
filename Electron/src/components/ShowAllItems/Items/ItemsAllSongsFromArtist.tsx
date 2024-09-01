import SongCard from 'components/Cards/SongCard/SongCard';
import useFetchGetArtistSongs from 'hooks/useFetchGetArtistSongs';
import { saniticeUserName } from 'utils/saniticeParameters';
import { PropsItemsSongsFromArtist } from '../types/propsItems';

export default function ItemsAllSongsFromArtist({
  artistName,
  changeSongName,
  refreshSidebarData,
}: PropsItemsSongsFromArtist) {
  const { songs } = useFetchGetArtistSongs(saniticeUserName(artistName));

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
              changeSongName={changeSongName}
              refreshSidebarData={refreshSidebarData}
            />
          );
        })}
    </>
  );
}
