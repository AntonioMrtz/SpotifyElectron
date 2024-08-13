import { useState, useEffect } from 'react';
import defaultThumbnailPlaylist from '../assets/imgs/DefaultThumbnailPlaylist.jpg';
import { PlaylistsService } from '../swagger/api/services/PlaylistsService';

interface PropsPlaylistCard {
  name: string;
  photo: string;
  description: string;
  refreshSidebarData: () => void;
  owner: string;
}

const useFetchGetPlaylists = (refreshSidebarData: () => void) => {
  const [playlists, setPlaylists] = useState<PropsPlaylistCard[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPlaylists = async () => {
      try {
        const data = await PlaylistsService.getPlaylistsPlaylistsGet();

        if (data.playlists) {
          const propsPlaylists: PropsPlaylistCard[] = [];

          data.playlists
            .slice(0, 5) // TODO get only a portion of total playlists in the query
            .forEach((playlist: any) => {
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
      } finally {
        setLoading(false);
      }
    };

    fetchPlaylists();
  }, [refreshSidebarData]);

  return { playlists, loading, error };
};

export default useFetchGetPlaylists;
