import { useNavigate } from 'react-router-dom';
import Token from 'utils/token';
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
    const username = Token.getTokenUsername();
    const type = Token.getTokenRole();
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
            Perfil
          </button>
        </li>
        <li>
          <button type="button" onClick={handleClickLogout}>
            Cerrar sesión
          </button>
        </li>
      </ul>
    </div>
  );
}
