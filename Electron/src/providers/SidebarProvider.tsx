import React, { createContext, useContext, useState, useEffect } from 'react';

interface SidebarContextType {
  refreshSidebarData: () => void;
}

const SidebarContext = createContext<SidebarContextType | undefined>(undefined);

export function SidebarProvider({ children }: { children: React.ReactNode }) {
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const refreshSidebarData = () => {
    setRefreshTrigger((prev) => prev + 1);
  };

  useEffect(() => {
    // Any side effects that need to run when refreshTrigger changes
    console.log('Sidebar data refreshed');
  }, [refreshTrigger]);

  return (
    <SidebarContext.Provider value={{ refreshSidebarData }}>
      {children}
    </SidebarContext.Provider>
  );
}

export function useSidebar() {
  const context = useContext(SidebarContext);
  if (context === undefined) {
    throw new Error('useSidebar must be used within a SidebarProvider');
  }
  return context;
}
