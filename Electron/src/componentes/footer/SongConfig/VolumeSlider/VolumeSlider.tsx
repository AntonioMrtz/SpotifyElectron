import { useState } from "react";
import Box from "@mui/material/Box";
import Slider from "@mui/material/Slider";
import styles from "./volumeSlider.module.css";


interface PropsVolumeSlider{
  changeVolume : (volume:number) => void 
}


export default function VolumeSlider(props:PropsVolumeSlider) {

  const [isHovered, setIsHovered] = useState(false);
  const [previousVolume, setPreviousVolume] = useState<number>(50);
  const [currentValue, setcurrentValue] = useState<number>(50);
  const [muted, setmuted] = useState(false);

  const handleMouseEnter = () => {
    setIsHovered(true);
  };

  const handleMouseLeave = () => {
    setIsHovered(false);
  };


const handleVolume = (event:Event, newValue:number | number[] ,activeThumb:number) : void => {
    if(typeof(newValue)=== "number"){
      setcurrentValue(newValue)
      setPreviousVolume(newValue)
      props.changeVolume(newValue)
      setmuted(false)
      if((newValue)=== 0){
        setmuted(true)
      }
    }
  };

  const handleMute = (): void => {
    if(!muted){
      setPreviousVolume(currentValue)
      setcurrentValue(0);
      props.changeVolume(0);
      setmuted(true);
    }else if (previousVolume !== undefined){
      setcurrentValue(previousVolume);
      setmuted(false);
      props.changeVolume(previousVolume);
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
        className={`btn ${styles.buttonSpeaker}`} 
        onClick={handleMute}
      >
        <i className={`fa-solid fa-volume-low fa-fw`} ></i>
      </button>
      <Slider classes
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
            "&:after":{
              width:24,
              heigh:24
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
