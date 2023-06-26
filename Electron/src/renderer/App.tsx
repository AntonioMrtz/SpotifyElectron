import styles from './AppCss.module.css';
import Sidebar from '../componentes/Sidebar/Sidebar';
import Home from '../componentes/Home/Home';
import Explorar from '../componentes/Explorar/Explorar';
import Footer from '../componentes/footer/Footer';
import { BrowserRouter, Route,Routes } from 'react-router-dom';

function App() {
 
  return (
    <div className={`App d-flex flex-column ${styles.appBackground}`}>
      <div className="d-flex flex-row">
        <Sidebar />
        <div
          className={`App d-flex container-fluid ${styles.mainContentWrapper}`}
        >
          <BrowserRouter>
          <Routes>

            <Route path="/" Component={Home} />
            <Route path="/explorar" Component={Explorar} />
            <Route path="*" Component={Home} />
          </Routes>

          </BrowserRouter>
        </div>
      </div>

      <Footer />
    </div>
  );
}

export default App;
