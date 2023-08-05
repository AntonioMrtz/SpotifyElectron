import { useState } from 'react';
import Box from '@mui/material/Box';
import Slider from '@mui/material/Slider';
import styles from './timeSlider.module.css';
import { useEffect } from 'react';

interface PropsTimeSlider {
  playBackTime: number;
  songDuration: number;
  changePlayBackTime: (playBackTime: number) => void;
}

export default function TimeSlider(props: PropsTimeSlider) {
  /* Song PLAYBACK TIME */

  const [songPlayBackTime, setSongPlayBackTime] = useState(0);
  const [songPlayBackTimeMinutesSeconds, setSongPlayBackTimeMinutesSeconds] =
    useState(0.0);

  const handleplaybacktime = (
    event: Event,
    value: number | number[],
    activeThumb: number
  ) => {
    if (typeof value === 'number') {
      setSongPlayBackTime(value);
      props.changePlayBackTime(value);
    }
  };

  useEffect(() => {
    setSongPlayBackTime(props.playBackTime);
    setSongPlayBackTimeMinutesSeconds(
      secondsToMinutesSeconds(props.playBackTime)
    );
  }, [props.playBackTime]);

  /* Song DURATION */

  const [songDuration, setSongDuration] = useState(0);
  const [songDurationMinutesSeconds, setsongDurationMinutesSeconds] =
    useState(0.0);

  useEffect(() => {
    setsongDurationMinutesSeconds(secondsToMinutesSeconds(props.songDuration));
    setSongDuration(props.songDuration);
  }, [props.songDuration]);

  /* Hover slider */

  const [isHovered, setIsHovered] = useState(false);

  const handleMouseEnter = () => {
    setIsHovered(true);
  };

  const handleMouseLeave = () => {
    setIsHovered(false);
  };

  return (
    <Box width="100%" paddingRight="2%" display="flex" alignItems={'center'}>
      <p className={styles.pSlider}>{songPlayBackTimeMinutesSeconds}</p>

      <Slider
        size="small"
        min={0}
        max={songDuration}
        step={1}
        defaultValue={0}
        aria-label="Medium"
        valueLabelDisplay="off"
        onChange={handleplaybacktime}
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

/* Utils */
const minutesSecondsToSeconds = (minutesSeconds: number) => {
  let result =
    Math.round(minutesSeconds) * 60 + ((minutesSeconds % 1) * 100).toFixed(2);
  return result;
};

const secondsToMinutesSeconds: Function = (secs: number) => {
  let minutes = Math.floor(secs / 60);
  let seconds = (secs - minutes * 60) / 100;

  return (minutes + seconds).toFixed(2).replace('.', ':');
};
