import { useEffect, useState, ChangeEvent, useCallback } from 'react';
import Global from 'global/global';
import genreColorsMap from 'utils/genre';
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
  changeSongName: Function;
  refreshSidebar: Function;
}

export default function Explorar({
  changeSongName,
  refreshSidebar,
}: PropsExplorar) {
  /* Searchbar */

  const [filterName, setFilterName] = useState('');

  const [filteredSongs, setFilteredSongs] = useState<PropsSongCard[]>([]);
  const [filteredPlaylists, setFilteredPlaylists] = useState<
    PropsPlaylistCard[]
  >([]);
  const [filteredUsers, setFilteredUsers] = useState<PropsUserCard[]>([]);
  const [filteredArtists, setFilteredArtists] = useState<PropsArtistCard[]>([]);

  const fetchFilteredItemsByName = useCallback(
    async (filterNameInput: string) => {
      try {
        const fetchUrlFilterItemsByName = `${Global.backendBaseUrl}search/?nombre=${filterNameInput}`;
        const resFetchUrlFilterItemsByName = await fetch(
          fetchUrlFilterItemsByName
        );
        const resFetchUrlFilterItemsByNameJson =
          await resFetchUrlFilterItemsByName.json();

        if (resFetchUrlFilterItemsByNameJson.songs) {
          const fetchedSongs: PropsSongCard[] = [];

          resFetchUrlFilterItemsByNameJson.songs
            .slice(0, 4)
            .forEach((songJson: any) => {
              const song = JSON.parse(songJson);
              fetchedSongs.push({
                name: song.name,
                artist: song.artist,
                photo: song.photo,
                refreshSidebarData: refreshSidebar,
                changeSongName,
              });
            });

          setFilteredSongs(fetchedSongs);
        }

        if (resFetchUrlFilterItemsByNameJson.playlists) {
          const fetchedPlaylists: PropsPlaylistCard[] = [];

          resFetchUrlFilterItemsByNameJson.playlists
            .slice(0, 4)
            .forEach((playlistJson: any) => {
              const playlist = JSON.parse(playlistJson);
              fetchedPlaylists.push({
                name: playlist.name,
                photo: playlist.photo,
                description: playlist.description,
                owner: playlist.owner,
                refreshSidebarData: refreshSidebar,
              });
            });

          setFilteredPlaylists(fetchedPlaylists);
        }

        if (resFetchUrlFilterItemsByNameJson.artists) {
          const fetchedArtists: PropsArtistCard[] = [];

          resFetchUrlFilterItemsByNameJson.artists
            .slice(0, 4)
            .forEach((artistJson: any) => {
              const artist = JSON.parse(artistJson);
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
            .forEach((userJson: any) => {
              const user = JSON.parse(userJson);
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
    [changeSongName, refreshSidebar]
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

  const [generos, setGeneros] = useState<{}>();

  const getGeneros = async () => {
    fetch(encodeURI(`${Global.backendBaseUrl}generos/`))
      .then((res) => res.json())
      .then(async (res) => {
        setGeneros(res);
        return null;
      })
      .catch(() => console.log('Cannot get genres'));
  };
  useEffect(() => {
    getGeneros();
  }, []);

  return (
    <div className={`container-fluid d-flex flex-column ${styles.principal}`}>
      <div
        className={`container-fluid d-flex flex-column ${styles.columnofGeneros}`}
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
              {generos &&
                Object.values(generos).map((genero) => {
                  return (
                    <GenreCard
                      key={genero as string}
                      name={genero as string}
                      color={genreColorsMap[genero as string]}
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
