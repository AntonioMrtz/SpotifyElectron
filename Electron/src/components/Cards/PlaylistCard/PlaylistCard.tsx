import { Link, useNavigate } from 'react-router-dom';
import { useState, MouseEvent, useEffect, useRef } from 'react'; // Import useRef
import ContextMenuPlaylist from 'components/AdvancedUIComponents/ContextMenu/Playlist/ContextMenuPlaylist';
import Popover, { PopoverPosition } from '@mui/material/Popover';
import { PropsPlaylistCard } from 'types/playlist';
import styles from '../cards.module.css';
import defaultThumbnailPlaylist from '../../../assets/imgs/DefaultThumbnailPlaylist.jpg';

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
    e.stopPropagation();
    e.preventDefault();
    handlePlay();
  };

  const handleClickArtist = (event: any) => {
    event.preventDefault();
    event.stopPropagation();
    navigate(`/user/${owner}`);
  };

  /* Context Menu */

  const [anchorPosition, setAnchorPosition] = useState<{
    top: number;
    left: number;
  } | null>(null);

  const open = Boolean(anchorPosition);
  const id = open ? 'parent-popover' : undefined;

  // Ref to hold the timeout ID
  const closeTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  const handleOpenContextMenu = (event: MouseEvent<HTMLDivElement>) => {
    // Clear any pending close timeout when opening
    if (closeTimeoutRef.current) {
      clearTimeout(closeTimeoutRef.current);
      closeTimeoutRef.current = null;
    }
    setAnchorPosition({
      top: event.clientY,
      left: event.clientX,
    });
  };

  const handleCloseContextMenu = () => {
    // Directly close without delay for clickAway/escape
    setAnchorPosition(null);
  };

  const handlePopoverMouseLeave = () => {
    // Set a timeout to close the popover after a short delay
    closeTimeoutRef.current = setTimeout(() => {
      setAnchorPosition(null);
    }, 200); // 200ms delay, adjust as needed
  };

  const handlePopoverMouseEnter = () => {
    // Clear the timeout if the mouse re-enters the popover before it closes
    if (closeTimeoutRef.current) {
      clearTimeout(closeTimeoutRef.current);
      closeTimeoutRef.current = null;
    }
  };

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
          // OPTIONAL: If you want the popover to hide when the mouse leaves the *card* image
          // onMouseLeave={handlePopoverMouseLeave}
          // onMouseEnter={handlePopoverMouseEnter} // To keep it open if mouse re-enters card
        >
          <img
            src={photo === '' ? defaultThumbnailPlaylist : photo}
            className="card-img-top rounded"
            alt="playlist thumbnail"
            onError={({ currentTarget }) => {
              currentTarget.onerror = null;
              currentTarget.src = defaultThumbnailPlaylist;
            }}
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
          onClose={handleCloseContextMenu} // This handles click-away and escape key
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
          {/* Wrap ContextMenuPlaylist to detect mouse leave on the popover content */}
          <div
            onMouseLeave={handlePopoverMouseLeave}
            onMouseEnter={handlePopoverMouseEnter}
          >
            <ContextMenuPlaylist
              playlistName={name}
              handleCloseParent={handleCloseContextMenu}
              owner={owner}
              refreshPlaylistData={() => {}}
              refreshSidebarData={refreshSidebarData}
            />
          </div>
        </Popover>
      </div>
    </>
  );
}