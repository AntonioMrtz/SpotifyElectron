import { useState, useEffect } from 'react';

export const useFetch = (url) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(url,{"Access-Control-Allow-Origin": "*"});
        const jsonData = await response.json();
        setData(jsonData);
        setLoading(false);
      } catch (error) {
        // Handle error here
      }
    };

    fetchData();
  }, []); // Empty dependency array ensures this effect runs only once

  return { data, loading };
};

