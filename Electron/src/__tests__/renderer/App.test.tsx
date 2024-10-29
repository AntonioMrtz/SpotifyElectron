import '@testing-library/jest-dom';
import { render } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { BrowserRouter } from 'react-router-dom';
import { SongNameChangeContextProvider } from 'hooks/useSongChangeContextApi';
import App from '../../renderer/App';

const scrollToMock = jest.fn();
Object.defineProperty(window, 'scrollTo', { value: scrollToMock });

describe('App', () => {
  it('should render', () => {
    expect(
      render(
        <BrowserRouter>
          <SongNameChangeContextProvider>
            <App />
          </SongNameChangeContextProvider>
        </BrowserRouter>,
      ),
    ).toBeTruthy();
  });
});
