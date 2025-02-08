// eslint-disable-next-line import/prefer-default-export
export const sanitizeUserName = (userName: string) => {
  return userName.replace(/[^a-zA-Z0-9_]/g, '');
};
