import { useState, Fragment } from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Modal from '@mui/material/Modal';
import PropsAddSongPlayListAccordion from './Accordion/AddSongPlayListAccordion';
import styles from './modal.module.css';

const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: '70svw',
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  p: 2,
};

export default function ModalAddSongPlaylist() {
  const [open, setOpen] = useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  return (
    <Fragment>
      <button className={`btn`} onClick={handleOpen}>
        <i className="fa-solid fa-plus fa-fw"></i>
      </button>
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={style} className={` ${styles.wrapperAccordion}`}>
          <PropsAddSongPlayListAccordion handleClose={handleClose} />
        </Box>
      </Modal>
    </Fragment>
  );
}
