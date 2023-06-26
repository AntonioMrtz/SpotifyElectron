import { useState, useEffect } from 'react';

interface FetchResult {
  data: any;
  loading: boolean | null;
  error: string | null;
}

const useFetch = (url: string): FetchResult => {
  const [data, setData] = useState<any>("");
  const [loading, setLoading] = useState<boolean | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    setData(null);
    setError(null);

    fetch(url, {"headers":{ 'Access-Control-Allow-Origin': '*' }})
      .then((res) => {
        setLoading(false);
        res.json().then((jsonData) => {
          //console.log(jsonData)
          if (jsonData.content) {
            setData(jsonData.content);
          } else {
            setData(jsonData);
          }
        });
      })
      .catch((err) => {
        setLoading(false);
        setError('An error occurred during Fetch: '+url);
      });
  }, [url]);

  return { data, loading, error };
}

export default useFetch;
