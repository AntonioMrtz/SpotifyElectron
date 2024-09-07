import '@testing-library/jest-dom/extend-expect';
import {
  getToken,
  getTokenHeader,
  getTokenRole,
  getTokenUsername,
} from 'utils/token';
import UserType from 'utils/role';

const token =
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NfdG9rZW4iOiJwcnVlYmEiLCJyb2xlIjoidXNlciIsInRva2VuX3R5cGUiOiJiZWFyZXIiLCJleHAiOjE2OTgwNzQzNzl9.uohsDyqBKKL8FEiWS7HkjmgKQ33iiGiTZx1ZHXu_MdY';
const username = 'prueba';
const userType = UserType.USER;

// Set up mock localStorage
const mockLocalStorage = {
  getItem: jest.fn(() => {
    return token;
  }),
};

Object.defineProperty(window, 'localStorage', {
  value: mockLocalStorage,
});

test('Get jwt token', () => {
  const jwtToken = getToken();

  expect(token).toEqual(jwtToken);
});

test('Get jwt token username', () => {
  const usernameJwtToken = getTokenUsername();

  expect(username).toEqual(usernameJwtToken);
});

test('Get jwt token role', () => {
  const userTypeJwtToken = getTokenRole();

  expect(userType).toEqual(userTypeJwtToken);
});

test('Get jwt header', () => {
  const headerJwtToken = getTokenHeader();

  expect({ Authorization: `Bearer ${token}` }).toMatchObject(headerJwtToken);
});
