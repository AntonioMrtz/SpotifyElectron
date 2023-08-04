import { useState, useEffect } from 'react';
import styles from '../playlist.module.css';
import { PropsSongs } from 'componentes/Sidebar/types/propsSongs.module';
import ContextMenuSong from 'componentes/ContextMenu/Song/ContextMenuSong';
import Popover, { PopoverPosition } from '@mui/material/Popover';
export default function Song(props: PropsSongs) {
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    if (!isOpen) {
      handleClose();
    }
  }, [isOpen]);

  const handleSongClicked = () => {
    props.handleSongCliked(props.name);
  };

  const handleRightClick = (event: React.MouseEvent<HTMLLIElement>) => {
    event.preventDefault();
    setIsOpen(isOpen ? false : true);
    handleClick(event);
  };

  const [anchorPosition, setAnchorPosition] = useState<{
    top: number;
    left: number;
  } | null>(null);

  const handleClick = (event: React.MouseEvent<HTMLLIElement>) => {
    setAnchorPosition({
      top: event.clientY,
      left: event.clientX,
    });
  };

  const handleClose = () => {
    setAnchorPosition(null);
    setIsOpen(false);
  };

  const open = Boolean(anchorPosition);
  const id = open ? 'parent-popover' : undefined;

  return (
    <li
      onDoubleClick={handleSongClicked}
      className={`container-fluid ${styles.gridContainer} align-items-center`}
      onContextMenu={handleRightClick}
    >
      <span className={` ${styles.songNumberTable}`}>{props.index}</span>
      <span className={`  d-flex flex-column`}>
        <span
          className={`${styles.songTitleTable} ${styles.titleContainer} pb-0`}
        >
          {props.name}
        </span>
        <span
          className={`${styles.gridItem} ${styles.artistNameContainer} p-0 `}
        >
          {props.artistName}
        </span>
      </span>
      <span className={` d-flex justify-content-center ${styles.gridItem}`}>
        {secondsToMinutesSeconds(props.duration)}
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
            },'& . MuiPopover-root':{

              zIndex:'1000'
            }
          }}
        >
          <ContextMenuSong
            songName={props.name}
            playlistName={props.playlistName}
            handleClose={handleClose}
            refreshPlaylistData={props.refreshPlaylistData}
          />
        </Popover>
      </div>
    </li>
  );
}

const secondsToMinutesSeconds: Function = (secs: number) => {
  let minutes = Math.floor(secs / 60);
  let seconds = (secs - minutes * 60) / 100;

  return (minutes + seconds).toFixed(2).replace('.', ':');
};
