import { useState, useEffect } from 'react';
import defaultThumbnailPlaylist from '../assets/imgs/DefaultThumbnailPlaylist.jpg';
import { ArtistsService } from '../swagger/api/services/ArtistsService';

interface PropsArtistCard {
  name: string;
  photo: string;
}

const useFetchGetArtists = () => {
  const [artists, setArtists] = useState<PropsArtistCard[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await ArtistsService.getArtistsArtistsGet();
        if (data.artists) {
          const propsArtists: PropsArtistCard[] = data.artists.map(
            (artist: any) => ({
              name: artist.name,
              photo:
                artist.photo === '' ? defaultThumbnailPlaylist : artist.photo,
            }),
          );
          setArtists(propsArtists);
        }
      } catch (err) {
        console.log(err);
        setError('Failed to fetch artists');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return { artists, loading, error };
};

export default useFetchGetArtists;
