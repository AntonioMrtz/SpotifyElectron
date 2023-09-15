/* eslint-disable jsx-a11y/label-has-associated-control */
import Popover, { PopoverPosition } from '@mui/material/Popover';
import { useEffect, useState, MouseEvent } from 'react';
import ContextMenuPlaylist from 'componentes/AdvancedUIComponents/ContextMenu/Playlist/ContextMenuPlaylist';
import styles from './playlist.module.css';
import { PropsPlaylist } from '../types/propsPlaylist.module';

export default function Playlist({
  name,
  photo,
  playlistStyle,
  handleUrlPlaylistClicked,
  reloadSidebar,
}: PropsPlaylist) {
  const handleClickPlaylist = () => {
    handleUrlPlaylistClicked(name);
  };

  const [isOpen, setIsOpen] = useState(false);

  const [anchorPosition, setAnchorPosition] = useState<{
    top: number;
    left: number;
  } | null>(null);

  const handleRightClick = (event: MouseEvent<HTMLButtonElement>) => {
    event.preventDefault();
    setIsOpen(!isOpen);
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

  useEffect(() => {
    if (!isOpen) {
      handleClose();
    }
  }, [isOpen]);

  return (
    <button
      type="button"
      className={`container-fluid d-flex flex-row ${styles.wrapperPlaylist} ${playlistStyle}`}
      onClick={handleClickPlaylist}
      onContextMenu={handleRightClick}
    >
      <img src={photo} alt="" className="img-fluid img-border-2" />

      <div
        className="container-fluid d-flex flex-column p-0 ms-2 justify-content-start"
        style={{
          textOverflow: 'ellipsis',
          overflow: 'hidden',
          whiteSpace: 'nowrap',
        }}
      >
        <label style={{ textAlign: 'start' }}>{name}</label>
        <p style={{ textAlign: 'start' }}>Lista</p>
      </div>
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
          <ContextMenuPlaylist
            playlistName={name}
            handleCloseParent={handleClose}
            refreshPlaylistData={() => {}}
            refreshSidebarData={reloadSidebar}
          />
        </Popover>
      </div>
    </button>
  );
}
