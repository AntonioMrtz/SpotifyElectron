import CircularProgress from '@mui/material/CircularProgress/';

export default function LoadingCircleSmall() {
  return (
    <CircularProgress
      style={{ width: '1rem', height: 'auto', margin: 'auto 0.5rem' }}
      sx={{
        ' & .MuiCircularProgress-circle': {
          color: 'var(--pure-white)',
        },
        '& .css-zk81sn-MuiCircularProgress-root': {
          width: '3rem',
        },
      }}
    />
  );
}
