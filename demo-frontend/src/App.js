import {ChakraProvider, extendTheme} from '@chakra-ui/react'
import React from 'react'
import Experiments from './pages/Experiments'
import Graph from './pages/Graph'
import {BrowserRouter as Router, Switch, Route, Link} from 'react-router-dom'

function App() {
  const config = {
    useSystemColorMode: false,
    initialColorMode: 'dark',
  }

  const customTheme = extendTheme({config})
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
  )
}

export default App
