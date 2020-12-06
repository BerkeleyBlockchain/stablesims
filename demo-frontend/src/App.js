import { ChakraProvider, extendTheme } from '@chakra-ui/react';
import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Experiments from './pages/Experiments';
import Graph from './pages/Graph';

function App() {
  const config = {
    useSystemColorMode: false,
    initialColorMode: 'dark',
  };

  const customTheme = extendTheme({ config });
  return (
    <ChakraProvider resetCSS theme={customTheme}>
      <Router>
        <Switch>
          <Route path="/graphs/:type">
            <Graph />
          </Route>
          <Route path="/">
            <Experiments />
          </Route>
        </Switch>
      </Router>
    </ChakraProvider>
  );
}

export default App;
