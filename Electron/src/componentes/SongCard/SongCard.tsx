import { useEffect, useState } from 'react';
import ContextMenuSong from 'componentes/AdvancedUIComponents/ContextMenu/Song/ContextMenuSong';
import Popover, { PopoverPosition } from '@mui/material/Popover/Popover';
import styles from './songCard.module.css';
import defaultThumbnailPlaylist from '../../assets/imgs/DefaultThumbnailPlaylist.jpg';

export interface PropsSongCard {
  name: string;
  artist: string;
  photo: string;
  refreshSidebarData: Function;
  changeSongName: Function;
}

export default function SongCard({
  name,
  artist,
  photo,
  refreshSidebarData,
  changeSongName,
}: PropsSongCard) {
  const handleClickSong = () => {
    changeSongName(name);
  };

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

  const handleRightClick = (event: any) => {
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
    <>
      <button
        type="button"
        className={`${styles.wrapperSongCardGenre}`}
        onDoubleClick={handleClickSong}
        onContextMenu={handleRightClick}
      >
        <div className={`${styles.wrapperImageCard}`}>
          <img
            className="img-fluid"
            src={photo === '' ? defaultThumbnailPlaylist : photo}
            alt=""
          />
        </div>
        <div className={`${styles.wrapperTextSongGenre}`}>
          <h5>{name}</h5>
          <p>{artist}</p>
        </div>
      </button>

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
            playlistName=""
            handleCloseParent={handleClose}
            refreshPlaylistData={() => {}}
            refreshSidebarData={refreshSidebarData}
          />
        </Popover>
      </div>
    </>
  );
}
