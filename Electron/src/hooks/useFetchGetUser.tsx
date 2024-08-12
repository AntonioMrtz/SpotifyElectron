import { useState, useEffect } from 'react';
import { UsersService } from '../swagger/api/services/UsersService';

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
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const data = await UsersService.getUserUsersNameGet(username);
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
        console.log(err);
        setError(`Failed to get User ${username}`);
      }
    };

    fetchUser();
  }, [username]);

  return { user, error };
};

export default useFetchGetUser;
