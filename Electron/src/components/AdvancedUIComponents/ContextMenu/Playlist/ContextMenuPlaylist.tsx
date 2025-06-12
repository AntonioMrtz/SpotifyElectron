import React, { useCallback, useEffect, useReducer, useState, useRef } from 'react';
import Popover from '@mui/material/Popover';
import Global from 'global/global';
import { useNavigate } from 'react-router-dom';
import LoadingCircle from 'components/AdvancedUIComponents/LoadingCircle/LoadingCircle';
import InfoPopover from 'components/AdvancedUIComponents/InfoPopOver/InfoPopover';
import { InfoPopoverType } from 'components/AdvancedUIComponents/InfoPopOver/types/InfoPopover';
import { getTokenUsername } from 'utils/token';
import useFetchGetUserPlaylistNames from 'hooks/useFetchGetUserPlaylistNames';
import { PlaylistsService } from 'swagger/api'; // Ensure this path is correct
import { t } from 'i18next'; // Ensure this path is correct
import styles from '../contextMenu.module.css'; // Ensure this path is correct
import { PropsContextMenuPlaylist } from '../types/propsContextMenu'; // Ensure this path is correct

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

interface ConfirmationMenuAction {
  type: ConfirmationMenuActionKind;
}

interface ConfirmationMenuState {
  payload: ConfirmationMenuData;
}

const reducerConfirmationMenu = (
  state: ConfirmationMenuState,
  action: ConfirmationMenuAction
): ConfirmationMenuState => {
  switch (action.type) {
    case ConfirmationMenuActionKind.ADD_SUCCESS:
      return {
        payload: {
          type: InfoPopoverType.SUCCESS,
          title: t('contextMenuPlaylist.confirmationMenu.add-success.title'),
          description: t('contextMenuPlaylist.confirmationMenu.add-success.description'),
        },
      };
    case ConfirmationMenuActionKind.ADD_ERROR:
      return {
        payload: {
          type: InfoPopoverType.ERROR,
          title: t('contextMenuPlaylist.confirmationMenu.add-error.title'),
          description: t('contextMenuPlaylist.confirmationMenu.add-error.description'),
        },
      };
    case ConfirmationMenuActionKind.DELETE_SUCCESS:
      return {
        payload: {
          type: InfoPopoverType.SUCCESS,
          title: t('contextMenuPlaylist.confirmationMenu.delete-success.title'),
          description: t('contextMenuPlaylist.confirmationMenu.delete-success.description'),
        },
      };
    case ConfirmationMenuActionKind.DELETE_ERROR:
      return {
        payload: {
          type: InfoPopoverType.ERROR,
          title: t('contextMenuPlaylist.confirmationMenu.delete-error.title'),
          description: t('contextMenuPlaylist.confirmationMenu.delete-error.description'),
        },
      };
    case ConfirmationMenuActionKind.CLIPBOARD:
      return {
        payload: {
          type: InfoPopoverType.CLIPBOARD,
          title: t('contextMenuPlaylist.confirmationMenu.clipboard.title'),
          description: t('contextMenuPlaylist.confirmationMenu.clipboard.description'),
        },
      };
    default:
      return state;
  }
};

