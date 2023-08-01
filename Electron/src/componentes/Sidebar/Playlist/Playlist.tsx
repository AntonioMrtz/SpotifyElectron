import styles from './playlist.module.css';
import { PropsPlaylist } from '../types/propsPlaylist.module';
import Popover, { PopoverPosition } from '@mui/material/Popover';
import { useEffect, useState } from 'react';
import ContextMenuPlaylist from '../../ContextMenu/Playlist/ContextMenuPlaylist';

export default function Playlist(props: PropsPlaylist) {


  const handleClickPlaylist = () => {
    props.handleUrlPlaylistClicked(props.name)
  }

  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    if (!isOpen) {
      handleClose();
    }
  }, [isOpen]);

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
    <span
      className={`container-fluid d-flex flex-row ${styles.wrapperPlaylist} ${props.playlistStyle}`}
      onClick={handleClickPlaylist}
      onContextMenu={handleRightClick}
    >
      <img src={props.photo} alt="" className="img-fluid img-border-2" />

      <div className="container-fluid d-flex flex-column p-0 ms-2 " style={{  textOverflow:'ellipsis',overflow:'hidden',
        whiteSpace: 'nowrap'

}}>
        <label>{props.name}</label>
        <p>Lista</p>
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
          }}
        >
          <ContextMenuPlaylist playlistName={props.name} handleClose={handleClose} reloadSidebar={props.reloadSidebar}/>
        </Popover>
      </div>
    </span>


  );
}
