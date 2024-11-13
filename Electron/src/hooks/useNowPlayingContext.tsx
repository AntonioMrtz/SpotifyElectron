import { NowPlayingContext } from 'providers/NowPlayingProvider';
import { useContext } from 'react';

// A custom hook for easy access for song

export const useNowPlayingContext = () => {
  const context = useContext(NowPlayingContext);

  if (!context) {
    throw new Error(
      'useNowPlayingContext must be used within a NowPlayingContextProvider',
    );
  }

  return context;
};

export default useNowPlayingContext;
