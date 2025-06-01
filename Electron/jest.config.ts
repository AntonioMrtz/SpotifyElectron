const config = {
  moduleDirectories: ['node_modules', 'src'],
  moduleFileExtensions: ['js', 'jsx', 'ts', 'tsx', 'json'],
  moduleNameMapper: {
    '\\.(jpg|jpeg|png|gif|eot|otf|webp|svg|ttf|woff|woff2|mp4|webm|wav|mp3|m4a|aac|oga)$':
      '<rootDir>/.erb/mocks/fileMock.js',
    '\\.(css|less)$': 'identity-obj-proxy',
  },
  setupFiles: [
    './.erb/scripts/check-build-exists.ts',
    './src/__tests__/setup/setup.jest.ts',
    './src/__tests__/setup/loadLocalization.jest.ts',
    './src/__tests__/setup/loadOpenAPI.jest.ts',
  ],
  testEnvironment: 'jsdom',
  testEnvironmentOptions: {
    url: 'http://localhost/',
  },
  testPathIgnorePatterns: [
    'release/app/dist',
    '.erb/dll',
    'src/__tests__/setup',
  ],
  transform: {
    '\\.(ts|tsx|js|jsx)$': 'ts-jest',
  },
};

module.exports = config;
