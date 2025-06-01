import '@testing-library/jest-dom';
import { render } from '@testing-library/react';
import Footer from 'components/footer/Footer';
import { NowPlayingContextProvider } from 'providers/NowPlayingProvider';
import { BrowserRouter } from 'react-router-dom';

test('Render footer', () => {
  const component = render(
    <BrowserRouter>
      <NowPlayingContextProvider>
        <Footer />
      </NowPlayingContextProvider>
    </BrowserRouter>,
  );
  expect(component).toBeTruthy();
});
