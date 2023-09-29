import { useCallback, useEffect, useState } from 'react';
import { PropsPlaylistCard } from 'componentes/Cards/PlaylistCard/types/propsPlaylistCard';
import PlaylistCard from 'componentes/Cards/PlaylistCard/PlaylistCard';
import Global from 'global/global';
import { PropsItemsPlaylist } from '../types/PropsItems';
import defaultThumbnailPlaylist from '../../../assets/imgs/DefaultThumbnailPlaylist.jpg';

export default function ItemsPlaylist({
  refreshSidebarData,
}: PropsItemsPlaylist) {
  const [playlists, setPlaylists] = useState<PropsPlaylistCard[]>();

  const handlePlaylists = useCallback(() => {
    fetch(`${Global.backendBaseUrl}playlists/`, {
      headers: { 'Access-Control-Allow-Origin': '*' },
    })
      .then((resFetchPlaylists) => resFetchPlaylists.json())
      .then((resFetchPlaylistsJson) => {
        if (resFetchPlaylistsJson.playlists) {
          const propsPlaylists: PropsPlaylistCard[] = [];

          resFetchPlaylistsJson.playlists.forEach((resPlaylistFetch: any) => {
            const resPlaylistFetchJson = JSON.parse(resPlaylistFetch);

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
          });
        }
        return null;
      })
      .catch(() => {
        console.log('No se pudieron obtener las playlists');
      });
  }, [refreshSidebarData]);

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
