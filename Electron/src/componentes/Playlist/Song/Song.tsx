import { useState, useEffect, MouseEvent } from 'react';
import { PropsSongs } from 'componentes/Sidebar/types/propsSongs.module';
import ContextMenuSong from 'componentes/AdvancedUIComponents/ContextMenu/Song/ContextMenuSong';
import Popover, { PopoverPosition } from '@mui/material/Popover';
import styles from '../playlist.module.css';

const secondsToMinutesSeconds: Function = (secs: number) => {
  const minutes = Math.floor(secs / 60);
  const seconds = (secs - minutes * 60) / 100;

  return (minutes + seconds).toFixed(2).replace('.', ':');
};

export default function Song({
  name,
  playlistName,
  artistName,
  index,
  duration,
  handleSongCliked,
  refreshPlaylistData,
  refreshSidebarData,
}: PropsSongs) {
  const [isOpen, setIsOpen] = useState(false);
  const [anchorPosition, setAnchorPosition] = useState<{
    top: number;
    left: number;
  } | null>(null);
  const handleClose = () => {
    setAnchorPosition(null);
    setIsOpen(false);
  };

  useEffect(() => {
    if (!isOpen) {
      handleClose();
    }
  }, [isOpen]);

  const handleSongClicked = () => {
    handleSongCliked(name);
  };

  const handleRightClick = (event: MouseEvent<HTMLLIElement>) => {
    event.preventDefault();
    setIsOpen(!isOpen);
    setAnchorPosition({
      top: event.clientY,
      left: event.clientX,
    });
  };

  const open = Boolean(anchorPosition);
  const id = open ? 'parent-popover' : undefined;

  return (
    <li
      onDoubleClick={handleSongClicked}
      className={`container-fluid ${styles.gridContainer} align-items-center`}
      onContextMenu={handleRightClick}
    >
      <span className={` ${styles.songNumberTable}`}>{index}</span>
      <span className={`  d-flex flex-column`}>
        <span
          className={`${styles.songTitleTable} ${styles.titleContainer} pb-0`}
        >
          {name}
        </span>
        <span
          className={`${styles.gridItem} ${styles.artistNameContainer} p-0 `}
        >
          {artistName}
        </span>
      </span>
      <span className={` d-flex justify-content-center ${styles.gridItem}`}>
        {secondsToMinutesSeconds(duration)}
      </span>

      <div>
        <Popover
          id={id}
          open={open}
          onClose={handleClose}
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
          <ContextMenuSong
            songName={name}
            playlistName={playlistName}
            handleCloseParent={handleClose}
            refreshPlaylistData={refreshPlaylistData}
            refreshSidebarData={refreshSidebarData}
          />
        </Popover>
      </div>
    </li>
  );
}
