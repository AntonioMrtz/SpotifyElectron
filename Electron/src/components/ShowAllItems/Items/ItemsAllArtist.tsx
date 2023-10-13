import { useCallback, useEffect, useState } from 'react';
import { PropsArtistCard } from 'components/Cards/ArtistCard/types/propsArtistCard';
import ArtistCard from 'components/Cards/ArtistCard/ArtistCard';
import Global from 'global/global';
/* import { PropsItems } from '../types/PropsItems';
 */
import defaultThumbnailPlaylist from '../../../assets/imgs/DefaultThumbnailPlaylist.jpg';

export default function ItemsAllArtist() {
  const [artists, setArtists] = useState<PropsArtistCard[]>();

  const handleArtist = useCallback(() => {
    fetch(`${Global.backendBaseUrl}artistas/`)
      .then((resFetchArtistas) => resFetchArtistas.json())
      .then((resFetchArtistasJson) => {
        if (resFetchArtistasJson.artists) {
          const propsArtists: PropsArtistCard[] = [];

          resFetchArtistasJson.artists.forEach((resArtistFetch: any) => {
            const resArtistFetchJson = JSON.parse(resArtistFetch);

            const propsArtist: PropsArtistCard = {
              name: resArtistFetchJson.name,
              photo:
                resArtistFetchJson.photo === ''
                  ? defaultThumbnailPlaylist
                  : resArtistFetchJson.photo,
            };

            propsArtists.push(propsArtist);

            setArtists(propsArtists);
          });
        }
        return null;
      })
      .catch(() => {
        console.log('Unable to get artists');
      });
  }, []);

  useEffect(() => {
    handleArtist();
  }, [handleArtist]);

  return (
    // eslint-disable-next-line react/jsx-no-useless-fragment
    <>
      {artists &&
        artists.map((artist) => (
          <ArtistCard
            name={artist?.name || 'No Name'}
            photo={artist?.photo || 'default-photo-url'}
            key={`${artist?.name}`}
          />
        ))}
    </>
  );
}
