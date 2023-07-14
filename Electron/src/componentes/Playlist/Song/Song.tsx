import {useState,useEffect} from 'react';
import styles from '../playlist.module.css';
import { PropsSongs } from 'componentes/Sidebar/types/propsSongs.module';
import ContextMenuSong from 'componentes/ContextMenuSong/ContextMenuSong';
import Popover, { PopoverPosition } from '@mui/material/Popover';
import Typography from '@mui/material/Typography';

export default function Song(props: PropsSongs) {

  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {

    console.log(isOpen)


    if(!isOpen){

      handleClose()
    }

  }, [isOpen])




  const handleSongClicked = () => {
    props.handleSongCliked(props.name);
  };

  const handleRightClick = (event: React.MouseEvent<HTMLLIElement>) => {
    event.preventDefault();
    setIsOpen( isOpen ? false : true)
    handleClick(event);

  };

  const [anchorPosition, setAnchorPosition] = useState<{ top: number; left: number } | null>(null);

  const handleClick = (event: React.MouseEvent<HTMLLIElement>) => {
    setAnchorPosition({
      top: event.clientY,
      left: event.clientX,
    });
  };

  const handleClose = () => {
    setAnchorPosition(null);
  };

  const open = Boolean(anchorPosition);
  const id = open ? 'simple-popover' : undefined;

  return (
    <li
      onDoubleClick={handleSongClicked}
      className={`container-fluid ${styles.gridContainer}`}
      onContextMenu={handleRightClick}
    >
      <span className={` ${styles.songNumberTable}`}>{props.index}</span>
      <span className={` ${styles.songTitleTable}`}>{props.name}</span>
      <span className={` ${styles.gridItem}`}>2:01</span>

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
          <Typography sx={{ m: 0, p: 0 }}>
            <ContextMenuSong />
          </Typography>
        </Popover>
      </div>
    </li>
  );
}
