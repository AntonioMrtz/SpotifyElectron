// SidebarContext.tsx
import React, { createContext, useContext, useCallback, useState } from 'react';

// Define the context type
interface SidebarContextType {
  refreshSidebarData: () => void;
  refreshCounter: number; // State variable to track refreshes
}

// Create the context with a default value
const SidebarContext = createContext<SidebarContextType | undefined>(undefined);

// Create a provider component
export const SidebarProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  // State for the refresh counter
  const [refreshCounter, setRefreshCounter] = useState(0);

  // Method to refresh sidebar data
  const refreshSidebarData = useCallback(() => {
    console.log('Sidebar data refreshed');
    // Update the counter which can be used to trigger updates
    setRefreshCounter((prev) => prev + 1);
  }, []);

  return (
    <SidebarContext.Provider value={{ refreshSidebarData, refreshCounter }}>
      {children}
    </SidebarContext.Provider>
  );
};

// Create a custom hook for using the SidebarContext
export const useSidebar = () => {
  const context = useContext(SidebarContext);
  if (!context) {
    throw new Error('useSidebar must be used within a SidebarProvider');
  }
  return context;
};
