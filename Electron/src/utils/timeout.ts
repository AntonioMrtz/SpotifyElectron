const timeout = (ms: number | undefined) =>
  new Promise((_resolve, reject) => {
    setTimeout(() => reject(new Error('Timeout')), ms);
  });

export default timeout;
