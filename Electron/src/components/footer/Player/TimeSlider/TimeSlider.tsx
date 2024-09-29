import { useState, useEffect } from 'react';
import Box from '@mui/material/Box';
import Slider from '@mui/material/Slider';
import { secondsToMinutesSeconds } from 'utils/date';
import styles from './timeSlider.module.css';

interface PropsTimeSlider {
  playBackTime: number;
  initialSongDuration: number;
  changePlayBackTime: (playBackTime: number) => void;
}

export default function TimeSlider({
  playBackTime,
  initialSongDuration,
  changePlayBackTime,
}: PropsTimeSlider) {
  /* Song PLAYBACK TIME */

  const [songPlayBackTime, setSongPlayBackTime] = useState(0);
  const [songPlayBackTimeMinutesSeconds, setSongPlayBackTimeMinutesSeconds] =
    useState('0.0');

  const handlePlaybackTime = (event: Event, value: number | number[]) => {
    if (typeof value === 'number') {
      setSongPlayBackTime(value);
      changePlayBackTime(value);
    }
  };

  useEffect(() => {
    setSongPlayBackTime(playBackTime);
    setSongPlayBackTimeMinutesSeconds(secondsToMinutesSeconds(playBackTime));
  }, [playBackTime]);

  /* Song DURATION */

  const [songDuration, setSongDuration] = useState(0);
  const [songDurationMinutesSeconds, setsongDurationMinutesSeconds] =
    useState('0.0');

  useEffect(() => {
    setsongDurationMinutesSeconds(secondsToMinutesSeconds(songDuration));
    setSongDuration(initialSongDuration);
  }, [initialSongDuration, songDuration]);

  /* Hover slider */

  const [isHovered, setIsHovered] = useState(false);

  const handleMouseEnter = () => {
    setIsHovered(true);
  };

  const handleMouseLeave = () => {
    setIsHovered(false);
  };

  return (
    <Box width="100%" paddingRight="2%" display="flex" alignItems="center">
      <p className={styles.pSlider}>{songPlayBackTimeMinutesSeconds}</p>

      <Slider
        size="small"
        min={0}
        max={songDuration}
        step={1}
        defaultValue={0}
        aria-label="Medium"
        valueLabelDisplay="off"
        onChange={handlePlaybackTime}
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
        value={songPlayBackTime === undefined ? 0 : songPlayBackTime}
        sx={{
          '& .MuiSlider-track': {
            backgroundColor: isHovered
              ? 'var(--primary-green)'
              : 'var(--primary-white)',
          },
          '& .MuiSlider-thumb': {
            backgroundColor: 'var(--primary-white)',
            '&:hover, &.Mui-focusVisible': {
              boxShadow: '0px 0px 0px 8px rgba(255, 255, 255, 0.16)',
            },
          },
          '& .MuiSlider-valueLabel': {
            color: '#fff',
          },
          '& .MuiSlider-rail': {
            backgroundColor: 'rgba(255, 255, 255, 0.5)',
          },
        }}
      />

      <p className={styles.pSlider}>{songDurationMinutesSeconds}</p>
    </Box>
  );
}
