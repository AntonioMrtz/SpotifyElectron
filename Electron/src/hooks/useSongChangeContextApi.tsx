import { createContext, useContext, useState, ReactNode } from 'react';
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
export const SongNameChangeContextProvider = ({
  children,
}: {
  children: ReactNode;
}) => {
  const [songName, setSongName] = useState<string>(Global.noSongPlaying);

  const changeSongName = (newSongName: string) => {
    setSongName(newSongName);
  };

  return (
    <SongNameContext.Provider value={{ songName, changeSongName }}>
      {children}
    </SongNameContext.Provider>
  );
};

// A custom hook for easy access for song
export const useSongNameChangeContext = () => {
  return useContext(SongNameContext);
};
