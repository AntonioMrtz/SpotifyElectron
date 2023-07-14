import styles from './contextMenuSong.module.css';
import Popover from '@mui/material/Popover';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import { useEffect, useState } from 'react';

export default function ContextMenuSong() {

  const [isOpen, setIsOpen] = useState(false);

  const [anchorEl, setAnchorEl] = useState(null);

  const handleClick = (event: any) => {
    setAnchorEl(event.currentTarget);
    setIsOpen( isOpen ? false : true)

  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const open = Boolean(anchorEl);
  const id = open ? 'simple-popover' : undefined;


  useEffect(() => {

    if(!isOpen){

      handleClose()
    }

  }, [isOpen])


  return (
    <div className={` ${styles.wrapperContextMenu}`}>
      <ul>
        <li>
          <button>Añadir a la cola</button>
        </li>
        <li>
          <button>Ir a radio de la canción</button>
          <button>Ir al artista</button>
          <button>Ir al álbum</button>
          <button>Mostrar créditos</button>
        </li>
        <li>
          <button>Quitar de canciones que te gustan</button>
          <button>Quitar de esta lista</button>
          <button className='d-flex justify-content-between' onClick={handleClick}>Añadir a la playlist <i className="fa-solid fa-chevron-right"></i>
            <Popover
              id={id}
              open={open}
              anchorEl={anchorEl}
              onClose={handleClose}
              anchorOrigin={{
                vertical: 'center',
                horizontal: 'right',
              }}
              transformOrigin={{
                vertical: 'center',
                horizontal: 'left',
              }}
              sx={{
                '& .MuiPaper-root': {
                  backgroundColor: 'var(--hover-white)',
                },
              }}
            >
                <div
                  className={` ${styles.wrapperContextMenu} ${styles.wrapperContextMenuAddToPlaylist}`}
                >
                  <ul>
                    <li>
                      <button>Buscar una lista</button>
                    </li>
                    <li>
                      <button>Crear lista</button>
                    </li>
                    <li>
                      <button>Playlist 1</button>
                    </li>
                    <li>
                      <button>Playlist 1</button>
                    </li>
                    <li>
                      <button>Playlist 1</button>
                    </li>
                    <li>
                      <button>Playlist 1</button>
                    </li>
                    <li>
                      <button>Playlist 1</button>
                    </li>
                    <li>
                      <button>Playlist 1</button>
                    </li>
                    <li>
                      <button>Playlist 1</button>
                    </li>
                    <li>
                      <button>Playlist 1</button>
                    </li>
                    <li>
                      <button>Playlist 1</button>
                    </li>
                    <li>
                      <button>Playlist 1</button>
                    </li>
                    <li>
                      <button>Playlist 1</button>
                    </li>
                  </ul>
                </div>
            </Popover>
          </button>
        </li>
        <li>
          <button>Compartir</button>
        </li>
      </ul>
    </div>
  );
}
