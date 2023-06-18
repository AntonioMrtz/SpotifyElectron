import * as React from "react";
import Box from "@mui/material/Box";
import Slider from "@mui/material/Slider";
import styles from "./volumeSlider.module.css";


export default function VolumeSlider() {
  const [isHovered, setIsHovered] = React.useState(false);

  const handleMouseEnter = () => {
    setIsHovered(true);
  };

  const handleMouseLeave = () => {
    setIsHovered(false);
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
        defaultValue={50}
        aria-label="Small"
        valueLabelDisplay="off"
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
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
