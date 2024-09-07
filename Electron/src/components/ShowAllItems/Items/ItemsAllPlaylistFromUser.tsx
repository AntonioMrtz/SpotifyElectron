import PlaylistCard from 'components/Cards/PlaylistCard/PlaylistCard';
import useFetchGetUserPlaylists from 'hooks/useFetchGetUserPlaylists';
import { PropsItemsPlaylistsFromUser } from '../types/PropsItems';
import defaultThumbnailPlaylist from '../../../assets/imgs/DefaultThumbnailPlaylist.jpg';

export default function ItemsAllPlaylistsFromUser({
  refreshSidebarData,
  userName,
}: PropsItemsPlaylistsFromUser) {
  const { playlists } = useFetchGetUserPlaylists(userName);

  return (
    // eslint-disable-next-line react/jsx-no-useless-fragment
    <>
      {playlists &&
        playlists.map((playlist) => (
          <PlaylistCard
            name={playlist.name}
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
