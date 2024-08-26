const timeout = (ms: number | undefined) =>
  new Promise((_, reject) => {
    setTimeout(() => reject(new Error('Timeout')), ms);
  });

export default timeout;
