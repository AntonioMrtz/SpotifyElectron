import '@testing-library/jest-dom';
import { act, fireEvent, render } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import StartMenu from 'pages/StartMenu/StartMenu';

afterEach(() => {
  jest.clearAllMocks();
});

test('render StartMenu', () => {
  expect(
    render(<StartMenu setIsLogged={() => {}} setIsSigningUp={() => {}} />),
  ).toBeTruthy();
});

test('StartMenu correct text', () => {
  const component = render(
    <StartMenu setIsLogged={jest.fn()} setIsSigningUp={jest.fn()} />,
  );

  expect(component.container).toHaveTextContent(
    'Inicia sesión en Spotify Electron',
  );
});

test('Login failed', () => {
  const mockSetIsLogged = jest.fn();

  const component = render(
    <StartMenu setIsLogged={mockSetIsLogged} setIsSigningUp={jest.fn()} />,
  );

  const loginButton = component.getByText('Iniciar sesión');
  fireEvent.click(loginButton);

  expect(
    component.queryByText('No se ha podido iniciar sesión'),
  ).toBeInTheDocument();

  const popover = document.getElementById('button-info-popover');
  expect(popover).toBeVisible();
  if (popover) {
    fireEvent.click(popover);
  }

  fireEvent.click(document.body);

  expect(component.queryByText('No se ha podido iniciar sesión')).toBeNull();
  expect(popover).not.toBeVisible();
});

test('Login success', async () => {
  const setIsLogged = jest.fn();
  const setIsSigningUp = jest.fn();

  global.fetch = jest.fn(() =>
    Promise.resolve({
      json: () => Promise.resolve({}),
      status: 200,
    }),
  ) as jest.Mock;

  const component = render(
    <StartMenu setIsLogged={setIsLogged} setIsSigningUp={setIsSigningUp} />,
  );

  // Simulate user input

  const inputName = component.getByPlaceholderText('Nombre de usuario');
  const inputPassword = component.getByPlaceholderText('Contraseña');

  fireEvent.change(inputName, {
    target: { value: 'testuser' },
  });
  fireEvent.change(inputPassword, {
    target: { value: 'testpassword' },
  });

  const loginButton = component.getByText('Iniciar sesión');

  await act(async () => {
    fireEvent.click(loginButton);
  });

  expect(setIsLogged).toHaveBeenCalledWith(true);
});

test('Change to register menu', () => {
  const mockSetIsRegistering = jest.fn();

  const component = render(
    <StartMenu setIsLogged={jest.fn()} setIsSigningUp={mockSetIsRegistering} />,
  );

  const regiserButton = component.getByText('Regístrate en Spotify Electron');
  fireEvent.click(regiserButton);

  expect(mockSetIsRegistering).toHaveBeenCalledWith(true);
});