export default function ContextMenuPlaylist({
  playlistName,
  owner,
  handleCloseParent, // This closes the *outermost* Material-UI Menu/Popover
  refreshSidebarData,
}: PropsContextMenuPlaylist) {
  const navigate = useNavigate();
  const [state, dispatch] = useReducer(reducerConfirmationMenu, {
    payload: {
      type: InfoPopoverType.ERROR,
      title: '',
      description: '',
    },
  });
  const [triggerOpenConfirmationModal, setTriggerOpenConfirmationModal] = useState(false);

  // Submenu state
  const [isSubmenuOpen, setIsSubmenuOpen] = useState(false);
  const [submenuAnchorEl, setSubmenuAnchorEl] = useState<HTMLElement | null>(null);

  // Refs for the main menu and submenu elements
  const mainMenuRef = useRef<HTMLDivElement>(null); // Ref for the main wrapperContextMenu div
  const submenuPopoverRef = useRef<HTMLDivElement>(null); // Ref for the div *inside* the Popover

  // Timeouts for closing menus
  const closeMenuTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const openSubmenuTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  const username = getTokenUsername();
  const { playlistNames, loading } = useFetchGetUserPlaylistNames(username);
  const [isOwnerPlaylist, setIsOwnerPlaylist] = useState<boolean>();
  const disabledButton = {
    color: isOwnerPlaylist ? 'var(--pure-white)' : 'var(--grey)',
    cursor: isOwnerPlaylist ? 'pointer' : 'not-allowed',
  };

  // Centralized function to clear all active close timers
  const clearCloseTimer = useCallback(() => {
    if (closeMenuTimeoutRef.current) {
      clearTimeout(closeMenuTimeoutRef.current);
      closeMenuTimeoutRef.current = null;
    }
  }, []);

  // Centralized function to set a close timer for the *entire* menu structure
  const setCloseTimer = useCallback(() => {
    clearCloseTimer(); // Clear any existing timer first
    closeMenuTimeoutRef.current = setTimeout(() => {
      // Check if the mouse is still inside the main menu OR the submenu content
      const isMouseOverMainMenu = mainMenuRef.current?.matches(':hover');
      const isMouseOverSubmenuContent = submenuPopoverRef.current?.matches(':hover'); // Check the content of the submenu popover

      // Only close if mouse is NOT over the main menu AND NOT over the submenu content
      if (!isMouseOverMainMenu && !isMouseOverSubmenuContent) {
        setIsSubmenuOpen(false); // Close submenu state
        setSubmenuAnchorEl(null); // Clear submenu anchor
        handleCloseParent(); // Close the outermost menu
      }
    }, 200); // Delay for closing
  }, [handleCloseParent, clearCloseTimer]);


  // Handler for mouse entering *any part* of the main context menu
  const handleMouseEnterOverallMenu = useCallback(() => {
    clearCloseTimer(); // If mouse enters, don't close!
  }, [clearCloseTimer]);

  // Handler for mouse leaving *any part* of the main context menu
  const handleMouseLeaveOverallMenu = useCallback(() => {
    setCloseTimer(); // If mouse leaves, start timer to close
  }, [setCloseTimer]);

  // Submenu button hover handlers
  const handleMouseEnterSubmenuButton = useCallback((event: React.MouseEvent<HTMLElement>) => {
    clearCloseTimer(); // Keep parent open
    if (openSubmenuTimeoutRef.current) {
      clearTimeout(openSubmenuTimeoutRef.current);
    }

    // Capture event.currentTarget immediately to avoid null issue in setTimeout
    const targetElement = event.currentTarget;

    openSubmenuTimeoutRef.current = setTimeout(() => {
      setIsSubmenuOpen(true);
      setSubmenuAnchorEl(targetElement); // Use the captured element

    }, 50); // Short delay for opening submenu
  }, [clearCloseTimer]);

  const handleMouseLeaveSubmenuButton = useCallback(() => {
    if (openSubmenuTimeoutRef.current) {
      clearTimeout(openSubmenuTimeoutRef.current);
      openSubmenuTimeoutRef.current = null;
    }
    // Rely on the overall menu's setCloseTimer to handle closing
    setCloseTimer();
  }, [setCloseTimer]);

  // Submenu Popover content hover handlers
  const handleMouseEnterSubmenuPopover = useCallback(() => {
    clearCloseTimer(); // Keep parent and submenu open
    setIsSubmenuOpen(true); // Ensure it's open
    // IMPORTANT: Clear any pending submenu opening timer if mouse re-enters the popover
    if (openSubmenuTimeoutRef.current) {
      clearTimeout(openSubmenuTimeoutRef.current);
      openSubmenuTimeoutRef.current = null;
    }
  }, [clearCloseTimer]);

  const handleMouseLeaveSubmenuPopover = useCallback(() => {
    // Rely on the overall menu's setCloseTimer to handle closing
    setCloseTimer();
  }, [setCloseTimer]);


  // Handle clicks outside all menus
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      const mainMenuElement = mainMenuRef.current;
      const submenuPopoverElement = submenuPopoverRef.current;

      if (mainMenuElement && !mainMenuElement.contains(event.target as Node) &&
          (submenuPopoverElement ? !submenuPopoverElement.contains(event.target as Node) : true)) {
        clearCloseTimer(); // Clear any pending timeouts
        setIsSubmenuOpen(false);
        setSubmenuAnchorEl(null);
        handleCloseParent(); // Close the parent Popover immediately on click outside
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [handleCloseParent, clearCloseTimer]);


  const displayConfirmationModal = (newState: ConfirmationMenuActionKind) => {
    dispatch({ type: newState });
    setTriggerOpenConfirmationModal(true);
  };

  const handleCopyToClipboard = (): void => {
    window.electron.copyToClipboard.sendMessage(
      'copy-to-clipboard',
      Global.repositoryUrl
    );
    displayConfirmationModal(ConfirmationMenuActionKind.CLIPBOARD);
    handleCloseParent(); // Close main menu after action
  };

  const handleOwner = useCallback(async () => {
    setIsOwnerPlaylist(owner === username);
  }, [owner, username]);

  useEffect(() => {
    handleOwner();
  }, [handleOwner]);

  const handleAddPlaylistToPlaylist = async (
    dstPlaylistName: string,
    srcPlaylistName: string
  ) => {
    try {
      const { song_names } = await PlaylistsService.getPlaylistPlaylistsNameGet(playlistName);
      await PlaylistsService.addSongsToPlaylistPlaylistsNameSongsPatch(
        dstPlaylistName,
        song_names
      );
      displayConfirmationModal(ConfirmationMenuActionKind.ADD_SUCCESS);
    } catch (err) {
      console.error(`Unable to add songs from ${srcPlaylistName} to ${dstPlaylistName}: `, err);
      displayConfirmationModal(ConfirmationMenuActionKind.ADD_ERROR);
    } finally {
      setIsSubmenuOpen(false); // Close submenu
      setSubmenuAnchorEl(null);
      handleCloseParent(); // Close main menu
    }
  };

  const handleDeletePlaylist = async (playlistNameToDelete: string) => {
    try {
      await PlaylistsService.deletePlaylistPlaylistsNameDelete(playlistNameToDelete);
      refreshSidebarData();
      navigate(`/home`);
    } catch (err) {
      console.log(`Unable to delete playlist ${playlistNameToDelete}: `, err);
      displayConfirmationModal(ConfirmationMenuActionKind.DELETE_ERROR);
    } finally {
      handleCloseParent(); // Close main menu
    }
  };

  const handleCreatePlaylist = () => {
    console.log('Create playlist clicked');
    setIsSubmenuOpen(false); // Close submenu
    setSubmenuAnchorEl(null);
    handleCloseParent(); // Close main menu
  };

  const handleEditPlaylistData = () => {
    navigate(`/playlists/${playlistName}?edit=true`, { replace: true });
    localStorage.setItem('playlistEdit', JSON.stringify(true));
    handleCloseParent(); // Close main menu
  };

  return (
    <div
      className={styles.wrapperContextMenu}
      ref={mainMenuRef} // Attach ref to the main menu wrapper
      onMouseEnter={handleMouseEnterOverallMenu} // Centralized enter handler
      onMouseLeave={handleMouseLeaveOverallMenu} // Centralized leave handler
    >
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
          <button type="button"> {t('contextMenuPlaylist.download')}</button>
        </li>
        <li>
          <div
            className="d-flex justify-content-between align-items-center"
            onMouseEnter={handleMouseEnterSubmenuButton}
            onMouseLeave={handleMouseLeaveSubmenuButton}
            style={{ padding: '12px', cursor: 'pointer' }}
          >
            {t('contextMenuPlaylist.add-to-playlist')}
            <i className="fa-solid fa-chevron-right" />
          </div>
          <Popover
            open={isSubmenuOpen}
            anchorEl={submenuAnchorEl}
            // onClose handles click away and escape key for the submenu
            onClose={() => {
                setIsSubmenuOpen(false);
                setSubmenuAnchorEl(null);
                setCloseTimer(); // Trigger a close check for the overall menu
            }}
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
                marginLeft: '8px',
              },
              // Removed pointerEvents from here as a test, based on previous discussion
            }}
            disableRestoreFocus
            // Add onMouseEnter and onMouseLeave directly to the Popover component itself
            // This captures the entire popover area for hover
            onMouseEnter={handleMouseEnterSubmenuPopover}
            onMouseLeave={handleMouseLeaveSubmenuPopover}
          >
            <div // This div inside the Popover provides a solid hover target
              className={`${styles.wrapperContextMenu} ${styles.wrapperContextMenuAddToPlaylist}`}
              ref={submenuPopoverRef} // Attach ref to the submenu's content div
              onMouseEnter={handleMouseEnterSubmenuPopover} // Redundant but harmless for now due to Popover's own handler
              onMouseLeave={handleMouseLeaveSubmenuPopover} // Redundant but harmless for now due to Popover's own handler
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
                {!loading && playlistNames?.map((playlistNameItem) => (
                  <li key={playlistNameItem}>
                    <button
                      type="button"
                      onClick={() => handleAddPlaylistToPlaylist(playlistNameItem.toString(), playlistName)}
                    >
                      {playlistNameItem}
                    </button>
                  </li>
                ))}
              </ul>
            </div>
          </Popover>
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
        handleClose={handleCloseParent}
      />
    </div>
  );
}