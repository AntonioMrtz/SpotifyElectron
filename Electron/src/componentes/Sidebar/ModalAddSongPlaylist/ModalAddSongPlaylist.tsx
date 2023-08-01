import { useState, Fragment } from 'react';
import Box from '@mui/material/Box';
import Modal from '@mui/material/Modal';
import AddSongPlayListAccordion from './Accordion/AddSongPlayListAccordion';
import styles from './modalAddSongPlaylist.module.css';
import PriorityHighIcon from '@mui/icons-material/PriorityHigh';
import CheckIcon from '@mui/icons-material/Check';
import ConfirmationModal from 'componentes/InfoPopover/InfoPopover';

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

export default function ModalAddSongPlaylist(props: PropsModalAddSongPlaylist) {
  /* ADDSONGPLAYLIST MODAL */

  const [open, setOpen] = useState(false);
  const handleOpen = () => setOpen(true);

  const handleClose = () => setOpen(false);

  return (
    <Fragment>
      <button className={`btn`} onClick={handleOpen}>
        <i className="fa-solid fa-plus fa-fw"></i>
      </button>

      {/* AddSongPlaylist Modal */}

      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={style} className={` ${styles.wrapperAccordion}`}>
          <AddSongPlayListAccordion
            reloadSidebar={props.reloadSidebar}
            handleClose={handleClose}
          />
        </Box>
      </Modal>
    </Fragment>
  );
}
