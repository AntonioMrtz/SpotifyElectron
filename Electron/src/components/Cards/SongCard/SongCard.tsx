import { useState, useRef, MouseEvent, useCallback } from 'react'; // Import useCallback
import ContextMenuSong from 'components/AdvancedUIComponents/ContextMenu/Song/ContextMenuSong';
import Popover, { PopoverPosition } from '@mui/material/Popover';
import { useNavigate } from 'react-router-dom';
import { PropsSongCard } from 'types/song';
import { useNowPlayingContext } from 'hooks/useNowPlayingContext';
import styles from '../cards.module.css';
import defaultThumbnailPlaylist from '../../../assets/imgs/DefaultThumbnailPlaylist.jpg';

export default function SongCard({
  name,
  artist,
  photo,
  refreshSidebarData,
}: PropsSongCard) {
  const { changeSongName } = useNowPlayingContext();

  const navigate = useNavigate();

  const handleClickArtist = () => {
    navigate(`/artist/${artist}`);
  };

  const handleClickSong = () => {
    changeSongName(name);
  };

  // State to control the visibility and position of the Popover
  const [anchorPosition, setAnchorPosition] = useState<{
    top: number;
    left: number;
  } | null>(null);

  // Refs for the SongCard div and the popover content
  const songCardRef = useRef<HTMLDivElement>(null);
  const popoverContentRef = useRef<HTMLDivElement>(null); // Ref for the div directly inside the Popover

  // Refs to hold the timeout IDs for opening and closing the menu on hover
  const openTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const closeTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  const open = Boolean(anchorPosition);
  const id = open ? 'parent-popover' : undefined;

  // Centralized function to clear any active close timers
  const clearCloseTimer = useCallback(() => {
    if (closeTimeoutRef.current) {
      clearTimeout(closeTimeoutRef.current);
      closeTimeoutRef.current = null;
    }
  }, []);

  // Centralized function to set a close timer for the *entire* SongCard menu structure
  const setCloseTimer = useCallback(() => {
    clearCloseTimer(); // Clear any existing timer first
    closeTimeoutRef.current = setTimeout(() => {
      const isMouseOverCard = songCardRef.current?.matches(':hover');
      const isMouseOverPopover = popoverContentRef.current?.matches(':hover');


      if (!isMouseOverCard && !isMouseOverPopover) {
        setAnchorPosition(null); // Close the main menu
      } else {
      }
      closeTimeoutRef.current = null; // Reset the timeout ref
    }, 200); // Increased delay for closing, adjust as needed
  }, [clearCloseTimer]);

  // handleClose is for Material-UI's onClose (click-away, escape key)
  // For hover-based closure, we use the custom mouse leave handlers and setCloseTimer.
  const handleClose = useCallback(() => {
    setAnchorPosition(null); // This is the direct close action
    clearCloseTimer(); // Clear any pending timeouts
    if (openTimeoutRef.current) { // Also clear pending open if somehow still active
      clearTimeout(openTimeoutRef.current);
      openTimeoutRef.current = null;
    }
  }, [clearCloseTimer, anchorPosition]); // anchorPosition dependency for logging, not strictly needed for functionality.

  // New handler for mouse entering the SongCard
  const handleMouseEnterCard = useCallback((event: MouseEvent<HTMLDivElement>) => {
    clearCloseTimer(); // Clear any pending close timeouts if the mouse re-enters before closing

    // Clear any previous open timeouts if triggered again
    if (openTimeoutRef.current) {
      clearTimeout(openTimeoutRef.current);
      openTimeoutRef.current = null;
    }

    if (!open && !anchorPosition) { // Ensure it's not already open or opening
      openTimeoutRef.current = setTimeout(() => {
        setAnchorPosition({
          top: event.clientY,
          left: event.clientX,
        });
        openTimeoutRef.current = null; // Reset the timeout ref
      }, 150); // 150ms delay to open, adjust as needed
    }
  }, [open, anchorPosition, clearCloseTimer]);

  // New handler for mouse leaving the SongCard
  const handleMouseLeaveCard = useCallback(() => {
    if (openTimeoutRef.current) {
      clearTimeout(openTimeoutRef.current);
      openTimeoutRef.current = null;
    }
    // Start the close timer with a delay.
    setCloseTimer();
  }, [setCloseTimer]);

  // New handler for mouse entering the Popover content (the context menu)
  const handleMouseEnterPopover = useCallback(() => {
    clearCloseTimer();
    // Also clear any pending open timeout from the card if it was still active (though less likely here)
    if (openTimeoutRef.current) {
      clearTimeout(openTimeoutRef.current);
      openTimeoutRef.current = null;
    }
  }, [clearCloseTimer]);

  // New handler for mouse leaving the Popover content (the context menu)
  const handleMouseLeavePopover = useCallback(() => {
    setCloseTimer();
  }, [setCloseTimer]);

  return (
    <>
      <div
        style={{
          border: 'none',
          backgroundColor: 'transparent',
          textAlign: 'left',
        }}
        key={name + artist}
        className={`rounded ${styles.card}`}
        onDoubleClick={handleClickSong}
        onMouseEnter={handleMouseEnterCard}
        onMouseLeave={handleMouseLeaveCard}
        ref={songCardRef} // Attach ref to the main div
      >
        <div className={`${styles.imgContainer}`}>
          <img
            src={photo === '' ? defaultThumbnailPlaylist : photo}
            className="card-img-top rounded"
            alt="song thumbnail"
            onError={({ currentTarget }) => {
              currentTarget.onerror = null;
              currentTarget.src = defaultThumbnailPlaylist;
            }}
          />
        </div>
        <div className={`${styles.cardBody}`}>
          <h5 className={`${styles.tituloLista}`}>{name}</h5>
          <button
            type="button"
            onClick={handleClickArtist}
            className={`${styles.autorLista}`}
          >
            {artist}
          </button>
        </div>
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
            '& .MuiPopover-root': { // Corrected selector for Popover's actual root
              zIndex: '1000',
            },
          }}
          onMouseEnter={handleMouseEnterPopover}
          onMouseLeave={handleMouseLeavePopover}
        >
          <div ref={popoverContentRef}> {/* Attach ref to the content div */}
            <ContextMenuSong
              songName={name}
              artistName={artist}
              playlistName=""
              handleCloseParent={handleClose}
              refreshPlaylistData={() => {}}
              refreshSidebarData={refreshSidebarData}
            />
          </div>
        </Popover>
      </div>
    </>
  );
}