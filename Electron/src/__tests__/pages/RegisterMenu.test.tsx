import '@testing-library/jest-dom';
import { act, fireEvent, render, screen } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import RegisterMenu from 'pages/StartMenu/RegisterMenu';
import Global from 'global/global';
import timeout from 'utils/timeout';
import { CancelablePromise } from 'swagger/api';
import { UsersService } from '../../swagger/api/services/UsersService';

jest.mock('../../swagger/api/services/UsersService');
jest.mock('utils/timeout');

describe('RegisterMenu Component', () => {
  afterEach(() => {
    jest.clearAllMocks();
    jest.resetAllMocks();
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
    expect(popover).toBeInTheDocument();
    if (popover) {
      fireEvent.click(popover);
    }

    expect(
      component.queryByText(
        'No se han introducido todos los datos de registro obligatorios',
      ),
    ).toBeNull();
    expect(popover).not.toBeInTheDocument();
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
    expect(popover).toBeInTheDocument();
    if (popover) {
      fireEvent.click(popover);
    }

    fireEvent.click(document.body);

    expect(
      component.queryByText(
        'No se han introducido todos los datos de registro obligatorios',
      ),
    ).toBeNull();
    expect(popover).not.toBeInTheDocument();
  });

  test('Register failed different password inputs', () => {
    const mockSetIsSigningUp = jest.fn();

    global.fetch = jest.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve({}),
        status: 200,
        ok: true,
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

  test('Register failed request timeout', async () => {
    const mockSetIsSigningUp = jest.fn();

    const mockRegisterPromise = new CancelablePromise(() => {});
    (UsersService.createUserUsersPost as jest.Mock).mockImplementationOnce(
      () => mockRegisterPromise,
    );
    (timeout as jest.Mock).mockRejectedValueOnce(new Error('Timeout'));

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
      target: { value: 'testphoto' },
    });
    fireEvent.change(inputConfirmPassword, {
      target: { value: 'testpassword' },
    });

    const registerButton = component.getByText('Registrar');

    await act(async () => {
      fireEvent.click(registerButton);
    });

    expect(mockRegisterPromise.isCancelled).toBe(true);
    expect(
      screen.getByText('El servidor esta iniciándose'),
    ).toBeInTheDocument();
  });

  test('Register success', async () => {
    const mockSetIsSigningUp = jest.fn();

    global.fetch = jest.fn((url: string) => {
      if (
        url ===
        `${Global.backendBaseUrl}/users/?name=testuser&photo=testphoto&password=testpassword`
      ) {
        return Promise.resolve({
          json: () => Promise.resolve({}),
          status: 201,
          ok: true,
        }).catch((error) => {
          console.log(error);
        });
      }

      // In case the URL doesn't match, return a rejected promise
      return Promise.reject(new Error(`Unhandled URL in fetch mock: ${url}`));
    }) as jest.Mock;

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
      target: { value: 'testphoto' },
    });
    fireEvent.change(inputConfirmPassword, {
      target: { value: 'testpassword' },
    });

    const registerButton = component.getByText('Registrar');

    await act(async () => {
      fireEvent.click(registerButton);
    });

    const popover = document.getElementById('button-info-popover');
    expect(popover).toBeInTheDocument();
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
});
