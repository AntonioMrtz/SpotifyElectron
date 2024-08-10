import { useState, useEffect } from 'react';
import Global from 'global/global';

const useFetchGetUserPlaylistNames = (username: string) => {
  const [playlistNames, setPlaylistNames] = useState<string[]>();
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // TODO only get user created playlists names in one query
    const fetchUserPlaylistNames = async () => {
      try {
        // TODO only one fetch URL
        const fetchGetUserResponse = await fetch(
          `${Global.backendBaseUrl}users/${username}`,
          {
            credentials: 'include',
          },
        );
        const fetchGetUserJson = await fetchGetUserResponse.json();
        const sidebarPlaylistNames = fetchGetUserJson.playlists.join(',');

        const response = await fetch(
          `${Global.backendBaseUrl}playlists/selected/${sidebarPlaylistNames}`,
          {
            credentials: 'include',
          },
        );
        const data = await response.json();
        const playlistNamesFromFetch: string[] = [];

        if (data.playlists) {
          data.playlists.forEach((playlistObject: any) => {
            playlistNamesFromFetch.push(playlistObject.name);
          });
        }
        setPlaylistNames(playlistNamesFromFetch);
        setLoading(false);
      } catch (err) {
        console.log(err);
        setError('Unable to get user playlists names');
        setPlaylistNames([]);
      } finally {
        setLoading(false);
      }
    };
    fetchUserPlaylistNames();
  }, [username]);

  return { playlistNames, loading, error };
};

export default useFetchGetUserPlaylistNames;
