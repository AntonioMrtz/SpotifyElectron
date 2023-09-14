import { useState } from 'react';
import Box from '@mui/material/Box';
import Modal from '@mui/material/Modal';
import styles from './modalAddSongPlaylist.module.css';
import AddSongPlayListAccordion from './Accordion/AddSongPlayListAccordion';

const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: '50svw',
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  p: 2,
};

interface PropsModalAddSongPlaylist {
  reloadSidebar: Function;
}

export default function ModalAddSongPlaylist({
  reloadSidebar,
}: PropsModalAddSongPlaylist) {
  /* ADDSONGPLAYLIST MODAL */

  const [open, setOpen] = useState(false);
  const handleOpen = () => setOpen(true);

  const handleClose = () => setOpen(false);

  return (
    <>
      <button type="button" className="btn" onClick={handleOpen}>
        <i className="fa-solid fa-plus fa-fw" />
      </button>

      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={style} className={` ${styles.wrapperAccordion}`}>
          <AddSongPlayListAccordion
            reloadSidebar={reloadSidebar}
            handleClose={handleClose}
          />
        </Box>
      </Modal>
    </>
  );
}
