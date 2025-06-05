import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
  components: {
    MuiContainer: {
      styleOverrides: {
        root: {
          paddingTop: '16px',
          paddingBottom: '16px',
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: '#fff',
          color: '#000',
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
        },
      },
    },
    MuiDrawer: {
      styleOverrides: {
        paper: {
          backgroundColor: '#fff',
          color: '#000',
        },
      },
    },
    MuiBottomNavigation: {
      styleOverrides: {
        root: {
          backgroundColor: '#fff',
          color: '#000',
          boxShadow: '0 -2px 4px rgba(0,0,0,0.1)',
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: '8px',
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
          transition: 'box-shadow 0.3s ease-in-out',
          '&:hover': {
            boxShadow: '0 4px 8px rgba(0,0,0,0.2)',
          },
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: '8px',
          textTransform: 'none',
        },
      },
    },
    MuiTypography: {
      styleOverrides: {
        h4: {
          fontWeight: 600,
          marginBottom: '16px',
        },
        h6: {
          fontWeight: 600,
        },
      },
    },
  },
  typography: {
    fontFamily: [
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Roboto',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif',
    ].join(','),
  },
  breakpoints: {
    values: {
      xs: 0,
      sm: 600,
      md: 960,
      lg: 1280,
      xl: 1920,
    },
  },
});

export default theme; 