import { useNavigate } from 'react-router-dom';
import { getTokenRole, getTokenUsername } from 'utils/token';
import { t } from 'i18next';
import styles from '../contextMenu.module.css';

interface PropsContextMenuProfile {
  handleLogout: Function;
  handleClose: Function;
}

const linkUserTypeMap: Record<string, string> = {
  artist: 'artist',
  user: 'user',
};

export default function ContextMenuProfile({
  handleLogout,
  handleClose,
}: PropsContextMenuProfile) {
  const navigate = useNavigate();

  const handleClickProfile = () => {
    const username = getTokenUsername();
    const type = getTokenRole();
    navigate(`/${linkUserTypeMap[type]}/${username}`);
    handleClose();
  };

  const handleClickLogout = () => {
    handleLogout(false);
  };

  return (
    <div className={` ${styles.wrapperContextMenu}`}>
      <ul>
        <li>
          <button type="button" onClick={handleClickProfile}>
            {t('contextMenuProfile.profile')}
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
