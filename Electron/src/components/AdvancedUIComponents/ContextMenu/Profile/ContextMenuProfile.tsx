import { useNavigate } from 'react-router-dom';
import { getTokenRole, getTokenUsername } from 'utils/token';
import { t } from 'i18next';
import styles from '../contextMenu.module.css';

interface PropsContextMenuProfile {
  handleLogout: Function;
  handleClose: Function;
  handleOpenAbout: Function; // Add this new prop
}

const linkUserTypeMap: Record<string, string> = {
  artist: 'artist',
  user: 'user',
};

export default function ContextMenuProfile({
  handleLogout,
  handleClose,
  handleOpenAbout, // Add this prop
}: PropsContextMenuProfile) {
  const navigate = useNavigate();

  const handleClickProfile = () => {
    const username = getTokenUsername();
    const type = getTokenRole();
    navigate(`/${linkUserTypeMap[type]}/${username}`);
    handleClose();
  };

  const handleClickAbout = () => {
    handleOpenAbout(); // This will open the AboutModal
    // handleClose() is called in the parent component
  };

  const handleClickLogout = () => {
    handleLogout(false);
  };

  return (
    <div className={styles.wrapperContextMenu}>
      <ul>
        <li>
          <button type="button" onClick={handleClickProfile}>
            {t('contextMenuProfile.profile')}
          </button>
        </li>
        {/* Add the About menu item */}
        <li>
          <button type="button" onClick={handleClickAbout}>
            {t('contextMenuProfile.about')}
          </button>
        </li>
        <li>
          <button type="button" onClick={handleClickLogout}>
            {t('contextMenuProfile.log-out')}
          </button>
        </li>
      </ul>
    </div>
  );
}