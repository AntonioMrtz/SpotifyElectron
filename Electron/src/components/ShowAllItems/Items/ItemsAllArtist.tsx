import ArtistCard from 'components/Cards/ArtistCard/ArtistCard';
import useFetchGetArtists from 'hooks/useFetchGetArtists';

export default function ItemsAllArtist() {
  const { artists } = useFetchGetArtists();

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
