import { useEffect, useState, ChangeEvent, useCallback } from 'react';
import Global from 'global/global';
import { genreColorsMapping } from 'utils/genre';
import SongCard, { PropsSongCard } from 'components/Cards/SongCard/SongCard';
import { PropsPlaylistCard } from 'components/Cards/PlaylistCard/types/propsPlaylistCard';
import { PropsUserCard } from 'components/Cards/UserCard/types/propsUserCard';
import { PropsArtistCard } from 'components/Cards/ArtistCard/types/propsArtistCard';
import PlaylistCard from 'components/Cards/PlaylistCard/PlaylistCard';
import ArtistCard from 'components/Cards/ArtistCard/ArtistCard';
import UserCard from 'components/Cards/UserCard/UserCard';
import styles from './explorar.module.css';
import GenreCard from '../../components/Cards/GenreCard/GenreCard';

interface PropsExplorar {
  changeSongName: (songName: string) => void;
  refreshSidebarData: () => void;
}

export default function Explorar({
  changeSongName,
  refreshSidebarData,
}: PropsExplorar) {
  const [filterName, setFilterName] = useState('');

  const [filteredSongs, setFilteredSongs] = useState<PropsSongCard[]>([]);
  const [filteredPlaylists, setFilteredPlaylists] = useState<
    PropsPlaylistCard[]
  >([]);
  const [filteredUsers, setFilteredUsers] = useState<PropsUserCard[]>([]);
  const [filteredArtists, setFilteredArtists] = useState<PropsArtistCard[]>([]);

  const fetchFilteredItemsByName = useCallback(
    async (filterNameInput: string) => {
      if (filterNameInput === '') {
        return;
      }
      try {
        const fetchUrlFilterItemsByName = `${Global.backendBaseUrl}/search/?name=${filterNameInput}`;
        const resFetchUrlFilterItemsByName = await fetch(
          fetchUrlFilterItemsByName,
          {},
        );
        const resFetchUrlFilterItemsByNameJson =
          await resFetchUrlFilterItemsByName.json();

        if (resFetchUrlFilterItemsByNameJson.songs) {
          const fetchedSongs: PropsSongCard[] = [];

          resFetchUrlFilterItemsByNameJson.songs
            .slice(0, 4)
            .forEach((song: any) => {
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

        if (resFetchUrlFilterItemsByNameJson.playlists) {
          const fetchedPlaylists: PropsPlaylistCard[] = [];

          resFetchUrlFilterItemsByNameJson.playlists
            .slice(0, 4)
            .forEach((playlist: any) => {
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

        if (resFetchUrlFilterItemsByNameJson.artists) {
          const fetchedArtists: PropsArtistCard[] = [];

          resFetchUrlFilterItemsByNameJson.artists
            .slice(0, 4)
            .forEach((artist: any) => {
              fetchedArtists.push({
                name: artist.name,
                photo: artist.photo,
              });
            });

          setFilteredArtists(fetchedArtists);
        }

        if (resFetchUrlFilterItemsByNameJson.users) {
          const fetchedUsers: PropsUserCard[] = [];

          resFetchUrlFilterItemsByNameJson.users
            .slice(0, 4)
            .forEach((user: any) => {
              fetchedUsers.push({
                name: user.name,
                photo: user.photo,
              });
            });

          setFilteredUsers(fetchedUsers);
        }
      } catch (error) {
        console.log(`Unable to get filtered items | ${error}`);
      }
    },
    [changeSongName, refreshSidebarData],
  );

  useEffect(() => {
    // Use a timeout to debounce the fetchData call
    const debounceTimeout = setTimeout(() => {
      if (filterName !== '') {
        fetchFilteredItemsByName(filterName);
      }
    }, 300); // Adjust the debounce time as needed (e.g., 300 milliseconds)

    // Clear the timeout if the component unmounts or if the query changes before the timeout completes
    return () => clearTimeout(debounceTimeout);
  }, [fetchFilteredItemsByName, filterName]);

  const handleChangeSearchBar = (event: ChangeEvent<HTMLInputElement>) => {
    fetchFilteredItemsByName(event.target.value?.trim());
    setFilterName(event.target.value?.trim());
  };

  /* Genres */

  const [genres, setGenres] = useState<{}>();

  const getGenres = async () => {
    try {
      const fetchGetGenresResponse = await fetch(
        encodeURI(`${Global.backendBaseUrl}/genres/`),
        {},
      );
      const GenresJson = await fetchGetGenresResponse.json();
      setGenres(GenresJson);
    } catch (error) {
      console.log('Cannot get genres');
      setGenres([]);
    }
  };
  useEffect(() => {
    getGenres();
  }, []);

  return (
    <div className={`container-fluid d-flex flex-column ${styles.principal}`}>
      <div
        className={`container-fluid d-flex flex-column ${styles.columnofGenres}`}
      >
        <header className="container-fluid d-flex flex-row mb-4">
          <div className={`d-flex ${styles.searchBarWrapper}`}>
            <i className="me-2 fa-solid fa-magnifying-glass fa-fw" />
            <input
              type="text"
              placeholder="¿Qué te apetece escuchar?"
              className={`${styles.inputSearchBar}`}
              onChange={handleChangeSearchBar}
              data-testid="explorar-input-searchbar"
            />
          </div>
        </header>
        {filterName && (
          <>
            {filteredSongs.length > 0 && (
              <div className="container-fluid d-flex flex-column mb-5">
                <header className="container-fluid d-flex flex-row">
                  <div
                    className={`container-fluid d-flex ${styles.columnTitle}`}
                  >
                    <h4>Canciones</h4>
                  </div>
                </header>
                <div
                  className={`container-fluid d-flex flex-row ${styles.cardContainer}`}
                  style={{ gap: '14px' }}
                >
                  {filteredSongs.map((song) => (
                    <SongCard
                      name={song.name}
                      artist={song.artist}
                      photo={song.photo}
                      refreshSidebarData={song.refreshSidebarData}
                      changeSongName={song.changeSongName}
                      key={`${song.name}${song.artist}`}
                    />
                  ))}
                </div>
              </div>
            )}
            {filteredPlaylists.length > 0 && (
              <div className="container-fluid d-flex flex-column mb-5">
                <header className="container-fluid d-flex flex-row">
                  <div
                    className={`container-fluid d-flex ${styles.columnTitle}`}
                  >
                    <h4>Playlists</h4>
                  </div>
                </header>
                <div
                  className={`container-fluid d-flex flex-row ${styles.cardContainer}`}
                  style={{ gap: '14px' }}
                >
                  {filteredPlaylists.map((playlist) => (
                    <PlaylistCard
                      name={playlist.name}
                      photo={playlist.photo}
                      description={playlist.description}
                      owner={playlist.owner}
                      refreshSidebarData={playlist.refreshSidebarData}
                      key={`${playlist.name}${playlist.owner}`}
                    />
                  ))}
                </div>
              </div>
            )}
            {filteredArtists.length > 0 && (
              <div className="container-fluid d-flex flex-column mb-5">
                <header className="container-fluid d-flex flex-row">
                  <div
                    className={`container-fluid d-flex ${styles.columnTitle}`}
                  >
                    <h4>Artistas</h4>
                  </div>
                </header>
                <div
                  className={`container-fluid d-flex flex-row ${styles.cardContainer}`}
                  style={{ gap: '14px' }}
                >
                  {filteredArtists.map((artist) => (
                    <ArtistCard
                      name={artist.name}
                      photo={artist.photo}
                      key={`${artist.name}${artist.photo}`}
                    />
                  ))}
                </div>
              </div>
            )}
            {filteredUsers.length > 0 && (
              <div className="container-fluid d-flex flex-column mb-5">
                <header className="container-fluid d-flex flex-row">
                  <div
                    className={`container-fluid d-flex ${styles.columnTitle}`}
                  >
                    <h4>Usuarios</h4>
                  </div>
                </header>
                <div
                  className={`container-fluid d-flex flex-row ${styles.cardContainer}`}
                  style={{ gap: '14px' }}
                >
                  {filteredUsers.map((user) => (
                    <UserCard
                      name={user.name}
                      photo={user.photo}
                      key={`${user.name}${user.photo}`}
                    />
                  ))}
                </div>
              </div>
            )}
          </>
        )}
        {!filterName && (
          <>
            <header className="container-fluid d-flex flex-row">
              <div className={`container-fluid d-flex ${styles.columnTitle}`}>
                <h4>Explorar Todo</h4>
              </div>
            </header>
            <div
              className={`container-fluid d-flex flex-row ${styles.cardContainer}`}
            >
              {genres &&
                Object.values(genres).map((genre) => {
                  return (
                    <GenreCard
                      key={genre as string}
                      name={genre as string}
                      color={genreColorsMapping[genre as string]}
                    />
                  );
                })}
            </div>
          </>
        )}
      </div>
    </div>
  );
}
