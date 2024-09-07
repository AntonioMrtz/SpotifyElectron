import jwtDecode from 'jwt-decode';

interface DecodedJwt {
  access_token: string;
  role: string;
}

const JWT_TOKEN_LOCAL_STORAGE_KEY = 'jwt';

export const getToken = () => {
  const jwt = localStorage.getItem(JWT_TOKEN_LOCAL_STORAGE_KEY);

  if (jwt) {
    return jwt;
  }

  return '';
};

export const deleteToken = () => {
  localStorage.removeItem(JWT_TOKEN_LOCAL_STORAGE_KEY);
};

export const getTokenHeader = () => {
  const jwt = localStorage.getItem(JWT_TOKEN_LOCAL_STORAGE_KEY);

  if (jwt) {
    return { Authorization: `Bearer ${jwt}` };
  }

  return { Authorization: 'Bearer ' };
};

export const getTokenUsername = () => {
  try {
    const jwt = getToken();
    const decodedJwt = jwtDecode<DecodedJwt>(jwt);

    return decodedJwt.access_token;
  } catch {
    console.log('Unable to get username from Jwt Token');
  }

  return '';
};

export const getTokenRole = () => {
  try {
    const jwt = getToken();
    const decodedJwt = jwtDecode<DecodedJwt>(jwt);

    return decodedJwt.role;
  } catch {
    console.log('Unable to get username from Jwt Token');
  }

  return '';
};
