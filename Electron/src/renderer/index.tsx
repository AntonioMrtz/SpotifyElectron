import { createRoot } from 'react-dom/client';
import { HashRouter } from 'react-router-dom';
import { initializeI18n } from 'i18n/i18n';
import App from './App';
import './index.css';
import initOpenAPIClient from '../swagger/openAPIClientInit';

initOpenAPIClient();
const container = document.getElementById('root') as HTMLElement;
const root = createRoot(container);

initializeI18n()
  .then(() => {
    return root.render(
      <HashRouter>
        <App />
      </HashRouter>,
    );
  })
  .catch((err) => {
    console.log(`Error initializing app: ${err}`);
  });
