import { useEffect } from 'react'
import { useLocation } from 'react-router-dom';


export default function Playlist() {

  const location = useLocation();
  const currentURL = location.pathname;


  return (
    <div>{currentURL}</div>
  )
}
