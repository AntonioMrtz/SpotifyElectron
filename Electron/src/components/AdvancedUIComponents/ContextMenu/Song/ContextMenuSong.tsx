import Popover from '@mui/material/Popover';
import { useState } from 'react';
import LoadingCircle from 'components/AdvancedUIComponents/LoadingCircle/LoadingCircle';
import InfoPopover from 'components/AdvancedUIComponents/InfoPopOver/InfoPopover';
import { InfoPopoverType } from 'components/AdvancedUIComponents/InfoPopOver/types/InfoPopover';
import Global from 'global/global';
import { getTokenUsername } from 'utils/token';
import { useNavigate } from 'react-router-dom';
import useFetchGetUserPlaylistNames from 'hooks/useFetchGetUserPlaylistNames';
import { PlaylistsService } from 'swagger/api';
import { t } from 'i18next';
import styles from '../contextMenu.module.css';
import { PropsContextMenuSong } from '../types/propsContextMenu';

const MessagesInfoPopOver = {
  CLIPBOARD_TITLE: 'Enlace copiado al portapapeles',
  CLIPBOARD_DESCRIPTION:
    'El enlace del repositorio del proyecto ha sido copiado éxitosamente',
};

// TODO tests not failing when app does

export default function ContextMenuSong({
  songName,
  artistName,
  playlistName,
  handleCloseParent,
  refreshPlaylistData,
  refreshSidebarData,
}: PropsContextMenuSong) {
  const navigate = useNavigate();

  const urlArtist = `/artist/${artistName}`;

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

  const handleClickGoToArtist = (event: any) => {
    event.preventDefault();
    event.stopPropagation();
    navigate(urlArtist);
  };

  const open = Boolean(anchorEl);
  const id = open ? 'child-popover' : undefined;

  const username = getTokenUsername();

  const { playlistNames, loading } = useFetchGetUserPlaylistNames(username);

  // triggers Confirmation Modal
  const [triggerOpenConfirmationModal, setTriggerOpenConfirmationModal] =
    useState(false);

  const handleCopyToClipboard = (): void => {
    window.electron.copyToClipboard.sendMessage(
      'copy-to-clipboard',
      Global.repositoryUrl,
    );
    setTriggerOpenConfirmationModal(true);
  };

  const handleAddSongToPlaylist = async (selectedPlaylistName: string) => {
    try {
      await PlaylistsService.addSongsToPlaylistPlaylistsNameSongsPatch(
        selectedPlaylistName,
        [songName],
      );
      handleClose();
    } catch (err) {
      console.log(
        `Unable to add Song ${songName} to Playlist ${selectedPlaylistName}`,
      );
      console.log(err);
    }
  };

  const handleDeleteSongFromPlaylist = async () => {
    try {
      await PlaylistsService.removeSongsFromPlaylistPlaylistsNameSongsDelete(
        playlistName,
        [songName],
      );
      refreshPlaylistData();
      handleClose();
    } catch (err) {
      console.log(
        `Unable to delete song ${songName} from playlist ${playlistName}`,
      );
      console.log(err);
    }
  };

  /* Handle crear lista */

  const HandleCreatePlaylistFromSong = async () => {
    try {
      // TODO may cause problems in the future if playlist already exists -> answer backend for valid name
      const newPlaylistName = `Playlist${Math.trunc(
        Math.floor(Math.random() * 1000),
      ).toString()}`;

      await PlaylistsService.createPlaylistPlaylistsPost(
        newPlaylistName,
        'no-photo',
        'Insertar descripción',
        [songName],
      );
      refreshSidebarData();
      handleClose();
    } catch (err) {
      console.log(
        console.log(`Unable to create playlist from Song ${songName}`),
      );
      console.log(err);
    }
  };

  return (
    <div className={` ${styles.wrapperContextMenu}`}>
      <ul>
        <li>
          <button type="button">{t('contextMenuSong.add-to-queue')}</button>
        </li>
        <li>
          <button type="button">{t('contextMenuSong.go-to-radio')}</button>
          <button type="button" onClick={(e) => handleClickGoToArtist(e)}>
            {t('contextMenuSong.go-to-artist')}
          </button>
          <button type="button">{t('contextMenuSong.go-to-album')}</button>
        </li>
        <li>
          <button type="button">
            {t('contextMenuSong.remove-from-liked-songs')}
          </button>
          {playlistName !== '' && (
            <button
              type="button"
              onClick={() => handleDeleteSongFromPlaylist()}
            >
              {t('contextMenuSong.remove-from-playlist')}
            </button>
          )}
          <button
            type="button"
            className="d-flex justify-content-between align-items-center"
            onClick={handleClick}
          >
            {t('contextMenuSong.add-to-playlist')}{' '}
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
                  border: '1px solid var(--third-black)',
                },
              }}
            >
              <div
                className={` ${styles.wrapperContextMenu} ${styles.wrapperContextMenuAddToPlaylist}`}
              >
                <ul style={{ height: '100%' }}>
                  <li>
                    <button type="button">
                      {t('contextMenuSong.search-playlist')}
                    </button>
                  </li>
                  <li>
                    <button
                      type="button"
                      onClick={HandleCreatePlaylistFromSong}
                    >
                      {t('contextMenuSong.create-playlist')}
                    </button>
                  </li>

                  {loading && <LoadingCircle />}

                  {!loading &&
                    playlistNames &&
                    playlistNames.map((playlistNameItem) => {
                      return (
                        <li key={playlistNameItem + songName}>
                          <button
                            type="button"
                            onClick={() =>
                              handleAddSongToPlaylist(
                                playlistNameItem.toString(),
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
            {t('contextMenuSong.share')}
          </button>
        </li>
      </ul>

      <InfoPopover
        type={InfoPopoverType.CLIPBOARD}
        title={MessagesInfoPopOver.CLIPBOARD_TITLE}
        description={MessagesInfoPopOver.CLIPBOARD_DESCRIPTION}
        triggerOpenConfirmationModal={triggerOpenConfirmationModal}
        handleClose={handleClose}
      />
    </div>
  );
}
