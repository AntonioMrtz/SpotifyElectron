import Footer from 'components/footer/Footer';
import ScrollToTop from 'components/helpers/ScrollToTop';
import Sidebar from 'components/Sidebar/Sidebar';
import StickyHeader from 'components/StickyHeader/StickyHeader';
import { Outlet } from 'react-router-dom';
import styles from 'layout/layout.module.css';

// TODO must go. Context providers?
export interface LayoutContextProps {
  // TODO can sidebar data be reloaded using another way?
  refreshSidebarData: () => void;
  refreshSidebarTriggerValue: boolean;
  handleLogout: () => void;
}

export function Layout({
  refreshSidebarTriggerValue,
  refreshSidebarData,
  handleLogout,
}: LayoutContextProps) {
  return (
    <div className={`App d-flex flex-column ${styles.appBackground}`}>
      <ScrollToTop />
      <StickyHeader handleLogout={handleLogout} />
      <div className="d-flex">
        <Sidebar
          refreshSidebarTriggerValue={refreshSidebarTriggerValue}
          refreshSidebarData={refreshSidebarData}
        />
        <div
          className={`App d-flex container-fluid ${styles.mainContentWrapper}`}
        >
          <Outlet />
        </div>
      </div>
      <Footer />
    </div>
  );
}
