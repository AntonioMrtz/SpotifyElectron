import { useState, useEffect, MouseEvent } from 'react';
import { PropsSongs } from 'components/Sidebar/types/propsSongs';
import ContextMenuSong from 'components/AdvancedUIComponents/ContextMenu/Song/ContextMenuSong';
import Popover, { PopoverPosition } from '@mui/material/Popover';
import { useNavigate } from 'react-router-dom';
import { secondsToMinutesSeconds } from 'utils/date';
import { useSidebar } from 'providers/SidebarProvider';
import styles from '../../pages/Playlist/playlist.module.css';

export default function Song({
  name,
  playlistName,
  artistName,
  index,
  secondsDuration,
  streams,
  handleSongCliked,
  refreshPlaylistData, // refreshSidebarData,
}: PropsSongs) {
  const navigate = useNavigate();
  const { refreshSidebarData } = useSidebar();

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

  const handleClickArtist = () => {
    navigate(`/artist/${artistName}`);
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

        <div>
          <button
            type="button"
            onClick={handleClickArtist}
            className={`${styles.gridItem} ${styles.artistNameContainer} p-0 `}
          >
            {artistName}
          </button>
        </div>
      </span>
      <span className={` d-flex justify-content-end ${styles.gridItem}`}>
        {streams}
      </span>
      <span className={` d-flex justify-content-end ${styles.gridItem}`}>
        {secondsToMinutesSeconds(secondsDuration)}
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
            artistName={artistName}
            playlistName={playlistName}
            handleCloseParent={handleClose}
            refreshPlaylistData={refreshPlaylistData}
            // refreshSidebarData={refreshSidebarData}
          />
        </Popover>
      </div>
    </li>
  );
}
