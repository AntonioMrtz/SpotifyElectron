import '@testing-library/jest-dom';
import { act, render } from '@testing-library/react';
import * as router from 'react-router';
import '@testing-library/jest-dom/extend-expect';
import Home from 'pages/Home/Home';

const navigate = jest.fn();

beforeEach(() => {
  jest.spyOn(router, 'useNavigate').mockImplementation(() => navigate);
});

test('render Home', async () => {
  global.fetch = jest.fn(() =>
    Promise.resolve({
      json: () => Promise.resolve({}),
      status: 200,
    })
  ) as jest.Mock;

  const component = await act(() => {
    return render(<Home refreshSidebarData={jest.fn()} />);
  });

  expect(component).toBeTruthy();
});

test('Home fields', async () => {
  global.fetch = jest.fn(() =>
    Promise.resolve({
      json: () => Promise.resolve({}),
      status: 200,
    })
  ) as jest.Mock;

  const component = await act(() => {
    return render(<Home refreshSidebarData={jest.fn()} />);
  });

  expect(component.queryByText('Especialmente para ti')).toBeInTheDocument();

  expect(component.queryByText('Artistas destacados')).toBeInTheDocument();
});
