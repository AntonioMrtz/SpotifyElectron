import { Link } from 'react-router-dom';
import { useState, MouseEvent, useEffect } from 'react';
import ContextMenuPlaylist from 'componentes/AdvancedUIComponents/ContextMenu/Playlist/ContextMenuPlaylist';
import Popover, { PopoverPosition } from '@mui/material/Popover/Popover';
import styles from './playlistCss.module.css';
import { PropsPlaylist } from '../types/propsPlaylist.module';

export default function Home({ name, photo, description }: PropsPlaylist) {
  const [displayPlay, setdisplayPlay] = useState(styles.displayTruePlay);
  const [displayPause, setdisplayPause] = useState(styles.displayNonePlay);
  const [Playing, setPlaying] = useState(false);

  const urlPlaylist = `/playlist/${name}`;

  const handlePlay = (): void => {
    if (Playing === false) {
      setdisplayPause(styles.displayTruePlay);
      setdisplayPlay(styles.displayNonePlay);
      setPlaying(true);
    } else {
      setdisplayPlay(styles.displayTruePlay);
      setdisplayPause(styles.displayNonePlay);
      setPlaying(false);
    }
  };

  const handleButtonClick = (e: MouseEvent<HTMLButtonElement>) => {
    e.stopPropagation(); // Detener la propagación del evento de clic
    e.preventDefault();
    handlePlay();
  };

  /* Context Menu */

  const [isOpen, setIsOpen] = useState(false);

  const [anchorPosition, setAnchorPosition] = useState<{
    top: number;
    left: number;
  } | null>(null);

  const open = Boolean(anchorPosition);
  const id = open ? 'parent-popover' : undefined;

  const handleOpenContextMenu = (event: MouseEvent<HTMLDivElement>) => {
    setIsOpen(!isOpen);
    setAnchorPosition({
      top: event.clientY,
      left: event.clientX,
    });
  };

  const handleCloseContextMenu = () => {
    setAnchorPosition(null);
    setIsOpen(false);
  };

  useEffect(() => {
    if (!isOpen) {
      handleCloseContextMenu();
    }
  }, [isOpen]);

  return (
    <span className={`rounded ${styles.card}`}>
      <Link to={urlPlaylist} key={name}>
        <div
          className={`${styles.imgContainer}`}
          onContextMenu={handleOpenContextMenu}
        >
          <img
            src={photo}
            className="card-img-top rounded"
            alt="playlist thumbnail"
          />
          <button
            type="button"
            className={`${styles.hoverablePlayButton} ${displayPlay}`}
            onClick={handleButtonClick}
          >
            <i className={`fa-solid fa-circle-play ${styles.playButton}`} />
          </button>
          <button
            type="button"
            className={`${styles.hoverablePlayButton} ${displayPause}`}
            onClick={handleButtonClick}
          >
            <i className={`fa-solid fa-circle-pause ${styles.playButton}`} />
          </button>
        </div>
        <div className={`${styles.cardBody}`}>
          <h5 className={`${styles.tituloLista}`}>{name}</h5>
          <p className={`${styles.autorLista}`}>{description}</p>
        </div>
      </Link>
      <div>
        <Popover
          id={id}
          open={open}
          onClose={handleCloseContextMenu}
          anchorReference="anchorPosition"
          anchorPosition={anchorPosition as PopoverPosition}
          anchorOrigin={{
            vertical: 'top',
            horizontal: 'left',
          }}
          transformOrigin={{
            vertical: 'top',
            horizontal: 'left',
          }}
          sx={{
            '& .MuiPaper-root': {
              backgroundColor: 'var(--hover-white)',
            },
            '& . MuiPopover-root': {
              zIndex: '1000',
            },
          }}
        >
          <ContextMenuPlaylist
            playlistName={name}
            handleCloseParent={handleCloseContextMenu}
            refreshPlaylistData={() => {}}
          />
        </Popover>
      </div>
    </span>
  );
}
