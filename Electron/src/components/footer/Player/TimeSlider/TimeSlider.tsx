import { useState, useEffect } from 'react';
import Box from '@mui/material/Box';
import Slider from '@mui/material/Slider';
import { secondsToMinutesSeconds } from 'utils/date';
import styles from './timeSlider.module.css';

interface PropsTimeSlider {
  streamTime: number;
  initialSongDuration: number;
  changeStreamTime: (streamTime: number) => void;
}

export default function TimeSlider({
  streamTime: streamTime,
  initialSongDuration,
  changeStreamTime: changeStreamTime,
}: PropsTimeSlider) {
  /* Song STREAM TIME */

  const [songStreamTime, setSongStreamTime] = useState(0);
  const [songStreamTimeMinutesSeconds, setSongStreamTimeMinutesSeconds] =
    useState('0.0');

  const handleStreamTime = (event: Event, value: number | number[]) => {
    if (typeof value === 'number') {
      setSongStreamTime(value);
      changeStreamTime(value);
    }
  };

  useEffect(() => {
    setSongStreamTime(streamTime);
    setSongStreamTimeMinutesSeconds(secondsToMinutesSeconds(streamTime));
  }, [streamTime]);

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
      <p className={styles.pSlider}>{songStreamTimeMinutesSeconds}</p>

      <Slider
        size="small"
        min={0}
        max={songDuration}
        step={1}
        defaultValue={0}
        aria-label="Medium"
        valueLabelDisplay="off"
        onChange={handleStreamTime}
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
        value={songStreamTime === undefined ? 0 : songStreamTime}
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
