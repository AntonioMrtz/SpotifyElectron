import Modal from '@mui/material/Modal';
import {
  InfoPopoverType,
  PropsInfoPopover,
} from 'componentes/types/InfoPopover';
import { useEffect, useImperativeHandle, useState } from 'react';
import Box from '@mui/material/Box';
import PriorityHighIcon from '@mui/icons-material/PriorityHigh';
import CheckIcon from '@mui/icons-material/Check';
import ContentPasteIcon from '@mui/icons-material/ContentPaste';
import styles from './confirmationModal.module.css';

export default function InfoPopover(props: PropsInfoPopover) {
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

  /* CONFIRMATION MODAL */

  const [openConfirmationModal, setOpenConfirmationModal] = useState(false);

  const handleCloseConfirmationModal = () => {
    setOpenConfirmationModal(false);
    if (props.handleClose) {
      props.handleClose();
    }
  };

  useEffect(() => {
    if (props.triggerOpenConfirmationModal === true) {
      setOpenConfirmationModal((state) => !state);
    }
  }, [props.triggerOpenConfirmationModal]);

  return (
    <div>
      <Modal
        className=""
        open={openConfirmationModal}
        onClose={handleCloseConfirmationModal}
        aria-labelledby="modal-modal-confirmation"
        aria-describedby="modal-modal-confirmation-description"
      >
        <Box sx={style} className={`${styles.wrapperConfirmationModal}`}>
          {' '}
          <div className={`${styles.wrapperConfirmationModalHeader}`}>
            <div className={`${styles.wrapperConfirmationModalText}`}>
              <span>{props.title}</span>
              <p>{props.description}</p>
            </div>

            <div className="d-flex container-fluid align-items-center justify-content-end">
              {props.type === InfoPopoverType.SUCCESS && (
                <CheckIcon
                  style={{
                    color: 'var(--secondary-green)',
                    fontSize: '6rem',
                  }}
                />
              )}

              {props.type === InfoPopoverType.ERROR && (
                <PriorityHighIcon
                  style={{
                    color: 'var(--secondary-green)',
                    fontSize: '6rem',
                  }}
                />
              )}

              {props.type === InfoPopoverType.CLIPBOARD && (
                <ContentPasteIcon
                  style={{
                    color: 'var(--secondary-green)',
                    fontSize: '6rem',
                  }}
                />
              )}
            </div>
          </div>
          <div
            className={`container-fluid d-flex flex-column justify-content-flex-end mt-4 ${styles.wrapperButton} `}
          >
            <button onClick={handleCloseConfirmationModal}>Confirmar</button>
          </div>
        </Box>
      </Modal>
    </div>
  );
}
