import { useState, useEffect } from 'react';
import { PropsSongCard } from 'components/Cards/SongCard/SongCard';
import { PropsUserCard } from 'components/Cards/UserCard/types/propsUserCard';
import { PropsArtistCard } from 'components/Cards/ArtistCard/types/propsArtistCard';
import { PropsPlaylistCard } from 'components/Cards/PlaylistCard/types/propsPlaylistCard';
import { SearchService } from '../swagger/api/services/SearchService';

const useFetchSearchItemsByName = (
  name: string,
  refreshSidebarData: () => void,
  changeSongName: (name: string) => void,
) => {
  const [filteredSongs, setFilteredSongs] = useState<PropsSongCard[]>([]);
  const [filteredPlaylists, setFilteredPlaylists] = useState<
    PropsPlaylistCard[]
  >([]);
  const [filteredUsers, setFilteredUsers] = useState<PropsUserCard[]>([]);
  const [filteredArtists, setFilteredArtists] = useState<PropsArtistCard[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);

      try {
        const data = await SearchService.getSearchNameSearchGet(name);
        if (name === '') {
          return;
        }
        if (data.songs) {
          const fetchedSongs: PropsSongCard[] = [];

          data.songs.slice(0, 4).forEach((song: any) => {
            fetchedSongs.push({
              name: song.name,
              artist: song.artist,
              photo: song.photo,
              refreshSidebarData,
              changeSongName,
            });
          });

          setFilteredSongs(fetchedSongs);
        }

        if (data.playlists) {
          const fetchedPlaylists: PropsPlaylistCard[] = [];

          data.playlists.slice(0, 4).forEach((playlist: any) => {
            fetchedPlaylists.push({
              name: playlist.name,
              photo: playlist.photo,
              description: playlist.description,
              owner: playlist.owner,
              refreshSidebarData,
            });
          });

          setFilteredPlaylists(fetchedPlaylists);
        }

        if (data.artists) {
          const fetchedArtists: PropsArtistCard[] = [];

          data.artists.slice(0, 4).forEach((artist: any) => {
            fetchedArtists.push({
              name: artist.name,
              photo: artist.photo,
            });
          });

          setFilteredArtists(fetchedArtists);
        }

        if (data.users) {
          const fetchedUsers: PropsUserCard[] = [];

          data.users.slice(0, 4).forEach((user: any) => {
            fetchedUsers.push({
              name: user.name,
              photo: user.photo,
            });
          });

          setFilteredUsers(fetchedUsers);
        }
      } catch (err) {
        console.log(err);
        setError(`Failed to search items by name ${name}`);
        setFilteredArtists([]);
        setFilteredPlaylists([]);
        setFilteredSongs([]);
        setFilteredUsers([]);
      } finally {
        setLoading(false);
      }
    };
    // Use a timeout to debounce the fetchData call
    const debounceTimeout = setTimeout(() => {
      if (name !== '') {
        fetchData();
      }
    }, 300);

    // Clear the timeout if the component unmounts or if the query changes before the timeout completes
    return () => clearTimeout(debounceTimeout);
  }, [name, changeSongName, refreshSidebarData]);

  return {
    filteredUsers,
    filteredSongs,
    filteredArtists,
    filteredPlaylists,
    loading,
    error,
  };
};

export default useFetchSearchItemsByName;
