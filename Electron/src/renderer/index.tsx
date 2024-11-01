import { createRoot } from 'react-dom/client';
import { HashRouter } from 'react-router-dom';
// Import bootstrap before app and custom styles so own code it's not overrided
import 'bootstrap/dist/css/bootstrap.min.css';
// import 'bootstrap/dist/js/bootstrap.bundle.min.js'; // Only needed for dynamic components
import App from './App';
import './index.css';
import initOpenAPIClient from '../swagger/openAPIClientInit';

initOpenAPIClient();
const container = document.getElementById('root') as HTMLElement;
const root = createRoot(container);
root.render(
  <HashRouter>
    <App />
  </HashRouter>,
);
