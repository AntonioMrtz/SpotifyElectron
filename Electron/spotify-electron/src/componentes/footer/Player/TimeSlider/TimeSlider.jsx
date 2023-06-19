import {useState} from "react";
import Box from "@mui/material/Box";
import Slider from "@mui/material/Slider";
import styles from "./timeSlider.module.css";
import { useEffect } from "react";

export default function TimeSlider(props) {


    const minutesSecondsToSeconds = (minutesSeconds) => {

        let result= Math.round(minutesSeconds)*60 + (((minutesSeconds % 1)*100).toFixed(2) )
        
        //console.log("RESULT "+Math.round(minutesSeconds)*60+"    "+(((minutesSeconds % 1)*100).toFixed(2)))
        return result
    }

    const secondsToMinutesSeconds = (secs) => {


        let minutes = Math.floor(secs / 60);
        let seconds = (secs - minutes * 60 ) / 100 ;

        return (minutes+seconds).toFixed(2)
    }


    const [songDuration,setSongDuration] = useState( 0 )
    const [songPlayTime,setsongPlayTime] = useState( 0 )
    const [songPlayTimeMinutesSeconds,setSongPlayTimeMinutesSeconds] = useState( +(0.00.toFixed(2)))


    const handlePlayTime = (event,value) => {

        console.log("cambio con value = " + value);


        setsongPlayTime(value);
        props.changePlayTime(value);
        console.log("cambio con songPlayTime = " + songPlayTime);
        console.log("duration = " + props.songDuration);

    }
    
    useEffect(() => {
        
        setsongPlayTime(props.playTime)
        setSongPlayTimeMinutesSeconds(secondsToMinutesSeconds(props.playTime))
       
    },[props.playTime])
    


    return (
        <Box width="100%" paddingRight="2%" display="flex">
            <p>{songPlayTime===undefined ?  (0.00.toFixed(2)) : songPlayTimeMinutesSeconds}</p>

            <Slider
                size="small"
                min={0}
                max={props.songDuration}
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

            <p>{secondsToMinutesSeconds(props.songDuration)}</p>
        </Box>
    );
}
