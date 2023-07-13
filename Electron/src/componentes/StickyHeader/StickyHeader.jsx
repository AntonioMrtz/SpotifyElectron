import { useEffect, useState } from 'react';
import styles from './stickyHeader.module.css';
import groupIcon from '../../assets/imgs/groupIcon.png';

export default function StickyHeader() {
  const [profileIcon, setProfileIcon] = useState(
    'https://i.scdn.co/image/ab67757000003b82ae8c728abc415a173667ff85'
  );

  const [visibleBackground, setVisibleBackground] = useState({});

  const handleScroll = () => {
    if (window.scrollY > 200) {
      setVisibleBackground({
        backgroundColor: 'var(--sticky-header-blue)',
        marginTop:'0',
      });
    }else if(window.scrollY > 150) {
      setVisibleBackground({
        backgroundColor: 'var(--sticky-header-blue)',
        marginTop:'0',
        opacity:'0.7'
      });
    }
    else if(window.scrollY > 100) {
      setVisibleBackground({
        backgroundColor: 'var(--sticky-header-blue)',
        marginTop:'0',
        opacity:'0.5',
      });
    } else {
      setVisibleBackground({});
    }
  };

  useEffect(() => {
    window.addEventListener('scroll', handleScroll);

    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  return (
    <header
      style={visibleBackground}
      className={`d-flex flex-row justify-content-space-evenly ${styles.wrapperStickyHeader}`}
    >
      <div
        className={`d-flex flex-row container-fluid ${styles.wrapperDirectionArrows}`}
      >
        <button>
          <i className="fa-solid fa-chevron-left"></i>
        </button>
        <button>
          <i className="fa-solid fa-chevron-right"></i>
        </button>
      </div>

      <div
        className={`d-flex flex-row container-fluid  ${styles.wrapperProfileOptions}`}
      >
        <button>
          <img src={profileIcon} alt="" />
        </button>

        <button>
          <img className={`${styles.groupIcon}`} src={groupIcon} alt="" />
        </button>
      </div>
    </header>
  );
}
