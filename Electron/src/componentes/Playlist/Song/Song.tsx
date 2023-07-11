import React from 'react';
import styles from '../playlist.module.css';
import { PropsSongs } from 'componentes/Sidebar/types/propsSongs.module';

export default function Song(props: PropsSongs) {
  const handleSongClicked = () => {
    props.handleSongCliked(props.name);
  };

  return (
    <li
      onDoubleClick={handleSongClicked}
      className={`container-fluid ${styles.gridContainer}`}
    >
      <span className={` ${styles.songNumberTable}`}>{props.index}</span>
      <span className={` ${styles.songTitleTable}`}>{props.name}</span>
      <span className={` ${styles.gridItem}`}>2:01</span>
    </li>
  );
}
