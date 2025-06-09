import Popover from '@mui/material/Popover';
import { useCallback, useEffect, useReducer, useState } from 'react';
import Global from 'global/global';
import { useNavigate } from 'react-router-dom';
import LoadingCircle from 'components/AdvancedUIComponents/LoadingCircle/LoadingCircle';
import InfoPopover from 'components/AdvancedUIComponents/InfoPopOver/InfoPopover';
import { InfoPopoverType } from 'components/AdvancedUIComponents/InfoPopOver/types/InfoPopover';
import { getTokenUsername } from 'utils/token';
import useFetchGetUserPlaylistNames from 'hooks/useFetchGetUserPlaylistNames';
import { PlaylistsService } from 'swagger/api';
import { t } from 'i18next';
import styles from '../contextMenu.module.css';
import { PropsContextMenuPlaylist } from '../types/propsContextMenu';

interface ConfirmationMenuData {
  title: string;
  type: InfoPopoverType;
  description: string;
}

enum ConfirmationMenuActionKind {
  ADD_SUCCESS = 'ADD_SUCCESS',
  ADD_ERROR = 'ADD_ERROR',
  DELETE_SUCCESS = 'DELETE_SUCCESS',
  DELETE_ERROR = 'DELETE_ERROR',
  CLIPBOARD = 'CLIPBOARD',
}

// An interface for our actions
interface ConfirmationMenuAction {
  type: ConfirmationMenuActionKind;
}

// An interface for our state
interface ConfirmationMenuState {
  payload: ConfirmationMenuData;
}

const reducerConfirmationMenu = (
  state: ConfirmationMenuState,
  action: ConfirmationMenuAction,
): ConfirmationMenuState => {
  switch (action.type) {
    case ConfirmationMenuActionKind.ADD_SUCCESS:
      return {
        payload: {
          type: InfoPopoverType.SUCCESS,
          title: t('contextMenuPlaylist.confirmationMenu.add-success.title'),
          description: t(
            'contextMenuPlaylist.confirmationMenu.add-success.description',
          ),
        },
      };

    case ConfirmationMenuActionKind.ADD_ERROR:
      return {
        payload: {
          type: InfoPopoverType.ERROR,
          title: t('contextMenuPlaylist.confirmationMenu.add-error.title'),
          description: t(
            'contextMenuPlaylist.confirmationMenu.add-error.description',
          ),
        },
      };

    case ConfirmationMenuActionKind.DELETE_SUCCESS:
      return {
        payload: {
          type: InfoPopoverType.SUCCESS,
          title: t('contextMenuPlaylist.confirmationMenu.delete-success.title'),
          description: t(
            'contextMenuPlaylist.confirmationMenu.delete-success.description',
          ),
        },
      };

    case ConfirmationMenuActionKind.DELETE_ERROR:
      return {
        payload: {
          type: InfoPopoverType.ERROR,
          title: t('contextMenuPlaylist.confirmationMenu.delete-error.title'),
          description: t(
            'contextMenuPlaylist.confirmationMenu.delete-error.description',
          ),
        },
      };

    case ConfirmationMenuActionKind.CLIPBOARD:
      return {
        payload: {
          type: InfoPopoverType.CLIPBOARD,
          title: t('contextMenuPlaylist.confirmationMenu.clipboard.title'),
          description: t(
            'contextMenuPlaylist.confirmationMenu.clipboard.description',
          ),
        },
      };

    default:
      return {
        payload: {
          type: InfoPopoverType.ERROR,
          title: t('contextMenuPlaylist.confirmationMenu.error.title'),
          description: t(
            'contextMenuPlaylist.confirmationMenu.error.description',
          ),
        },
      };
  }
};

