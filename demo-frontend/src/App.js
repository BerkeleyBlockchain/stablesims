import React from "react";
import "./App.css";
import Graph from "./components/Graph";
import Parameters from "./components/Parameters";
import Button from "@material-ui/core/Button";
import io from "socket.io-client";
import LandingPage from "./components/LandingPage";
import {
  createMuiTheme,
  makeStyles,
  ThemeProvider,
} from "@material-ui/core/styles";

const theme = createMuiTheme({
  palette: {
    type: "dark",
  },
});

const endpoint = "http://localhost:5000";

const socket = io.connect(`${endpoint}`);

export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      dataReceived: false,
      warmupData: [],
      marketData: [],
      trackerData: {},
      landing: true,
    };
    this.getWarmupData = this.getWarmupData.bind(this);
    this.getMarketData = this.getMarketData.bind(this);
    this.getTrackerData = this.getTrackerData.bind(this);
  }

  componentDidMount = () => {
    this.getWarmupData();
    this.getMarketData();
    this.getTrackerData();
  };

  getWarmupData = () => {
    socket.on("warmup", (warmupDataObj) => {
      const warmupData = Array.from(warmupDataObj);
      this.setState({ warmupData: [...this.state.warmupData, ...warmupData] });
    });
  };

  getMarketData = () => {
    socket.on("data", (marketDataObj) => {
      const marketData = Array.from(marketDataObj);
      this.setState({ marketData: [...this.state.marketData, ...marketData] });
    });
  };

  getTrackerData = () => {
    socket.on("trackers", (trackerData) => {
      this.setState({ trackerData });
    });
  };

  onClick = () => {
    socket.emit("run", {});
    this.setState({ marketData: [] });
  };

  getData() {
    console.log("GET DATA");
    const data = [
      { x: 1, y: 1.0 },
      { x: 2, y: 1.09 },
      { x: 3, y: 0.99 },
      { x: 4, y: 0.9 },
      { x: 5, y: 0.91 },
    ];
    this.setState({ dataReceived: true, data: data });
  }

  render() {
    const { landing } = this.state;
    return (
      <div>
        <ThemeProvider theme={theme}>
          {landing ? (
            <LandingPage />
          ) : (
            <div className="App">
              <div className="App-header">
                <h1>Basis Simulation</h1>
                <Parameters />
                <Button
                  variant="contained"
                  color="primary"
                  onClick={() => this.onClick()}
                  size="large"
                >
                  Run
                </Button>
                {this.state.dataReceived && <Graph data={this.state.data} />}
              </div>
            </div>
          )}
        </ThemeProvider>
      </div>
    );
  }
}
