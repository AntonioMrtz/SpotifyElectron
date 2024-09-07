import { useState, useEffect } from 'react';
import { PropsPlaylistCard } from 'types/playlist';
import { UsersService } from '../swagger/api/services/UsersService';
import defaultThumbnailPlaylist from '../assets/imgs/DefaultThumbnailPlaylist.jpg';

const useFetchGetUserPlaylists = (userName: string | undefined) => {
  const [playlists, setPlaylists] = useState<PropsPlaylistCard[]>();
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      if (!userName) return;
      setLoading(true);

      try {
        const data =
          await UsersService.getUserPlaylistsUsersNamePlaylistsGet(userName);
        const propsPlaylists: PropsPlaylistCard[] = [];

        data.forEach((playlist: any) => {
          const propsPlaylist: PropsPlaylistCard = {
            name: playlist.name,
            photo:
              playlist.photo === '' ? defaultThumbnailPlaylist : playlist.photo,
            owner: playlist.owner,
            description: playlist.description,
            refreshSidebarData: () => {},
          };

          propsPlaylists.push(propsPlaylist);
        });
        setPlaylists(propsPlaylists);
      } catch (err) {
        console.log(err);
        setError('Failed to get user playlists');
        setPlaylists([]);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [userName]);

  return { playlists, loading, error };
};

export default useFetchGetUserPlaylists;
