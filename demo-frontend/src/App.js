import { ChakraProvider, extendTheme } from '@chakra-ui/react';
import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Experiments from './pages/Experiments';
import BTGraph from './pages/BTGraph';
import NavBar from './components/NavBar';

function App() {
  const config = {
    useSystemColorMode: false,
    initialColorMode: 'dark',
  };

  const customTheme = extendTheme({ config });
  return (
    <ChakraProvider resetCSS theme={customTheme}>
      <Router>
        <NavBar />
        <Switch>
          <Route path="/graphs/blackthursday">
            <BTGraph />
          </Route>
          <Route path="/graphs/:type">
            <h1>Graph</h1>
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
