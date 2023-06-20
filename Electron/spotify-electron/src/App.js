import styles from './AppCss.module.css';
import Sidebar from './componentes/Sidebar/Sidebar'
import Home from './componentes/Home/Home'
import Explorar from './componentes/Explorar/Explorar';
import Footer from './componentes/footer/Footer';


import { RouterProvider, createBrowserRouter } from 'react-router-dom';

function App() {


  const router = createBrowserRouter([
    {
      path: '/',
      element: <Home />,
    },
    {
      path: '/explorar',
      element:  <Explorar/>,
    }
  ]);


  return (
    <div className={`App d-flex flex-column ${styles.appBackground}`}>

      <div className='d-flex flex-row'>

      <Sidebar />
      <div className={`App d-flex container-fluid ${styles.mainContentWrapper}`}>
        <RouterProvider router={router} />

      </div>

      </div>

      <Footer/>

    </div>
  );
}

export default App;
