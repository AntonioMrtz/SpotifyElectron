import {useState} from "react";
import Box from "@mui/material/Box";
import Slider from "@mui/material/Slider";
import styles from "./timeSlider.module.css";
import { useEffect } from "react";


export default function TimeSlider(props) {


    /* Song PLAYTIME */

    const [songPlayTime,setsongPlayTime] = useState( 0 )
    const [songPlayTimeMinutesSeconds,setSongPlayTimeMinutesSeconds] = useState( 0.00 )
    
    
    const handlePlayTime = (event, value) => {
        console.log("cambio con value = " + value);
        
        setsongPlayTime(value);
        props.changePlayTime(value);
    };

    useEffect(() => {
        setsongPlayTime(props.playTime);
        setSongPlayTimeMinutesSeconds(secondsToMinutesSeconds(props.playTime));
    }, [props.playTime]);
    
    
    /* Song DURATION */
    
    const [songDuration,setSongDuration] = useState( 0 )
    const [songDurationMinutesSeconds,setsongDurationMinutesSeconds] = useState( 0.00 )

    useEffect(() => {
        setsongDurationMinutesSeconds(
            secondsToMinutesSeconds(props.songDuration)
        );
        setSongDuration(props.songDuration);
    }, [props.songDuration]);
    


    return (
        <Box width="100%" paddingRight="2%" display="flex">
            <p>{songPlayTimeMinutesSeconds}</p>

            <Slider
                size="small"
                min={0}
                max={songDuration}
                step={1}
                defaultValue={0}
                aria-label="Medium"
                valueLabelDisplay="off"
                onChange={handlePlayTime}
                value={songPlayTime===undefined ?  0 : songPlayTime }
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

            <p>{songDurationMinutesSeconds}</p>
        </Box>
    );
}


/* Utils */
const minutesSecondsToSeconds = (minutesSeconds) => {

    let result= Math.round(minutesSeconds)*60 + (((minutesSeconds % 1)*100).toFixed(2) )
    return result
}

const secondsToMinutesSeconds = (secs) => {


    let minutes = Math.floor(secs / 60);
    let seconds = (secs - minutes * 60 ) / 100 ;

    return (minutes+seconds).toFixed(2)
}