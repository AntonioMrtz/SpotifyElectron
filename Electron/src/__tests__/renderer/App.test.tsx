import '@testing-library/jest-dom';
import { render } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { BrowserRouter } from 'react-router-dom';
import App from '../../renderer/App';
import { SidebarProvider } from '../../components/Sidebar/SidebarContext'; // Adjust the path as necessary

const scrollToMock = jest.fn();
Object.defineProperty(window, 'scrollTo', { value: scrollToMock });

describe('App', () => {
  it('should render', () => {
    expect(
      render(
        <BrowserRouter>
          <SidebarProvider>
            {' '}
            {/* Wrap App with SidebarProvider */}
            <App />
          </SidebarProvider>
        </BrowserRouter>,
      ),
    ).toBeTruthy();
  });
});
