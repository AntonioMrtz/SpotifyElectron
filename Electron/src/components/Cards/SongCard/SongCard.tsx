import { useEffect, useState } from 'react';
import ContextMenuSong from 'components/AdvancedUIComponents/ContextMenu/Song/ContextMenuSong';
import Popover, { PopoverPosition } from '@mui/material/Popover';
import { useNavigate } from 'react-router-dom';
import styles from '../cards.module.css';
import defaultThumbnailPlaylist from '../../../assets/imgs/DefaultThumbnailPlaylist.jpg';

export interface PropsSongCard {
  name: string;
  artist: string;
  photo: string;
  refreshSidebarData: () => void;
  changeSongName: Function;
}

export default function SongCard({
  name,
  artist,
  photo,
  refreshSidebarData,
  changeSongName,
}: PropsSongCard) {
  const navigate = useNavigate();

  const handleClickArtist = () => {
    navigate(`/artist/${artist}`);
  };

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
      <div
        style={{
          border: 'none',
          backgroundColor: 'transparent',
          textAlign: 'left',
        }}
        key={name + artist}
        className={`rounded ${styles.card}`}
        onDoubleClick={handleClickSong}
        onContextMenu={handleRightClick}
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
            '& . MuiPopover-root': {
              zIndex: '1000',
            },
          }}
        >
          <ContextMenuSong
            songName={name}
            artistName={artist}
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
