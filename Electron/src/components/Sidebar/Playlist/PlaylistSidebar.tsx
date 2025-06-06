/* eslint-disable jsx-a11y/label-has-associated-control */
import Popover, { PopoverPosition } from '@mui/material/Popover';
import { useState, MouseEvent, useRef } from 'react';
import ContextMenuPlaylist from 'components/AdvancedUIComponents/ContextMenu/Playlist/ContextMenuPlaylist';
import { PropsPlaylistCardSidebar } from 'types/playlist';
import { t } from 'i18next';
import styles from './playlistSidebar.module.css';

export default function PlaylistSidebar({
  name,
  photo,
  owner,
  playlistStyle,
  handleUrlPlaylistClicked,
  refreshSidebarData,
}: PropsPlaylistCardSidebar) {
  const handleClickPlaylist = () => {
    handleUrlPlaylistClicked(name);
  };

  const [anchorPosition, setAnchorPosition] = useState<{
    top: number;
    left: number;
  } | null>(null);

  // Use separate refs for open and close timeouts to be more explicit
  const openTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const closeTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  const handleClose = () => {
    
    // Attempt to blur the active element immediately before closing
    if (document.activeElement instanceof HTMLElement) {
      document.activeElement.blur();
    }

    // Delay setting anchorPosition to null slightly to ensure blur processes
    // This is the core line that closes the Popover
    setTimeout(() => {
      setAnchorPosition(null); 
    }, 0); 

    // Clear any pending open or close timeouts
    if (openTimeoutRef.current) {
      clearTimeout(openTimeoutRef.current);
      openTimeoutRef.current = null;
    }
    if (closeTimeoutRef.current) {
      clearTimeout(closeTimeoutRef.current);
      closeTimeoutRef.current = null;
    }
  };

  // Handler for mouse entering the playlist item (button)
  const handleMouseEnterButton = (event: MouseEvent<HTMLButtonElement>) => {
    // Clear any pending close timeout if the mouse re-enters before closing
    if (closeTimeoutRef.current) {
      clearTimeout(closeTimeoutRef.current);
      closeTimeoutRef.current = null;
    }
    // Only open if not already scheduled to open
    if (!openTimeoutRef.current && !anchorPosition) { // Ensure it's not already open or opening
      openTimeoutRef.current = setTimeout(() => {
        setAnchorPosition({
          top: event.clientY,
          left: event.clientX,
        });
        openTimeoutRef.current = null; // Reset the timeout ref
      }, 50); // Small delay for opening
    }
  };

  // Handler for mouse leaving the playlist item (button)
  const handleMouseLeaveButton = () => {
    // Clear any pending open timeout if the mouse leaves before it triggers
    if (openTimeoutRef.current) {
      clearTimeout(openTimeoutRef.current);
      openTimeoutRef.current = null;
    }
    // Schedule the close with a delay
    if (!closeTimeoutRef.current) { // Prevent multiple close schedules
      closeTimeoutRef.current = setTimeout(() => {
          handleClose();
          closeTimeoutRef.current = null; // Reset the timeout ref
      }, 100); // 100ms grace period before closing
    }
  };

  // Handler for mouse entering the Popover content (the context menu itself)
  const handleMouseEnterPopover = () => {
    // If the mouse moves from the button into the popover, cancel any pending close timeout.
    if (closeTimeoutRef.current) {
      clearTimeout(closeTimeoutRef.current);
      closeTimeoutRef.current = null;
    }
    // Also clear any pending open timeout from the button if it was still active
    if (openTimeoutRef.current) {
      clearTimeout(openTimeoutRef.current);
      openTimeoutRef.current = null;
    }
  };

  // Handler for mouse leaving the Popover content (the context menu itself)
  const handleMouseLeavePopover = () => {
    // Schedule the close with a delay when leaving the popover.
    if (!closeTimeoutRef.current) { // Prevent multiple close schedules
      closeTimeoutRef.current = setTimeout(() => {
          handleClose();
          closeTimeoutRef.current = null; // Reset the timeout ref
      }, 100); // 100ms grace period before closing
    }
  };

  const open = Boolean(anchorPosition);
  const id = open ? 'parent-popover' : undefined;

  return (
    <button
      type="button"
      className={`container-fluid d-flex flex-row ${styles.wrapperPlaylist} ${playlistStyle}`}
      onClick={handleClickPlaylist}
      onMouseEnter={handleMouseEnterButton} 
      onMouseLeave={handleMouseLeaveButton} 
      data-testid="sidebar-playlist-wrapper"
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
        <p style={{ textAlign: 'start' }}>{t('common.playlist')}</p>
      </div>
      <div>
        <Popover
          id={id}
          open={open}
          onClose={handleClose} // This handles closing if you click outside the popover
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
            '.MuiPopover-root': { // Corrected selector for Popover's actual root
              zIndex: '1000',
            },
          }}
          onMouseEnter={handleMouseEnterPopover} 
          onMouseLeave={handleMouseLeavePopover} 
        >
          <ContextMenuPlaylist
            playlistName={name}
            handleCloseParent={handleClose} 
            owner={owner}
            refreshPlaylistData={() => {}} 
            refreshSidebarData={refreshSidebarData}
          />
        </Popover>
      </div>
    </button>
  );
}