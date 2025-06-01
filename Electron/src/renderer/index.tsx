import { createRoot } from 'react-dom/client';
import { initializeI18n } from 'i18n/i18n';
// Import bootstrap before app and custom styles so own code it's not overrided
import 'bootstrap/dist/css/bootstrap.min.css';
// import 'bootstrap/dist/js/bootstrap.bundle.min.js'; // Only needed for dynamic components
import { StrictMode } from 'react';
import App from './App';
import './index.css';
import initOpenAPIClient from '../swagger/openAPIClientInit';

initOpenAPIClient();
const container = document.getElementById('root') as HTMLElement;
const root = createRoot(container);

initializeI18n()
  .then(() => {
    return root.render(
      <StrictMode>
        <App />
      </StrictMode>,
    );
  })
  .catch((err) => {
    console.log(`Error initializing app: ${err}`);
  });
