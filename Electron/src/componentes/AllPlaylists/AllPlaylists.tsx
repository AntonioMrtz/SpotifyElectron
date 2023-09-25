import { useParams } from 'react-router-dom';
import { useCallback, useEffect, useState } from 'react';
import Global from 'global/global';
import { PropsPlaylistCard } from 'componentes/PlaylistCard/types/propsPlaylistCard.module';
import PlaylistCard from 'componentes/PlaylistCard/PlaylistCard';
import styles from './allPlaylists.module.css';
import defaultThumbnailPlaylist from '../../assets/imgs/DefaultThumbnailPlaylist.jpg';

interface PropsAllPlaylists {
  refreshSidebarData: Function;
}

export default function AllPlaylists({
  refreshSidebarData,
}: PropsAllPlaylists) {
  const { id } = useParams();

  const [playlists, setPlaylists] = useState<PropsPlaylistCard[]>();

  const handlePlaylists = useCallback(() => {
    fetch(`${Global.backendBaseUrl}playlists/`, {
      headers: { 'Access-Control-Allow-Origin': '*' },
    })
      .then((resFetchPlaylists) => resFetchPlaylists.json())
      .then((resFetchPlaylistsJson) => {
        if (resFetchPlaylistsJson.playlists) {
          const propsPlaylists: PropsPlaylistCard[] = [];

          resFetchPlaylistsJson.playlists.forEach((resPlaylistFetch: any) => {
            const resPlaylistFetchJson = JSON.parse(resPlaylistFetch);

            const propsPlaylist: PropsPlaylistCard = {
              name: resPlaylistFetchJson.name,
              photo:
                resPlaylistFetchJson.photo === ''
                  ? defaultThumbnailPlaylist
                  : resPlaylistFetchJson.photo,
              description: resPlaylistFetchJson.description,
              refreshSidebarData,
              owner: resPlaylistFetchJson.owner,
            };

            propsPlaylists.push(propsPlaylist);

            setPlaylists(propsPlaylists);
          });
        }
        return null;
      })
      .catch((error) => {
        console.log(error);
        console.log('No se pudieron obtener las playlists');
      });
  }, [refreshSidebarData]);

  useEffect(() => {
    handlePlaylists();
  }, [handlePlaylists, id]);

  return (
    <div
      className={`container-fluid d-flex flex-column ${styles.categoryTitle}`}
    >
      <h1>{id}</h1>

      <div
        className={`d-flex container-fluid flex-wrap ${styles.wrapperPlaylists} p-0`}
      >
        {playlists &&
          playlists.map((playlist) => {
            return (
              <PlaylistCard
                name={playlist.name}
                photo={playlist.photo}
                description={playlist.description}
                owner={playlist.owner}
                key={playlist.name + playlist.description}
                refreshSidebarData={refreshSidebarData}
              />
            );
          })}
      </div>
    </div>
  );
}
