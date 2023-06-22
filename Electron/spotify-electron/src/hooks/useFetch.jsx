import { useState,useEffect } from "react";

export const useFetch = (url,field) => {
    const [data, setData] = useState();

    
    useEffect(() => {
        fetch(url,{"Access-Control-Allow-Origin": "*"})
            .then((res) => res.json())
            .then((res) => {
                setData(res[field]);
                //console.log(res)
            })
            .catch(console.log);
    }, []);

    return {
        data,
    };
};
