import '@testing-library/jest-dom';
import '@testing-library/jest-dom/extend-expect';
import { render } from '@testing-library/react';
import Footer from 'components/footer/Footer';
import { SongNameChangeContextProvider } from 'hooks/useSongChangeContextApi';
import { BrowserRouter } from 'react-router-dom';

test('Render footer', () => {
  const component = render(
    <BrowserRouter>
      <SongNameChangeContextProvider>
        <Footer />
      </SongNameChangeContextProvider>
    </BrowserRouter>,
  );
  expect(component).toBeTruthy();
});
