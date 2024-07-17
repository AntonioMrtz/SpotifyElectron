import { useState, useEffect } from 'react';
import Global from 'global/global';
import defaultThumbnailPlaylist from '../assets/imgs/DefaultThumbnailPlaylist.jpg';

interface PropsPlaylistCard {
  name: string;
  photo: string;
  description: string;
  refreshSidebarData: () => void;
  owner: string;
}

const useFetchPlaylists = (refreshSidebarData: () => void) => {
  const [playlists, setPlaylists] = useState<PropsPlaylistCard[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPlaylists = async () => {
      try {
        const response = await fetch(`${Global.backendBaseUrl}playlists/`, {
          credentials: 'include',
        });

        if (!response.ok) {
          throw new Error(`Failed to fetch Playlists`);
        }

        const data = await response.json();
        if (data.playlists) {
          const propsPlaylists: PropsPlaylistCard[] = data.playlists
            .slice(0, 5)
            .map((playlist: any) => ({
              name: playlist.name,
              photo:
                playlist.photo === ''
                  ? defaultThumbnailPlaylist
                  : playlist.photo,
              description: playlist.description,
              refreshSidebarData,
              owner: playlist.owner,
            }));
          setPlaylists(propsPlaylists);
        }
      } catch (err) {
        setError('Failed to fetch playlists');
      } finally {
        setLoading(false);
      }
    };

    fetchPlaylists();
  }, [refreshSidebarData]);

  return { playlists, loading, error };
};

export default useFetchPlaylists;
