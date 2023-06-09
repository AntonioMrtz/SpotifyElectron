import logo from './logo.svg';
import styles from './AppCss.module.css';
import Sidebar from './componentes/sidebar/Sidebar'
import Home from './componentes/home/Home'


import { RouterProvider, createBrowserRouter } from 'react-router-dom';

function App() {


  const router = createBrowserRouter([
    {
      path: '/',
      element: <Home />,
    },
    {
      path: '/explorar',
      element:  <Home/>,
    }
  ]);


  return (
    <div className={`App d-flex flex-row ${styles.appBackground}`}>

      <Sidebar />

      <RouterProvider router={router} />


    </div>
  );
}

export default App;
