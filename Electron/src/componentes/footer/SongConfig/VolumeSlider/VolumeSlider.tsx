import { useState } from "react";
import Box from "@mui/material/Box";
import Slider from "@mui/material/Slider";
import styles from "./volumeSlider.module.css";



interface PropsVolumeSlider{
  changeVolume : (volume:number) => void
}


export default function VolumeSlider(props: PropsVolumeSlider) {

  const [isHovered, setIsHovered] = useState(false);
  const [previousVolume, setPreviousVolume] = useState<number>(50);
  const [currentValue, setcurrentValue] = useState<number>(50);
  const [muted, setmuted] = useState(false);
  const [displayUnmuted, setdisplayUnmuted] = useState('');
  const [displayHigh,setdisplayHigh] = useState(styles.displayMuted);
  const [displayMuted, setdisplayMuted] = useState(styles.displayMuted);

  const handleMouseEnter = () => {
    setIsHovered(true);
  };

  const handleMouseLeave = () => {
    setIsHovered(false);
  };


  const handleVolume = (event: Event, newValue: number | number[], activeThumb: number): void => {
    if (typeof (newValue) === "number") {
      setcurrentValue(newValue)
      setPreviousVolume(newValue)
      props.changeVolume(newValue)
      setmuted(false)
      if (newValue === 0) {
        setdisplayUnmuted(styles.displayMuted);
        setdisplayMuted('');
        setPreviousVolume(50);
        setcurrentValue(0);
        setmuted(true);
      }else if(newValue >= 75){
        setdisplayHigh('');
        setdisplayUnmuted(styles.displayMuted);
      }else {
        setdisplayHigh(styles.displayMuted);
        setdisplayMuted(styles.displayMuted);
        setdisplayUnmuted('');
      }
    }
  };

  const handleMute = (): void => {
    if (!muted) {
      setPreviousVolume(currentValue)
      setcurrentValue(0);
      props.changeVolume(0);
      setdisplayUnmuted(styles.displayMuted);
      setdisplayHigh(styles.displayMuted);
      setdisplayMuted('');
      setmuted(true);
    } else if (previousVolume !== undefined) {
      setcurrentValue(previousVolume);
      setdisplayMuted(styles.displayMuted);
      setmuted(false);
      props.changeVolume(previousVolume);
      if(previousVolume >= 75){
        setdisplayHigh('')
      }else{
        setdisplayUnmuted('')
      }
    }
  };

  return (
    <Box width="30%" paddingRight="2%" display="flex">
        <button
          onMouseEnter={handleMouseEnter}
          onMouseLeave={handleMouseLeave}
          style={{
            color: isHovered ? "var(--pure-white)" : "var(--primary-white)",
          }}
          className={`btn ${displayUnmuted} ${styles.buttonMargins}`}
          onClick={handleMute}>
          <i className={`fa-solid fa-volume-low fa-fw`} ></i>
        </button>

        <button
          onMouseEnter={handleMouseEnter}
          onMouseLeave={handleMouseLeave}
          style={{
            color: isHovered ? "var(--pure-white)" : "var(--primary-white)",
          }}
          className={`btn ${displayHigh} ${styles.buttonMargins}`}
          onClick={handleMute}>
          <i className={`fa-solid fa-volume-high fa-fw`} ></i>
        </button>

        <button
          onMouseEnter={handleMouseEnter}
          onMouseLeave={handleMouseLeave}
          style={{
            color: isHovered ? "var(--pure-white)" : "var(--primary-white)",
          }}
          className={`btn ${displayMuted} ${styles.buttonMargins}`}
          onClick={handleMute}>
          <i className={`fa-solid fa-volume-xmark`} ></i>
        </button>

      <Slider
        style={{display:'flex',justifyContent:'center',alignItems:'center'}}
        size="small"
        min={0}
        max={100}
        step={1}
        defaultValue={50}
        aria-label="Small"
        valueLabelDisplay="off"
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
        onChange={handleVolume}
        value={currentValue}
        sx={{
          "& .MuiSlider-track": {
            backgroundColor: isHovered ? "var(--primary-green)" : "var(--primary-white)",
          },
          "& .MuiSlider-thumb": {
            backgroundColor: isHovered ? "var(--primary-green)" : "var(--primary-white)",
            "&:hover, &.Mui-focusVisible": {
              boxShadow: "0px 0px 0px 8px rgba(255, 255, 255, 0.16)",
            },
            "&:after": {
              width: 24,
              heigh: 24
            }
          },
          "& .MuiSlider-valueLabel": {
            color: "#fff",
          },
          "& .MuiSlider-rail": {
            backgroundColor: "rgba(255, 255, 255, 0.5)",
          },
        }}
      />
    </Box>
  );
}
