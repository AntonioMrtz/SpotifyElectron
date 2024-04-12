import jwtDecode from 'jwt-decode';

interface DecodedJwt {
  access_token: string;
  role: string;
}

namespace Token {
  export const getToken = () => {
    const jwt = localStorage.getItem('jwt');

    if (jwt) {
      return jwt;
    }

    return '';
  };

  export const getTokenHeader = () => {
    const jwt = localStorage.getItem('jwt');

    if (jwt) {
      return { Authorization: jwt };
    }

    return { Authorization: '' };
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
}

export default Token;
