import { useState } from "react";
import Box from "@mui/material/Box";
import Slider from "@mui/material/Slider";
import styles from "./volumeSlider.module.css";


export default function VolumeSlider(props) {

  const [isHovered, setIsHovered] = useState(false);

  const handleMouseEnter = () => {
    setIsHovered(true);
  };

  const handleMouseLeave = () => {
    setIsHovered(false);
  };


  const handleVolume = (event, newValue) => {

    props.changeVolume(newValue)
  };

  return (
    <Box width="30%" paddingRight="2%" display="flex">
      <span
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
        style={{
            color: isHovered ? "var(--pure-white)" : "var(--primary-white)",
        }}
        className={` ${styles.volumeSpan} `}
      >
        <i className="fa-solid fa-volume-low fa-fw"></i>
      </span>
      <Slider
        size="small"
        min={1}
        max={100}
        step={1}
        defaultValue={50}
        aria-label="Small"
        valueLabelDisplay="off"
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
        onChange={handleVolume}
        sx={{
          "& .MuiSlider-track": {
            backgroundColor: isHovered ? "var(--primary-green)" : "var(--primary-white)",
          },
          "& .MuiSlider-thumb": {
            backgroundColor: isHovered ? "var(--primary-green)" : "var(--primary-white)",
            "&:hover, &.Mui-focusVisible": {
              boxShadow: "0px 0px 0px 8px rgba(255, 255, 255, 0.16)",
            },
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
