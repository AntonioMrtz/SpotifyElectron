import { useCallback, useEffect, useState } from 'react';
import { PropsPlaylistCard } from 'components/Cards/PlaylistCard/types/propsPlaylistCard';
import PlaylistCard from 'components/Cards/PlaylistCard/PlaylistCard';
import Global from 'global/global';
import { PropsItemsPlaylistsFromUser } from '../types/PropsItems';
import defaultThumbnailPlaylist from '../../../assets/imgs/DefaultThumbnailPlaylist.jpg';

export default function ItemsAllPlaylistsFromUser({
  refreshSidebarData,
  userName,
}: PropsItemsPlaylistsFromUser) {
  const [playlists, setPlaylists] = useState<PropsPlaylistCard[]>();

  const handlePlaylists = useCallback(async () => {
    const playlistNames: string[] = [];

    try {
      const fetchUrlPlaylistFromUser = `${Global.backendBaseUrl}users/${userName}`;

      const resFetchUrlPlaylistFromUser = await fetch(
        fetchUrlPlaylistFromUser,
        {
          credentials: 'include',
        },
      );
      const resFetchUrlPlaylistFromUserJson =
        await resFetchUrlPlaylistFromUser.json();

      playlistNames.push(resFetchUrlPlaylistFromUserJson.playlists.join(','));
    } catch {
      console.log('Unable to get user data');
      return;
    }

    fetch(`${Global.backendBaseUrl}playlists/selected/${playlistNames}`, {
      credentials: 'include',
    })
      .then((resFetchPlaylists) => resFetchPlaylists.json())
      .then((resFetchPlaylistsJson) => {
        if (resFetchPlaylistsJson.playlists) {
          const propsPlaylists: PropsPlaylistCard[] = [];

          resFetchPlaylistsJson.playlists.forEach(
            (resPlaylistFetchJson: any) => {
              const propsPlaylist: PropsPlaylistCard = {
                name: resPlaylistFetchJson.name,
                photo:
                  resPlaylistFetchJson.photo === ''
                    ? defaultThumbnailPlaylist
                    : resPlaylistFetchJson.photo,
                description: resPlaylistFetchJson.description,
                refreshSidebarData,
                owner: resPlaylistFetchJson.owner,
              };

              propsPlaylists.push(propsPlaylist);

              setPlaylists(propsPlaylists);
            },
          );
        }
        return null;
      })
      .catch(() => {
        console.log('No se pudieron obtener las playlists');
      });
  }, [refreshSidebarData, userName]);

  useEffect(() => {
    handlePlaylists();
  }, [handlePlaylists]);

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
