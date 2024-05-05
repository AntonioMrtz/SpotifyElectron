import { useCallback, useEffect, useState } from 'react';
import SongCard, { PropsSongCard } from 'components/Cards/SongCard/SongCard';
import Global from 'global/global';
import { PropsItemsSongsFromArtist } from '../types/PropsItems';

export default function ItemsAllSongsFromArtist({
  artistName,
  changeSongName,
  refreshSidebarData,
}: PropsItemsSongsFromArtist) {
  const [songs, setSongs] = useState<PropsSongCard[]>([]);

  const loadSongsFromArtist = useCallback(async () => {
    const songPromises: Promise<any>[] = [];
    let resFetchGetArtistJson;

    try {
      const fetchURLGetArtist = `${
        Global.backendBaseUrl
      }artists/${artistName.replace(/[^a-zA-Z0-9_]/g, '')}`;

      const resFetchGetArtist = await fetch(fetchURLGetArtist);
      resFetchGetArtistJson = await resFetchGetArtist.json();
    } catch {
      console.log('Unable to get artist data');
      return;
    }

    if (resFetchGetArtistJson.uploaded_songs) {
      resFetchGetArtistJson.uploaded_songs.forEach((songName: string) => {
        songPromises.push(
          new Promise((resolve) => {
            fetch(`${Global.backendBaseUrl}canciones/dto/${songName}`)
              .then((resFetchSongDTO) => {
                return resFetchSongDTO.json();
              })
              .then((resFetchSongDTOJson) => {
                const propsSong: PropsSongCard = {
                  name: resFetchSongDTOJson.name,
                  photo: resFetchSongDTOJson.photo,
                  artist: resFetchSongDTOJson.artist,
                  changeSongName,
                  refreshSidebarData,
                };

                resolve(propsSong);
                return propsSong;
              })
              .catch(() => {
                console.log('Unable to get Songs Data from Artist');
              });
          }),
        );
      });

      Promise.all(songPromises)
        .then((resSongPromises) => {
          setSongs([...resSongPromises]);
          return null;
        })
        .catch(() => {
          console.log('Unable to get Songs Data from Artist');
        });
    }
  }, [artistName, changeSongName, refreshSidebarData]);

  useEffect(() => {
    loadSongsFromArtist();
  }, [loadSongsFromArtist]);

  return (
    // eslint-disable-next-line react/jsx-no-useless-fragment
    <>
      {songs &&
        songs.map((songItem, index) => {
          return (
            <SongCard
              // eslint-disable-next-line react/no-array-index-key
              key={`${songItem.name}${index}`}
              name={songItem.name}
              photo={songItem.photo}
              artist={songItem.artist}
              changeSongName={songItem.changeSongName}
              refreshSidebarData={refreshSidebarData}
            />
          );
        })}
    </>
  );
}
