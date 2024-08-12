const getMockHeaders = () => {
  return {
    get: (header: any) => {
      if (header.toLowerCase() === 'content-type') {
        return 'application/json'; // or 'application/problem+json'
      }
      return null;
    },
  };
};

export default getMockHeaders;
