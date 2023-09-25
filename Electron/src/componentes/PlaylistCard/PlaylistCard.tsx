import { Link, useNavigate } from 'react-router-dom';
import { useState, MouseEvent, useEffect } from 'react';
import ContextMenuPlaylist from 'componentes/AdvancedUIComponents/ContextMenu/Playlist/ContextMenuPlaylist';
import Popover, { PopoverPosition } from '@mui/material/Popover/Popover';
import styles from './playlistCard.module.css';
import { PropsPlaylistCard } from './types/propsPlaylistCard.module';
import defaultThumbnailPlaylist from '../../assets/imgs/DefaultThumbnailPlaylist.jpg';

export default function PlaylistCard({
  name,
  photo,
  owner,
  refreshSidebarData,
}: PropsPlaylistCard) {
  const navigate = useNavigate();

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

  const handleClickArtist = (event: any) => {
    event.preventDefault();
    event.stopPropagation();
    navigate(`/user/${owner}`);
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
    <>
      <Link
        to={urlPlaylist}
        key={urlPlaylist + name}
        className={`rounded ${styles.card}`}
      >
        <div
          className={`${styles.imgContainer}`}
          onContextMenu={handleOpenContextMenu}
        >
          <img
            src={photo === '' ? defaultThumbnailPlaylist : photo}
            className="card-img-top rounded"
            alt="playlist thumbnail"
          />
          <button
            type="button"
            className={`${styles.hoverablePlayButton} ${displayPlay} ${styles.buttonCardPlaylistCard}`}
            onClick={handleButtonClick}
          >
            <i
              className={`fa-solid fa-circle-play ${styles.playButton} ${styles.buttonCardPlaylistCard}`}
            />
          </button>
          <button
            type="button"
            className={`${styles.hoverablePlayButton} ${displayPause} ${styles.buttonCardPlaylistCard}`}
            onClick={handleButtonClick}
          >
            <i
              className={`fa-solid fa-circle-pause ${styles.playButton} ${styles.buttonCardPlaylistCard}`}
            />
          </button>
        </div>
        <div className={`${styles.cardBody}`}>
          <h5 className={`${styles.tituloLista}`}>{name}</h5>
          <button
            type="button"
            onClick={handleClickArtist}
            className={`${styles.autorLista}`}
          >
            {owner}
          </button>
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
            owner={owner}
            refreshPlaylistData={() => {}}
            refreshSidebarData={refreshSidebarData}
          />
        </Popover>
      </div>
    </>
  );
}
