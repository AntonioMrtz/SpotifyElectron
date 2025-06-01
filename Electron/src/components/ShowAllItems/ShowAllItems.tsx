import { useParams } from 'react-router-dom';
import { JSX } from 'react';
import styles from './showAllItems.module.css';
import ItemsPlaylist from './Items/ItemsAllPlaylists';
import { PropsAllItems, ShowAllItemsTypes } from './types/PropsShowAllItems';
import ItemsArtist from './Items/ItemsAllArtist';
import ItemsAllPlaylistsFromUser from './Items/ItemsAllPlaylistFromUser';
import ItemsAllSongsFromArtist from './Items/ItemsAllSongsFromArtist';

export default function ShowAllItems({
  refreshSidebarData,
  type,
}: PropsAllItems) {
  const { id, user, artist } = useParams();

  // Reverse mapping object
  const itemsDisplayed: Record<ShowAllItemsTypes, JSX.Element> = {
    [ShowAllItemsTypes.ALL_PLAYLISTS]: (
      <ItemsPlaylist id={id} refreshSidebarData={refreshSidebarData} />
    ),
    [ShowAllItemsTypes.ALL_ARTISTS]: <ItemsArtist />,
    [ShowAllItemsTypes.SONG]: <>Rejected</>,
    [ShowAllItemsTypes.ALL_PLAYLIST_FROM_USER]: (
      <ItemsAllPlaylistsFromUser
        userName={user || 'NoUser'}
        refreshSidebarData={refreshSidebarData}
        id={id}
      />
    ),
    [ShowAllItemsTypes.ALL_SONGS_FROM_ARTIST]: (
      <ItemsAllSongsFromArtist
        artistName={artist || 'NoArtist'}
        id={id}
        refreshSidebarData={refreshSidebarData}
      />
    ),
  };

  return (
    <div
      className={`container-fluid d-flex flex-column ${styles.categoryTitle}`}
    >
      <h1>{id}</h1>

      <div
        className={`d-flex container-fluid flex-wrap ${styles.wrapperPlaylists} p-0`}
      >
        {itemsDisplayed[type]}
      </div>
    </div>
  );
}
