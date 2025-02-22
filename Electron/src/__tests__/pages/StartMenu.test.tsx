import {
  render,
  screen,
  fireEvent,
  waitFor,
  act,
} from '@testing-library/react';
import '@testing-library/jest-dom';
import StartMenu from 'pages/StartMenu/StartMenu';
import { getToken } from 'utils/token';
import timeout from 'utils/timeout';
import { CancelablePromise } from 'swagger/api';
import { LoginService } from '../../swagger/api/services/LoginService';
import '@testing-library/jest-dom/extend-expect';

jest.mock('../../swagger/api/services/LoginService');
jest.mock('utils/token');
jest.mock('utils/timeout');

describe('StartMenu Component', () => {
  const setIsLoggedMock = jest.fn();
  const setIsSigningUpMock = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
    jest.resetAllMocks();
  });

  test('renders the component and displays title and form', async () => {
    await act(async () => {
      render(
        <StartMenu
          setIsLogged={setIsLoggedMock}
          setIsSigningUp={setIsSigningUpMock}
        />,
      );
    });

    expect(screen.getByText('Spotify Electron')).toBeInTheDocument();
    expect(
      screen.getByText('Inicia sesión en Spotify Electron'),
    ).toBeInTheDocument();
    expect(screen.getByText('Nombre de usuario')).toBeInTheDocument();
    expect(screen.getByText('Contraseña')).toBeInTheDocument();
  });

  test('handles input changes and form submission', async () => {
    (LoginService.loginUserLoginPost as jest.Mock).mockResolvedValue(
      'mock-jwt-token',
    );
    (getToken as jest.Mock).mockReturnValue('mock-jwt-token');

    (
      LoginService.loginUserWithJwtLoginTokenTokenPost as jest.Mock
    ).mockResolvedValue('mock-jwt-token');
    (getToken as jest.Mock).mockReturnValue('mock-jwt-token');

    await act(async () => {
      render(
        <StartMenu
          setIsLogged={setIsLoggedMock}
          setIsSigningUp={setIsSigningUpMock}
        />,
      );
    });

    await act(async () => {
      fireEvent.change(screen.getByPlaceholderText('Nombre de usuario'), {
        target: { value: 'user123' },
      });
      fireEvent.change(screen.getByPlaceholderText('Contraseña'), {
        target: { value: 'password123' },
      });
      fireEvent.click(screen.getByText('Iniciar sesión'));

      await waitFor(() => {
        expect(setIsLoggedMock).toHaveBeenCalledWith(true);
      });
    });
  });

  test('handles auto-login on component mount', async () => {
    (
      LoginService.loginUserWithJwtLoginTokenTokenPost as jest.Mock
    ).mockResolvedValue(undefined);
    (getToken as jest.Mock).mockReturnValue('mock-jwt-token');

    await act(async () => {
      render(
        <StartMenu
          setIsLogged={setIsLoggedMock}
          setIsSigningUp={setIsSigningUpMock}
        />,
      );
    });

    expect(setIsLoggedMock).toHaveBeenCalledWith(true);
  });

  test('handles auto-login timeout on component mount and displays error popover', async () => {
    (getToken as jest.Mock).mockReturnValue('mock-jwt-token');
    const mockLoginPromise = new CancelablePromise(() => {});
    (
      LoginService.loginUserWithJwtLoginTokenTokenPost as jest.Mock
    ).mockImplementationOnce(() => mockLoginPromise);
    (timeout as jest.Mock).mockRejectedValueOnce(new Error('Timeout'));

    await act(async () => {
      render(
        <StartMenu
          setIsLogged={setIsLoggedMock}
          setIsSigningUp={setIsSigningUpMock}
        />,
      );
    });

    expect(mockLoginPromise.isCancelled).toBe(true);
    expect(
      screen.getByText('El servidor esta iniciándose'),
    ).toBeInTheDocument();
  });

  test('handles login error and displays error popover', async () => {
    (LoginService.loginUserLoginPost as jest.Mock).mockRejectedValue(
      new Error('Login error'),
    );

    await act(async () => {
      render(
        <StartMenu
          setIsLogged={setIsLoggedMock}
          setIsSigningUp={setIsSigningUpMock}
        />,
      );
    });

    fireEvent.change(screen.getByPlaceholderText('Nombre de usuario'), {
      target: { value: 'user123' },
    });
    fireEvent.change(screen.getByPlaceholderText('Contraseña'), {
      target: { value: 'password123' },
    });
    await act(async () => {
      fireEvent.click(screen.getByText('Iniciar sesión'));
    });

    expect(setIsLoggedMock).toHaveBeenCalledWith(false);
    expect(
      screen.getByText('Los credenciales introducidos no son válidos'),
    ).toBeInTheDocument();
  });

  test('handles login timeout and displays error popover', async () => {
    const mockLoginPromise = new CancelablePromise(() => {});
    (LoginService.loginUserLoginPost as jest.Mock).mockImplementationOnce(
      () => mockLoginPromise,
    );
    (timeout as jest.Mock).mockRejectedValueOnce(new Error('Timeout'));

    await act(async () => {
      render(
        <StartMenu
          setIsLogged={setIsLoggedMock}
          setIsSigningUp={setIsSigningUpMock}
        />,
      );
    });

    fireEvent.change(screen.getByPlaceholderText('Nombre de usuario'), {
      target: { value: 'user123' },
    });
    fireEvent.change(screen.getByPlaceholderText('Contraseña'), {
      target: { value: 'password123' },
    });
    await act(async () => {
      fireEvent.click(screen.getByText('Iniciar sesión'));
    });

    expect(mockLoginPromise.isCancelled).toBe(true);
    expect(setIsLoggedMock).toHaveBeenCalledWith(false);
    expect(
      screen.getByText('El servidor esta iniciándose'),
    ).toBeInTheDocument();
  });

  test('handles register button click', async () => {
    await act(async () => {
      render(
        <StartMenu
          setIsLogged={setIsLoggedMock}
          setIsSigningUp={setIsSigningUpMock}
        />,
      );
    });

    act(() => {
      fireEvent.click(screen.getByText('Regístrate en Spotify Electron'));
    });

    expect(setIsSigningUpMock).toHaveBeenCalledWith(true);
  });
});
