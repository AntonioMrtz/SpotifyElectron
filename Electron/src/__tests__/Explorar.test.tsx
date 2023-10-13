import '@testing-library/jest-dom';
import { act, render } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import Explorar from 'pages/Explorar/Explorar';
import { BrowserRouter } from 'react-router-dom';

global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () => Promise.resolve({ ROCK: 'Rock', POP: 'Pop' }),
    status: 200,
  })
) as jest.Mock;

test('Render Explorar and get Genres', async () => {
  const component = await act(() => {
    return render(
      <BrowserRouter>
        <Explorar />
      </BrowserRouter>
    );
  });
  expect(component).toBeTruthy();
});
