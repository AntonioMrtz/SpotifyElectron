import '@testing-library/jest-dom/extend-expect';
import Token from 'utils/token';
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
  const jwtToken = Token.getToken();

  expect(token).toEqual(jwtToken);
});

test('Get jwt token username', () => {
  const usernameJwtToken = Token.getTokenUsername();

  expect(username).toEqual(usernameJwtToken);
});

test('Get jwt token role', () => {
  const userTypeJwtToken = Token.getTokenRole();

  expect(userType).toEqual(userTypeJwtToken);
});

test('Get jwt header', () => {
  const headerJwtToken = Token.getTokenHeader();

  expect({ Authorization: token }).toMatchObject(headerJwtToken);
});
