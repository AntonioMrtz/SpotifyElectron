import { useState, useEffect } from 'react';
import { PropsPlaylistCard } from 'types/playlist';
import { useSidebar } from 'providers/SidebarProvider';
import defaultThumbnailPlaylist from '../assets/imgs/DefaultThumbnailPlaylist.jpg';
import { PlaylistsService } from '../swagger/api/services/PlaylistsService';

const useFetchGetPlaylists = () => {
  const { refreshSidebarData } = useSidebar();
  const [playlists, setPlaylists] = useState<PropsPlaylistCard[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);

        const data = await PlaylistsService.getPlaylistsPlaylistsGet();

        if (data.playlists) {
          const propsPlaylists: PropsPlaylistCard[] = [];

          data.playlists.forEach((playlist: any) => {
            const propsPlaylist: PropsPlaylistCard = {
              name: playlist.name,
              photo:
                playlist.photo === ''
                  ? defaultThumbnailPlaylist
                  : playlist.photo,
              description: playlist.description,
              refreshSidebarData,
              owner: playlist.owner,
            };

            propsPlaylists.push(propsPlaylist);

            setPlaylists(propsPlaylists);
          });
        }
      } catch (err) {
        console.log(err);
        setError('Unable to get all playlists');
        setPlaylists([]);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [refreshSidebarData]);

  return { playlists, loading, error };
};

export default useFetchGetPlaylists;
