import {useState} from "react";
import Box from "@mui/material/Box";
import Slider from "@mui/material/Slider";
import styles from "./timeSlider.module.css";
import { useEffect } from "react";

export default function TimeSlider(props) {


    const [songDuration,setSongDuration] = useState( +(0.00.toFixed(2)))
    const [songPlayTime,setsongPlayTime] = useState( +(0.00.toFixed(2)))

    const handlePlayTime = (event,value) => {
        //console.log(value)
        setsongPlayTime(value)
    }

    useEffect(() => {
        
        setsongPlayTime(props.playTime)
        console.log(songPlayTime)
       
    },[props.playTime])
    


    return (
        <Box width="100%" paddingRight="2%" display="flex">
            <p>{songPlayTime===undefined ?  (0.00.toFixed(2)) : songPlayTime.toFixed(2)}</p>

            <Slider
                size="small"
                min={0.00}
                max={props.songDuration}
                step={0.01}
                defaultValue={0}
                aria-label="Medium"
                valueLabelDisplay="off"
                /* onChange={handlePlayTime} */
                value={songPlayTime===undefined ?  +(0.00.toFixed(2)) : songPlayTime.toFixed(2)}
                sx={{
                    "& .MuiSlider-track": {
                        backgroundColor: 
                            "var(--primary-white)",
                    },
                    "& .MuiSlider-thumb": {
                        backgroundColor: 
                         "var(--primary-white)",
                        "&:hover, &.Mui-focusVisible": {
                            boxShadow:
                                "0px 0px 0px 8px rgba(255, 255, 255, 0.16)",
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

            <p>{props.songDuration.toFixed(2)}</p>
        </Box>
    );
}
