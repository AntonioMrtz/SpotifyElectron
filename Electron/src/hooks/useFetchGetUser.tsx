import { useState, useEffect } from 'react';
import { UserProps } from 'types/user';
import { UsersService } from '../swagger/api/services/UsersService';

const useFetchGetUser = (username: string) => {
  const [user, setUser] = useState<UserProps | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const data = await UsersService.getUserUsersNameGet(username);
        const mappedUser: UserProps = {
          name: data.name || '',
          photo: data.photo || '',
          register_date: data.register_date || '',
          recently_played: data.recently_played || [],
          saved_playlists: data.saved_playlists || [],
          playlists: data.playlists || [],
        };

        setUser(mappedUser);
      } catch (err) {
        console.log(err);
        setError(`Failed to get User ${username}`);
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [username]);

  return { user, loading, error };
};

export default useFetchGetUser;
