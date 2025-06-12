// import React from 'react';
// import { render, screen, fireEvent, waitFor } from '@testing-library/react';
// import AboutModal from './AboutModal';

// // Mock window.open for testing
// const mockWindowOpen = jest.fn();
// Object.defineProperty(window, 'open', {
//   value: mockWindowOpen,
//   writable: true,
// });

// // Mock Global module to avoid package.json issues
// jest.mock('global/global', () => ({
//   default: {
//     APPVERSION: 'v2.2.0',
//     repositoryUrl: 'https://github.com/AntonioMrtz/SpotifyElectron',
//   },
//   APPVERSION: 'v2.2.0',
// }));

// // Mock i18next
// jest.mock('i18next', () => ({
//   t: (key: string, options?: any) => {
//     const translations: Record<string, string> = {
//       'aboutModal.title': 'About SpotifyElectron',
//       'aboutModal.version': `Version ${options?.version || 'v1.0.0'}`,
//       'aboutModal.projectLinks': 'Project Links',
//       'aboutModal.officialWebsite': 'Official Website',
//       'aboutModal.githubRepository': 'GitHub Repository',
//       'aboutModal.documentation': 'Documentation',
//       'aboutModal.createdBy': 'Created by',
//       'aboutModal.connectDeveloper': 'Connect with the developer:',
//       'aboutModal.supportText':
//         'Found this helpful? Support the project by starring it on GitHub!',
//       'aboutModal.starButton': 'Star on GitHub',
//     };
//     return translations[key] || key;
//   },
// }));

// describe('AboutModal', () => {
//   beforeEach(() => {
//     jest.clearAllMocks();
//   });

//   test('renders modal when open is true', () => {
//     render(<AboutModal open={true} onClose={jest.fn()} />);

//     const dialog = screen.getByRole('dialog');
//     expect(dialog).toBeTruthy();

//     const title = screen.getByText('About SpotifyElectron');
//     expect(title).toBeTruthy();
//   });

//   test('does not render modal when open is false', () => {
//     render(<AboutModal open={false} onClose={jest.fn()} />);

//     const dialog = screen.queryByRole('dialog');
//     expect(dialog).toBeFalsy();
//   });

//   test('displays app version correctly', () => {
//     render(<AboutModal open={true} onClose={jest.fn()} />);

//     const versionText = screen.getByText(/Version v\d+\.\d+\.\d+/);
//     expect(versionText).toBeTruthy();
//   });

//   test('closes modal when close button is clicked', () => {
//     const onClose = jest.fn();
//     render(<AboutModal open={true} onClose={onClose} />);

//     const closeButton = screen.getByLabelText('Close about dialog');
//     fireEvent.click(closeButton);

//     expect(onClose).toHaveBeenCalledTimes(1);
//   });

//   test('opens external links using window.open', async () => {
//     render(<AboutModal open={true} onClose={jest.fn()} />);

//     const githubButton = screen.getByText('GitHub Repository');
//     fireEvent.click(githubButton);

//     await waitFor(() => {
//       expect(mockWindowOpen).toHaveBeenCalledWith(
//         expect.stringContaining('github.com'),
//         '_blank',
//       );
//     });
//   });

//   test('handles GitHub star button click', async () => {
//     render(<AboutModal open={true} onClose={jest.fn()} />);

//     const starButton = screen.getByText('Star on GitHub');
//     fireEvent.click(starButton);

//     await waitFor(() => {
//       expect(mockWindowOpen).toHaveBeenCalledWith(
//         expect.stringContaining('github.com'),
//         '_blank',
//       );
//     });
//   });

//   test('renders all required project links', () => {
//     render(<AboutModal open={true} onClose={jest.fn()} />);

//     expect(screen.getByText('Official Website')).toBeTruthy();
//     expect(screen.getByText('GitHub Repository')).toBeTruthy();
//     expect(screen.getByText('Documentation')).toBeTruthy();
//   });

//   test('renders developer information', () => {
//     render(<AboutModal open={true} onClose={jest.fn()} />);

//     expect(screen.getByText(/Created by/)).toBeTruthy();
//     expect(screen.getByText('AntonioMrtz')).toBeTruthy();
//   });

//   test('renders social media links', () => {
//     render(<AboutModal open={true} onClose={jest.fn()} />);

//     expect(screen.getByText('Connect with the developer:')).toBeTruthy();
//     expect(screen.getByText('🐦 Twitter')).toBeTruthy();
//     expect(screen.getByText('💼 LinkedIn')).toBeTruthy();
//     expect(screen.getByText('✉️ Email')).toBeTruthy();
//   });

//   test('handles social media link clicks', async () => {
//     render(<AboutModal open={true} onClose={jest.fn()} />);

//     const twitterButton = screen.getByText('🐦 Twitter');
//     fireEvent.click(twitterButton);

//     await waitFor(() => {
//       expect(mockWindowOpen).toHaveBeenCalledWith(
//         expect.stringContaining('twitter.com'),
//         '_blank',
//       );
//     });
//   });

//   test('renders with proper MUI Dialog structure', () => {
//     render(<AboutModal open={true} onClose={jest.fn()} />);

//     const dialog = screen.getByRole('dialog');
//     expect(dialog).toBeTruthy();

//     // Check for proper ARIA attributes
//     expect(dialog.getAttribute('aria-labelledby')).toBeTruthy();
//   });

//   test('uses internationalization for all text content', () => {
//     render(<AboutModal open={true} onClose={jest.fn()} />);

//     // Check that i18next keys are being used
//     expect(screen.getByText('About SpotifyElectron')).toBeTruthy();
//     expect(screen.getByText('Project Links')).toBeTruthy();
//     expect(screen.getByText('Created by')).toBeTruthy();
//   });
// });
