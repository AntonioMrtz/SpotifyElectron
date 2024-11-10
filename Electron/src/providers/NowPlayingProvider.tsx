import { createContext, useState, ReactNode, useMemo } from 'react';
import Global from 'global/global';

interface NowPlayingContextType {
  songName: string;
  changeSongName: (newSongName: string) => void;
}

export const NowPlayingContext = createContext<
  NowPlayingContextType | undefined
>(undefined);

export function NowPlayingContextProvider({
  children,
}: {
  children: ReactNode;
}) {
  const [songName, setSongName] = useState<string>(Global.noSongPlaying);

  const changeSongName = (newSongName: string) => {
    setSongName(newSongName);
  };

  const value = useMemo<NowPlayingContextType>(() => {
    return { songName, changeSongName };
  }, [songName]);

  return (
    <NowPlayingContext.Provider value={value}>
      {children}
    </NowPlayingContext.Provider>
  );
}
