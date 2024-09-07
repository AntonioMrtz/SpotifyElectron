import { useState, useEffect } from 'react';
import { PropsPlaylistCardSidebar } from 'types/playlist';
import { UsersService } from '../swagger/api/services/UsersService';
import defaultThumbnailPlaylist from '../assets/imgs/DefaultThumbnailPlaylist.jpg';

const useFetchGetUserRelevantPlaylists = (
  userName: string,
  refreshSidebarTriggerValue: boolean,
) => {
  const [playlists, setPlaylists] = useState<PropsPlaylistCardSidebar[]>();
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);

      try {
        const data =
          await UsersService.getUserRelevantPlaylistsUsersNameRelevantPlaylistsGet(
            userName,
          );
        const propsPlaylists: PropsPlaylistCardSidebar[] = [];

        data.forEach((playlist: any) => {
          const propsPlaylist: PropsPlaylistCardSidebar = {
            name: playlist.name,
            photo:
              playlist.photo === '' ? defaultThumbnailPlaylist : playlist.photo,
            owner: playlist.owner,
            handleUrlPlaylistClicked: () => {},
            refreshSidebarData: () => {},

            playlistStyle: '',
          };

          propsPlaylists.push(propsPlaylist);
        });
        setPlaylists(propsPlaylists);
      } catch (err) {
        console.log(err);
        setError('Failed to get user relevant playlists');
        setPlaylists([]);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [userName, refreshSidebarTriggerValue]);

  return { playlists, loading, error };
};

export default useFetchGetUserRelevantPlaylists;
