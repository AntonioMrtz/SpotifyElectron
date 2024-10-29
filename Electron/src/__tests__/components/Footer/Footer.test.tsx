import '@testing-library/jest-dom';
import '@testing-library/jest-dom/extend-expect';
import { render } from '@testing-library/react';
import Footer from 'components/footer/Footer';
import { BrowserRouter } from 'react-router-dom';

test('Render footer', () => {
  const component = render(
    <BrowserRouter>
      <Footer />
    </BrowserRouter>,
  );
  expect(component).toBeTruthy();
});
