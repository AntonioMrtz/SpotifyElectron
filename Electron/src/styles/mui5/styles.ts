/* eslint-disable import/prefer-default-export */
// TODO Delete this eslint rule when more styles are added
export const inputStyle = {
  width: '100%',
  color: 'var(--primary-white)',
  backgroundColor: 'var(--separator-white)', // Default background color for the input
  borderRadius: '4px',

  '& .MuiInputBase-root': {
    backgroundColor: 'var(--separator-white)', // Ensure background is set for the root
  },

  '& .MuiInputBase-input': {
    color: 'var(--primary-white)', // Input text color
    backgroundColor: 'var(--separator-white)', // Input default background color
    '&:focus': {
      backgroundColor: 'var(--focus-grey-background)', // Background color when focused
    },
    borderRadius: '4px',
  },

  '& .MuiInputLabel-root': {
    color: 'var(--primary-white)', // Label color
  },

  '& .MuiInputLabel-root.Mui-focused': {
    color: 'var(--primary-white)', // Label color when focused
  },

  '& .MuiOutlinedInput-root': {
    '& fieldset': {
      borderColor: 'transparent', // Default border color
      borderWidth: '1px', // Default border thickness
      borderRadius: '4px',
    },
    '&:hover fieldset': {
      borderColor: 'transparent', // Border color on hover
    },
    '&.Mui-focused fieldset': {
      borderColor: 'var(--primary-white)', // Border color when focused
      borderWidth: '1px', // Border thickness when focused
    },
  },
};
