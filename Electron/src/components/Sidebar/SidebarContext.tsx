import React, {
  createContext,
  useContext,
  useState,
  useCallback,
  useMemo,
  ReactNode,
} from 'react';

// Define the shape of the context
interface SidebarContextProps {
  refreshSidebarData: () => void;
  sidebarData: any; // You can replace 'any' with a more specific type if you know the shape of the data
}

// Define the props for SidebarProvider, which includes 'children'
interface SidebarProviderProps {
  children: ReactNode; // ReactNode is the correct type for children in React components
}

// Create the context with an empty default value
const SidebarContext = createContext<SidebarContextProps | undefined>(
  undefined,
);

// SidebarProvider component that wraps around the application or components that need sidebar data
export function SidebarProvider({ children }: SidebarProviderProps) {
  // Changed to function declaration
  const [sidebarData, setSidebarData] = useState<any>(null);

  // A function to refresh the sidebar data
  const refreshSidebarData = useCallback(() => {
    // Here you would add your logic to refresh the sidebar data
    console.log('Sidebar data refreshed');

    // Dummy data for demonstration purposes. Replace this with actual data-fetching logic.
    const newData = {
      playlists: ['Playlist 1', 'Playlist 2', 'Playlist 3'],
      userInfo: {
        username: 'user123',
        email: 'user123@example.com',
      },
    };

    // Update the state with the new data
    setSidebarData(newData);
  }, []);

  // Memoize the value object
  const value = useMemo(
    () => ({ refreshSidebarData, sidebarData }),
    [refreshSidebarData, sidebarData],
  );

  return (
    <SidebarContext.Provider value={value}>{children}</SidebarContext.Provider>
  );
}

// Hook to access the sidebar context
export const useSidebar = () => {
  const context = useContext(SidebarContext);
  if (!context) {
    throw new Error('useSidebar must be used within a SidebarProvider');
  }
  return context;
};
