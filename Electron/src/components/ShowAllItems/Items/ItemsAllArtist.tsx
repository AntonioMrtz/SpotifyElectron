import { useCallback, useEffect, useState } from 'react';
import { PropsArtistCard } from 'components/Cards/ArtistCard/types/propsArtistCard';
import ArtistCard from 'components/Cards/ArtistCard/ArtistCard';
import Global from 'global/global';
import defaultThumbnailPlaylist from '../../../assets/imgs/DefaultThumbnailPlaylist.jpg';

export default function ItemsAllArtist() {
  const [artists, setArtists] = useState<PropsArtistCard[]>();

  const handleArtist = useCallback(async () => {
    try {
      const fetchGetArtistsResponse = await fetch(
        `${Global.backendBaseUrl}/artists/`,
        {
          credentials: 'include',
        },
      );
      const fetchGetArtistsJson = await fetchGetArtistsResponse.json();
      if (fetchGetArtistsJson.artists) {
        const propsArtists: PropsArtistCard[] = [];

        fetchGetArtistsJson.artists.forEach((resArtistFetchJson: any) => {
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
    } catch (error) {
      console.log('Unable to get all artists');
      setArtists([]);
    }
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
