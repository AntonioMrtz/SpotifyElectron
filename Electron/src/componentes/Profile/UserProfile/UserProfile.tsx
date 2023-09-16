import { useEffect, useState } from 'react';
import { FastAverageColor } from 'fast-average-color';
import Global from 'global/global';
import styles from './userProfile.module.css';
import defaultThumbnailPlaylist from '../../../assets/imgs/DefaultThumbnailPlaylist.jpg';

export default function UserProfile() {
  const userName = 'usuarioprovisionalcambiar';

  const [thumbnail, setThumbnail] = useState<string>(defaultThumbnailPlaylist);
  const [mainColorThumbnail, setMainColorThumbnail] = useState('');

  const handleLoadProfile = async () => {
    const fetchUrlGetUser = `${Global.backendBaseUrl}usuarios/${userName}`;

    const resGetUser = await fetch(fetchUrlGetUser);
    const resGetUserJson = await resGetUser.json();

    setThumbnail(resGetUserJson.photo);
  };

  useEffect(() => {
    handleLoadProfile();
  }, []);

  /* Process photo color */
  useEffect(() => {
    const fac = new FastAverageColor();

    const options = {
      crossOrigin: '*',
    };

    fac
      .getColorAsync(thumbnail, options)
      .then((color) => {
        setMainColorThumbnail(color.hex);

        return null;
      })
      .catch(() => {
        // console.log(e);
      });

    fac.destroy();
  }, [thumbnail]);

  return (
    <div className="d-flex flex-column container-fluid p-0">
      <div
        className={`d-flex align-items-end container-fluid ${styles.headerUserProfile}`}
        style={{
          backgroundColor: `${mainColorThumbnail}`,
          paddingTop: 'var(--pading-top-sticky-header)',
        }}
      >
        <div
          className={`d-flex flex-row ms-3 align-items-center ${styles.wrapperHeaderData}`}
          style={{ zIndex: 2 }}
        >
          <img
            src={thumbnail === '' ? defaultThumbnailPlaylist : thumbnail}
            alt=""
          />
          <div className="d-flex flex-column">
            <p>Usuario</p>
            <h1>{userName}</h1>
          </div>
        </div>
      </div>
    </div>
  );
}
