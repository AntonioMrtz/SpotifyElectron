import '@testing-library/jest-dom';
import { render } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { NowPlayingContextProvider } from 'providers/NowPlayingProvider';
import App from '../../renderer/App';

const scrollToMock = jest.fn();
Object.defineProperty(window, 'scrollTo', { value: scrollToMock });

describe('App', () => {
  it('should render', () => {
    expect(
      render(
        <BrowserRouter>
          <NowPlayingContextProvider>
            <App />
          </NowPlayingContextProvider>
        </BrowserRouter>,
      ),
    ).toBeTruthy();
  });
});
