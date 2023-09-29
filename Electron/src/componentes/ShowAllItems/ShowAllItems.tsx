import { useParams } from 'react-router-dom';
import styles from './showAllItems.module.css';
import ItemsPlaylist from './Items/ItemsPlaylist';
import { PropsAllItems, ShowAllItemsTypes } from './types/PropsShowAllItems';
import ItemsArtist from './Items/ItemsArtist';

export default function AllPlaylists({
  refreshSidebarData,
  type,
}: PropsAllItems) {
  const { id } = useParams();

  // Reverse mapping object
  const itemsDisplayed: {
    [key in ShowAllItemsTypes]: typeof ItemsPlaylist | any;
  } = {
    [ShowAllItemsTypes.PLAYLIST]: (
      <ItemsPlaylist id={id} refreshSidebarData={refreshSidebarData} />
    ),
    [ShowAllItemsTypes.ARTIST]: <ItemsArtist />,
    [ShowAllItemsTypes.SONG]: 'Rejected',
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
