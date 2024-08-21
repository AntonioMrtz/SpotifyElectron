import PlaylistCard from 'components/Cards/PlaylistCard/PlaylistCard';
import useFetchGetPlaylists from 'hooks/useFetchGetPlaylists';
import { PropsItemsPlaylist } from '../types/propsItems';
import defaultThumbnailPlaylist from '../../../assets/imgs/DefaultThumbnailPlaylist.jpg';

export default function ItemsAllPlaylists({
  refreshSidebarData,
}: PropsItemsPlaylist) {
  const { playlists } = useFetchGetPlaylists(refreshSidebarData);

  return (
    // eslint-disable-next-line react/jsx-no-useless-fragment
    <>
      {playlists &&
        playlists.map((playlist) => (
          <PlaylistCard
            name={playlist?.name || 'No Name'}
            photo={playlist?.photo || defaultThumbnailPlaylist}
            description={playlist?.description || 'No Description'}
            owner={playlist?.owner || 'Unknown Owner'}
            key={`${playlist?.name}-${playlist?.owner}`}
            refreshSidebarData={refreshSidebarData}
          />
        ))}
    </>
  );
}
