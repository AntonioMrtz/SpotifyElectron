import { createContext, useContext, useState, ReactNode, useMemo } from 'react';
import Global from 'global/global';

// type of context state
interface SongNameContextType {
  songName: string;
  changeSongName: (newSongName: string) => void;
}

// Create the context for songname and change song name
const SongNameContext = createContext<SongNameContextType | undefined>(
  undefined,
);

// Define the provider component
export function SongNameChangeContextProvider({
  children,
}: {
  children: ReactNode;
}) {
  const [songName, setSongName] = useState<string>(Global.noSongPlaying);

  const changeSongName = (newSongName: string) => {
    setSongName(newSongName);
  };

  const value = useMemo<SongNameContextType>(() => {
    return { songName, changeSongName };
  }, [songName]);

  return (
    <SongNameContext.Provider value={value}>
      {children}
    </SongNameContext.Provider>
  );
}

// A custom hook for easy access for song
export const useSongNameChangeContext = () => {
  const context = useContext(SongNameContext);

  if (!context) {
    throw new Error(
      'useSongNameChangeContext must be used within a SongNameProvider',
    );
  }

  return context;
};
