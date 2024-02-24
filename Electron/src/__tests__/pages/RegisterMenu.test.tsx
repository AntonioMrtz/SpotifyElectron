import '@testing-library/jest-dom';
import { act, fireEvent, render } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import RegisterMenu from 'pages/StartMenu/RegisterMenu';

afterEach(() => {
  jest.clearAllMocks();
});

test('render RegisterMenu', () => {
  expect(render(<RegisterMenu setIsSigningUp={() => {}} />)).toBeTruthy();
});

test('RegisterMenu correct text', () => {
  const component = render(<RegisterMenu setIsSigningUp={jest.fn()} />);

  expect(component.container).toHaveTextContent(
    'Regístrate en Spotify Electron',
  );
});

test('Register failed not all required inputs filled', () => {
  const mockSetIsSigningUp = jest.fn();

  const component = render(
    <RegisterMenu setIsSigningUp={mockSetIsSigningUp} />,
  );

  const registerButton = component.getByText('Registrar');
  fireEvent.click(registerButton);

  expect(
    component.queryByText(
      'No se han introducido todos los datos de registro obligatorios',
    ),
  ).toBeInTheDocument();

  const popover = document.getElementById('button-info-popover');
  expect(popover).toBeVisible();
  if (popover) {
    fireEvent.click(popover);
  }

  fireEvent.click(document.body);

  expect(
    component.queryByText(
      'No se han introducido todos los datos de registro obligatorios',
    ),
  ).toBeNull();
  expect(popover).not.toBeVisible();
});

test('Register failed bad input', () => {
  const mockSetIsSigningUp = jest.fn();

  const component = render(
    <RegisterMenu setIsSigningUp={mockSetIsSigningUp} />,
  );

  const registerButton = component.getByText('Registrar');
  fireEvent.click(registerButton);

  expect(
    component.queryByText(
      'No se han introducido todos los datos de registro obligatorios',
    ),
  ).toBeInTheDocument();

  const popover = document.getElementById('button-info-popover');
  expect(popover).toBeVisible();
  if (popover) {
    fireEvent.click(popover);
  }

  fireEvent.click(document.body);

  expect(
    component.queryByText(
      'No se han introducido todos los datos de registro obligatorios',
    ),
  ).toBeNull();
  expect(popover).not.toBeVisible();
});

test('Register failed different password inputs', () => {
  const mockSetIsSigningUp = jest.fn();

  global.fetch = jest.fn(() =>
    Promise.resolve({
      json: () => Promise.resolve({}),
      status: 200,
    }),
  ) as jest.Mock;

  const component = render(
    <RegisterMenu setIsSigningUp={mockSetIsSigningUp} />,
  );

  // Simulate user input

  const inputName = component.getByPlaceholderText('Nombre de usuario');
  const inputPhoto = component.getByPlaceholderText('Foto de perfil');
  const inputPassword = component.getByPlaceholderText('Contraseña');
  const inputConfirmPassword = component.getByPlaceholderText(
    'Confirma tu contraseña',
  );

  fireEvent.change(inputName, {
    target: { value: 'testuser' },
  });
  fireEvent.change(inputPassword, {
    target: { value: 'testpassword' },
  });
  fireEvent.change(inputPhoto, {
    target: { value: 'testfoto' },
  });
  fireEvent.change(inputConfirmPassword, {
    target: { value: 'testpassworddiferente' },
  });

  const registerButton = component.getByText('Registrar');
  fireEvent.click(registerButton);

  expect(
    component.queryByText('Las contraseñas no coinciden'),
  ).toBeInTheDocument();
});

test('Register success', async () => {
  const mockSetIsSigningUp = jest.fn();

  global.fetch = jest.fn(() =>
    Promise.resolve({
      json: () => Promise.resolve({}),
      status: 201,
    }),
  ) as jest.Mock;

  const component = render(
    <RegisterMenu setIsSigningUp={mockSetIsSigningUp} />,
  );

  // Simulate user input

  const inputName = component.getByPlaceholderText('Nombre de usuario');
  const inputPhoto = component.getByPlaceholderText('Foto de perfil');
  const inputPassword = component.getByPlaceholderText('Contraseña');
  const inputConfirmPassword = component.getByPlaceholderText(
    'Confirma tu contraseña',
  );

  fireEvent.change(inputName, {
    target: { value: 'testuser' },
  });
  fireEvent.change(inputPassword, {
    target: { value: 'testpassword' },
  });
  fireEvent.change(inputPhoto, {
    target: { value: 'testfoto' },
  });
  fireEvent.change(inputConfirmPassword, {
    target: { value: 'testpassword' },
  });

  const registerButton = component.getByText('Registrar');

  await act(async () => {
    fireEvent.click(registerButton);
  });

  const popover = document.getElementById('button-info-popover');
  expect(popover).toBeVisible();
  if (popover) {
    fireEvent.click(popover);
  }

  expect(mockSetIsSigningUp).toHaveBeenCalledWith(false);
});

test('Change to login menu', () => {
  const mockSetIsSigningUp = jest.fn();

  const component = render(
    <RegisterMenu setIsSigningUp={mockSetIsSigningUp} />,
  );

  const regiserButton = component.getByText(
    'Inicia sesión en Spotify Electron',
  );
  fireEvent.click(regiserButton);

  expect(mockSetIsSigningUp).toHaveBeenCalledWith(false);
});
