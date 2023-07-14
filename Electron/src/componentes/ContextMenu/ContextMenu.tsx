import React from 'react';
import styles from './contentMenu.module.css';

export default function ContextMenu() {
  return (
    <div className={` ${styles.wrapperContextMenu}`}>
      <ul>
        <li>
          <button>Añadir a la cola</button>
        </li>
        <li>
          <button>Añadir a otra copsa</button>
          <button>Añadir a la cola</button>
        </li>
        <li>
          <button>Añadir a otra copsa</button>
          <button>Añadir a la cola</button>
        </li>
        <li>
          <button>Añadir a otra copsa</button>
          <button>Añadir a la cola</button>
        </li>
      </ul>
    </div>
  );
}
