import { useState, useEffect } from 'react';
import Global from 'global/global';

interface SongProps {
  name: string;
  artist: string;
  photo: string;
  duration: string;
  genre: string;
  streams: string;
}

const useFetchGetUser = (username: string) => {
  const [user, setUser] = useState<SongProps | null>(null);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await fetch(
          `${Global.backendBaseUrl}users/${username}`,
        );
        if (!response.ok) {
          throw new Error(`Failed to fetch User ${username}`);
        }

        const data = await response.json();
        const mappedUser: SongProps = {
          name: data.name || '',
          artist: data.artist || '',
          photo: data.photo || '',
          duration: data.duration || '',
          genre: data.genre || '',
          streams: data.streams || '',
        };

        setUser(mappedUser);
      } catch (err) {
        console.log(`Failed to get User ${username}: ${err}`);
      }
    };

    fetchUser();
  }, [username]);

  return { user };
};

export default useFetchGetUser;
