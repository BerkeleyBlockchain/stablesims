import { ChakraProvider, extendTheme, Box } from '@chakra-ui/react';
import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Experiments from './pages/Experiments';
import Graphs from './pages/Graphs';
import NavBar from './components/NavBar';

function App() {
  const config = {
    useSystemColorMode: false,
    initialColorMode: 'dark',
  };

  const customTheme = extendTheme({ config });
  return (
    <ChakraProvider resetCSS theme={customTheme}>
      <Box maxH="100vh" overflow="hidden">
        <Router>
          <NavBar />
          <Switch>
            <Route path="/graphs/:type">
              <Graphs />
            </Route>
            <Route path="/">
              <Experiments />
            </Route>
          </Switch>
        </Router>
      </Box>
    </ChakraProvider>
  );
}

export default App;
