/* eslint-disable jsx-a11y/label-has-associated-control */
import Popover, { PopoverPosition } from '@mui/material/Popover';
import { useEffect, useState, MouseEvent } from 'react';
import ContextMenuPlaylist from 'components/AdvancedUIComponents/ContextMenu/Playlist/ContextMenuPlaylist';
import { PropsPlaylistCardSidebar } from 'types/playlist';
import { t } from 'i18next';
import { useSidebar } from 'providers/SidebarProvider';
import styles from './playlistSidebar.module.css';

export default function PlaylistSidebar({
  name,
  photo,
  owner,
  playlistStyle,
  handleUrlPlaylistClicked, // refreshSidebarData,
}: PropsPlaylistCardSidebar) {
  const handleClickPlaylist = () => {
    handleUrlPlaylistClicked(name);
  };

  const { refreshSidebarData } = useSidebar();

  const [isOpen, setIsOpen] = useState(false);

  console.log('Line number 23:', refreshSidebarData);

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
            owner={owner}
            refreshPlaylistData={() => {}}
            // refreshSidebarData={refreshSidebarData}
          />
        </Popover>
      </div>
    </button>
  );
}