export default function ContextMenuPlaylist({
  playlistName,
  owner,
  handleCloseParent,
  refreshSidebarData,
}: PropsContextMenuPlaylist) {
  const navigate = useNavigate();

  const initialState: ConfirmationMenuState = {
    payload: {
      type: InfoPopoverType.ERROR,
      title: '',
      description: '',
    },
  };
  const [state, dispatch] = useReducer(reducerConfirmationMenu, initialState);

  // triggers Confirmation Modal
  const [triggerOpenConfirmationModal, setTriggerOpenConfirmationModal] =
    useState(false);

  /* Handle copy to clipboard on share button */

  const displayConfirmationModal = (newState: ConfirmationMenuActionKind) => {
    dispatch({ type: newState });
    setTriggerOpenConfirmationModal(true);
  };

  const handleCopyToClipboard = (): void => {
    window.electron.copyToClipboard.sendMessage(
      'copy-to-clipboard',
      Global.repositoryUrl,
    );
    displayConfirmationModal(ConfirmationMenuActionKind.CLIPBOARD);
  };

  const [isOpen, setIsOpen] = useState(false);

  const [anchorEl, setAnchorEl] = useState(null);

  const handleClick = (event: any) => {
    setAnchorEl(event.currentTarget);
    setIsOpen(!isOpen);
  };

  const handleClose = () => {
    setAnchorEl(null);
    handleCloseParent();
  };

  const open = Boolean(anchorEl);
  const id = open ? 'child-popover' : undefined;

  const username = getTokenUsername();

  const { playlistNames, loading } = useFetchGetUserPlaylistNames(username);

  const [isOwnerPlaylist, setIsOwnerPlaylist] = useState<boolean>();

  const disabledButton = {
    color: isOwnerPlaylist ? 'var(--pure-white)' : 'var(--grey)',
  };

  const handleOwner = useCallback(async () => {
    if (owner === username) {
      setIsOwnerPlaylist(true);
    } else {
      setIsOwnerPlaylist(false);
    }
  }, [owner, username]);

  useEffect(() => {
    handleOwner();
  }, [handleOwner]);

  const handleAddPlaylistToPlaylist = async (
    dstPlaylistName: string,
    srcPlaylistName: string,
  ) => {
    try {
      // eslint-disable-next-line camelcase
      const { song_names } =
        await PlaylistsService.getPlaylistPlaylistsNameGet(playlistName);

      await PlaylistsService.addSongsToPlaylistPlaylistsNameSongsPatch(
        dstPlaylistName,
        song_names,
      );

      displayConfirmationModal(ConfirmationMenuActionKind.ADD_SUCCESS);
    } catch (err) {
      console.error(
        `Unable to add songs from ${srcPlaylistName} to ${dstPlaylistName}: `,
        err,
      );
      displayConfirmationModal(ConfirmationMenuActionKind.ADD_ERROR);
    }
  };

  const handleDeletePlaylist = async (playlistNameToDelete: string) => {
    try {
      await PlaylistsService.deletePlaylistPlaylistsNameDelete(
        playlistNameToDelete,
      );
      refreshSidebarData();
      navigate(`/home`);
    } catch (err) {
      console.log(`Unable to delete playlist ${playlistNameToDelete}: `, err);
      displayConfirmationModal(ConfirmationMenuActionKind.DELETE_ERROR);
    } finally {
      handleClose();
    }
  };

  const handleCreatePlaylist = () => {
    // TODO implement, check for handleAddPlaylistToPlaylist
    // TODO may cause problems in the future if playlist already exists -> answer backend for valid name
  };

  const handleEditPlaylistData = () => {
    navigate(`/playlist/${playlistName}?edit=true`, { replace: true });

    localStorage.setItem('playlistEdit', JSON.stringify(true));

    handleClose();
  };

  return (
    <div className={` ${styles.wrapperContextMenu}`}>
      <ul>
        <li>
          <button type="button">{t('contextMenuPlaylist.add-to-queue')}</button>
        </li>
        <li>
          <button type="button" onClick={handleEditPlaylistData}>
            {t('contextMenuPlaylist.edit')}
          </button>
          <button type="button">
            {t('contextMenuPlaylist.create-similar-playlist')}
          </button>
          <button
            type="button"
            disabled={!isOwnerPlaylist}
            style={disabledButton}
            onClick={() => handleDeletePlaylist(playlistName)}
          >
            {t('contextMenuPlaylist.delete')}
          </button>
          <button type="button">{t('contextMenuPlaylist.download')}</button>
        </li>
        <li>
          <button
            type="button"
            className="d-flex justify-content-between align-items-center"
            onClick={handleClick}
          >
            {t('contextMenuPlaylist.add-to-playlist')}
            <i className="fa-solid fa-chevron-right" />
            <Popover
              id={id}
              open={open}
              anchorEl={anchorEl}
              onClose={handleClose}
              anchorOrigin={{
                vertical: 'center',
                horizontal: 'right',
              }}
              transformOrigin={{
                vertical: 'center',
                horizontal: 'left',
              }}
              sx={{
                '& .MuiPaper-root': {
                  backgroundColor: 'var(--hover-white)',
                },
              }}
            >
              <div
                className={` ${styles.wrapperContextMenu} ${styles.wrapperContextMenuAddToPlaylist}`}
              >
                <ul style={{ height: '100%' }}>
                  <li>
                    <button type="button">
                      {t('contextMenuPlaylist.search-playlist')}
                    </button>
                  </li>
                  <li>
                    <button type="button" onClick={handleCreatePlaylist}>
                      {t('contextMenuPlaylist.create-playlist')}
                    </button>
                  </li>

                  {loading && <LoadingCircle />}

                  {!loading &&
                    playlistNames &&
                    playlistNames.map((playlistNameItem) => {
                      return (
                        <li key={playlistNameItem}>
                          <button
                            type="button"
                            onClick={() =>
                              handleAddPlaylistToPlaylist(
                                playlistNameItem.toString(),
                                playlistName,
                              )
                            }
                          >
                            {playlistNameItem}
                          </button>
                        </li>
                      );
                    })}
                </ul>
              </div>
            </Popover>
          </button>
        </li>
        <li>
          <button type="button" onClick={handleCopyToClipboard}>
            {t('contextMenuPlaylist.share')}
          </button>
        </li>
      </ul>

      <InfoPopover
        type={state.payload.type}
        title={state.payload.title}
        description={state.payload.description}
        triggerOpenConfirmationModal={triggerOpenConfirmationModal}
        handleClose={handleClose}
      />
    </div>
  );
}
