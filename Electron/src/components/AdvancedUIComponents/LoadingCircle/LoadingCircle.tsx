import CircularProgress from '@mui/material/CircularProgress';

export default function LoadingCircle() {
  return (
    <div
      className="container-fluid d-flex justify-content-center align-content-center"
      style={{
        height: '100%',
        justifyContent: 'center',
        alignItems: 'center',
        padding: '5%',
      }}
    >
      <CircularProgress
        style={{ width: '2rem', height: 'auto' }}
        sx={{
          ' & .MuiCircularProgress-circle': {
            color: 'var(--pure-white)',
          },
          '& .css-zk81sn-MuiCircularProgress-root': {
            width: '3rem',
          },
        }}
      />
    </div>
  );
}
