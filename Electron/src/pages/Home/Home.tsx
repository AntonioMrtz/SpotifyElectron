import { useNavigate } from 'react-router-dom';
import LoadingCircle from 'components/AdvancedUIComponents/LoadingCircle/LoadingCircle';
import ArtistCard from 'components/Cards/ArtistCard/ArtistCard';
import styles from './homeCss.module.css';
import PlaylistCard from '../../components/Cards/PlaylistCard/PlaylistCard';
import useFetchGetPlaylists from '../../hooks/useFetchGetPlaylists';
import useFetchGetArtists from '../../hooks/useFetchGetArtists';

interface PropsHome {
  refreshSidebarData: () => void;
}

export default function Home({ refreshSidebarData }: PropsHome) {
  const navigate = useNavigate();

  const { playlists, loading: loadingPlaylists } =
    useFetchGetPlaylists(refreshSidebarData);
  const { artists, loading: loadingArtists } = useFetchGetArtists();

  return (
    <div
      className={`container-fluid d-flex flex-column ${styles.mainContentContainer}`}
    >
      <div
        className={`container-fluid d-flex flex-column ${styles.columnOfListas}`}
      >
        <header
          className={`container-fluid d-flex flex-row ${styles.columnHead}`}
        >
          <div
            className={`container-fluid d-flex ${styles.categoryTitleContainer}`}
          >
            <button
              type="button"
              className={`${styles.categoryTitle}`}
              onClick={() => {
                navigate(`/showAllItemsPlaylist/Especialmente para ti`);
              }}
            >
              {' '}
              Especialmente para ti{' '}
            </button>
          </div>
          <div
            className={`container-fluid d-flex ${styles.mostrarTodoContainer}`}
          >
            <button
              type="button"
              className={`${styles.mostrarTodo}`}
              onClick={() => {
                navigate(`/showAllItemsPlaylist/Especialmente para ti`);
              }}
            >
              Mostrar todos
            </button>
          </div>
        </header>

        <ul className={`container-fluid d-flex flex-row ${styles.row}`}>
          {loadingPlaylists && <LoadingCircle />}
          {!loadingPlaylists &&
            playlists &&
            playlists
              .slice(0, 5)
              .map((playlist) => (
                <PlaylistCard
                  name={playlist.name}
                  photo={playlist.photo}
                  description={playlist.description}
                  owner={playlist.owner}
                  key={playlist.name + playlist.description}
                  refreshSidebarData={refreshSidebarData}
                />
              ))}
        </ul>
      </div>

      <div
        className={`container-fluid d-flex flex-column ${styles.columnOfListas}`}
      >
        <header
          className={`container-fluid d-flex flex-row ${styles.columnHead}`}
        >
          <div
            className={`container-fluid d-flex ${styles.categoryTitleContainer}`}
          >
            <button
              type="button"
              className={`${styles.categoryTitle}`}
              onClick={() => {
                navigate(`/showAllItemsArtist/Artistas recomendados`);
              }}
            >
              Artistas destacados
            </button>
          </div>
          <div
            className={`container-fluid d-flex ${styles.mostrarTodoContainer}`}
          >
            <button
              type="button"
              className={`${styles.mostrarTodo}`}
              onClick={() => {
                navigate(`/showAllItemsArtist/Artistas recomendados`);
              }}
            >
              Mostrar todos
            </button>
          </div>
        </header>

        <section className={`container-fluid d-flex flex-row ${styles.row}`}>
          {loadingArtists && <LoadingCircle />}
          {!loadingArtists &&
            artists &&
            artists
              .slice(0, 5)
              .map((artist) => (
                <ArtistCard
                  name={artist.name}
                  photo={artist.photo}
                  key={artist.name}
                />
              ))}
        </section>
      </div>
    </div>
  );
}
