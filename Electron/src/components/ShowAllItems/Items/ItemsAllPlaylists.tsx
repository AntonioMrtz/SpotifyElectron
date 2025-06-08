import PlaylistCard from 'components/Cards/PlaylistCard/PlaylistCard';
import useFetchGetPlaylists from 'hooks/useFetchGetPlaylists';
import { PropsItemsPlaylist } from '../types/PropsItems';
import defaultThumbnailPlaylist from '../../../assets/imgs/DefaultThumbnailPlaylist.jpg';
import { useSidebar } from 'providers/SidebarProvider';

export default function ItemsAllPlaylists() {
  const { refreshSidebarData } = useSidebar();
  const { playlists } = useFetchGetPlaylists();

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
