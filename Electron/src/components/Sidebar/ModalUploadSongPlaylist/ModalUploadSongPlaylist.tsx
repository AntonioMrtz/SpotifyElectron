import { useState } from 'react';
import Box from '@mui/material/Box';
import Modal from '@mui/material/Modal';
import styles from './modalUploadSongPlaylist.module.css';
import UploadSongPlaylistAccordion from './Accordion/UploadSongPlaylistAccordion';

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

interface PropsModalUploadSongPlaylist {
  refreshSidebarData: () => void;
}

export default function ModalUploadSongPlaylist({
  refreshSidebarData,
}: PropsModalUploadSongPlaylist) {
  /* ADDSONGPLAYLIST MODAL */

  const [open, setOpen] = useState(false);
  const handleOpen = () => setOpen(true);

  const handleClose = () => setOpen(false);

  const [isCloseAllowed, setIsCloseAllowed] = useState(true);

  return (
    <>
      <button type="button" className="btn" onClick={handleOpen}>
        <i className="fa-solid fa-plus fa-fw" />
      </button>

      <Modal
        open={open}
        onClose={isCloseAllowed === true ? handleClose : () => {}}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={style} className={` ${styles.wrapperAccordion}`}>
          <UploadSongPlaylistAccordion
            refreshSidebarData={refreshSidebarData}
            handleClose={handleClose}
            setIsCloseAllowed={setIsCloseAllowed}
          />
        </Box>
      </Modal>
    </>
  );
}
