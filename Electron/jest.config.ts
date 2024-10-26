const config = {
  moduleDirectories: ['node_modules', 'src'],
  moduleFileExtensions: ['js', 'jsx', 'ts', 'tsx', 'json'],
  moduleNameMapper: {
    '\\.(jpg|jpeg|png|gif|eot|otf|webp|svg|ttf|woff|woff2|mp4|webm|wav|mp3|m4a|aac|oga)$':
      '<rootDir>/.erb/mocks/fileMock.js',
    '\\.(css|less|sass|scss)$': 'identity-obj-proxy',
  },
  setupFiles: [
    './.erb/scripts/check-build-exists.ts',
    './src/__tests__/utils/loadLocalization.ts',
    './src/__tests__/utils/loadOpenAPI.ts',
  ],
  testEnvironment: 'jsdom',
  testEnvironmentOptions: {
    url: 'http://localhost/',
  },
  testPathIgnorePatterns: [
    'release/app/dist',
    '.erb/dll',
    'src/__tests__/utils',
  ],
  transform: {
    '\\.(ts|tsx|js|jsx)$': 'ts-jest',
  },
};

module.exports = config;
