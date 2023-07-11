import { useState, Fragment } from 'react';
import Box from '@mui/material/Box';
import Modal from '@mui/material/Modal';
import AddSongPlayListAccordion from './Accordion/AddSongPlayListAccordion';
import styles from './modalAddSongPlaylist.module.css';
import PriorityHighIcon from '@mui/icons-material/PriorityHigh';
import CheckIcon from '@mui/icons-material/Check';

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
  enum ModalConfirmationTypes {
    PLAYLIST = 'Playlist',
    SONG = 'Canción',
  }

  enum ModalConfirmationResponse {
    ERROR = 'no se ha podido añadir',
    SUCCESS = 'se ha añadido correctamente',
  }
  /* ADDSONGPLAYLIST MODAL */

  const [open, setOpen] = useState(false);
  const handleOpen = () => setOpen(true);

  const handleClose = () => setOpen(false);

  const handleShowConfirmationModal = (
    type: ModalConfirmationTypes,
    response: ModalConfirmationResponse
  ) => {
    handleOpenConfirmationModal(type, response);
  };

  /* CONFIRMATION MODAL */

  const [modalConfirmationData, setModalConfirmationData] = useState({
    type: '',
    response: '',
  });

  const [openConfirmationModal, setOpenConfirmationModal] = useState(false);
  const handleOpenConfirmationModal = (
    type: ModalConfirmationTypes,
    response: ModalConfirmationResponse
  ) => {
    setOpenConfirmationModal(true);
    setModalConfirmationData({
      type: type,
      response: response,
    });
  };

  const handleCloseConfirmationModal = () => {
    setOpenConfirmationModal(false);
  };

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
            handleShowConfirmationModal={handleShowConfirmationModal}
            reloadSidebar={props.reloadSidebar}
            handleClose={handleClose}
          />
        </Box>
      </Modal>

      {/* Confirmation Modal */}
      <div>
        <Modal
          className={``}
          open={openConfirmationModal}
          onClose={handleCloseConfirmationModal}
          aria-labelledby="modal-modal-title2"
          aria-describedby="modal-modal-description2"
        >
          <Box sx={style} className={`${styles.wrapperConfirmationModal}`}>
            {' '}
            <div className={`${styles.wrapperConfirmationModalHeader}`}>
              <div className={`${styles.wrapperConfirmationModalText}`}>
                <span>
                  {modalConfirmationData.type} {modalConfirmationData.response}
                </span>
                <p>
                  {modalConfirmationData.type} {modalConfirmationData.response}
                </p>
              </div>

              <div className="d-flex container-fluid align-items-center justify-content-center">
                <CheckIcon
                  style={{ color: 'var(--secondary-green)', fontSize: '6rem' }}
                ></CheckIcon>
              </div>
            </div>
            <div className={`container-fluid d-flex flex-column justify-content-flex-end mt-4 ${styles.wrapperButton} `}>
              <button onClick={handleCloseConfirmationModal}>
                Confirmar
              </button>
            </div>
          </Box>
        </Modal>
      </div>
    </Fragment>
  );
}
