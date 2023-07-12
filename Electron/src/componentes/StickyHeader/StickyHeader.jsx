import {useState} from 'react';
import styles from './stickyHeader.module.css';
import groupIcon from '../../assets/imgs/groupIcon.png'

export default function StickyHeader() {

  const [profileIcon, setProfileIcon] = useState('https://i.scdn.co/image/ab67757000003b82ae8c728abc415a173667ff85')


  return (
    <header
      className={`d-flex flex-row container-fluid justify-content-space-evenly ${styles.wrapperStickyHeader}`}
    >
      <div
        className={`d-flex flex-row container-fluid ${styles.wrapperDirectionArrows}`}
      >

        <figure><i class="fa-solid fa-chevron-left"></i></figure>
        <figure><i class="fa-solid fa-chevron-right"></i></figure>


      </div>

      <div
        className={`d-flex flex-row container-fluid justify-content-end ${styles.wrapperProfileOptions}`}
      >
        <figure>

          <img src={profileIcon} alt="" />
        </figure>

        <figure>

          <img className={`${styles.groupIcon}`} src={groupIcon} alt="" />
        </figure>
      </div>
    </header>
  );
}
