import React from "react";
import "./App.css";
import Graph from "./components/Graph";
import Parameters from "./components/Parameters";
import Button from "@material-ui/core/Button";
import io from "socket.io-client";
import LandingPage from "./components/LandingPage";
import {
  createMuiTheme,
  ThemeProvider,
} from "@material-ui/core/styles";
import logo from "./logo_horizontal.png";

const theme = createMuiTheme({
  palette: {
    type: "dark",
    primary: { main: "#fecb33" }
  },
});

const endpoint = "http://localhost:5000";

const socket = io.connect(`${endpoint}`);

export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      warmupData: [],
      marketData: [],
      trackerData: {},
      params: {
        TRADES_PER_DAY: 15000,
        NUM_ORDERS_INIT: 3000,
        NUM_ORDERS_LIVE: 600000,
        TRACK_FREQ: 1000,
        MARKET_SPEED: 0.2,
        BASE_SPREAD: 0.001,
        PRICE_NOISE: 0.0001,
        BASIC_TRADER_THRESHOLD: 0.02,
        PRICE_SCALE: 0.0001,
        VAR_SCALE: 0.00001,
        BOND_EXPIRY: 60 * (30 * 24 * 60 * 60),
        BOND_DELAY: 15000,
      },
      landing: false,
    };
    this.getWarmupData = this.getWarmupData.bind(this);
    this.getMarketData = this.getMarketData.bind(this);
    this.getTrackerData = this.getTrackerData.bind(this);
    this.setParam = this.setParam.bind(this);
    this.run = this.run.bind(this);
    this.formatData = this.formatData.bind(this);
  }

  componentDidMount = () => {
    this.getWarmupData();
    this.getMarketData();
    this.getTrackerData();
  };

  getWarmupData = () => {
    socket.on("warmup", (warmupDataObj) => {
      this.setState({ warmupData: [...this.state.warmupData, warmupDataObj] });
    });
  };
  
  getMarketData = () => {
    socket.on("data", (marketDataObj) => {
      this.setState({ marketData: [...this.state.marketData, marketDataObj] });
    });
  };

  getTrackerData = () => {
    socket.on("trackers", (trackerData) => {
      this.setState({ trackerData });
    });
  };

  run = () => {
    socket.emit("run", this.state.params);
    this.setState({ marketData: [] });
    this.setState({ warmupData: [] });
  }

  formatData = (priceData) => {
    let data = [];
    priceData.forEach((y, index) => data.push({ x: index, y: y }));
    return data;
  }

  setParam = (paramKey, paramVal) => {
    const params = this.state.params;
    params[paramKey] = paramVal;
    this.setState({ params });
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
              <div className="dashboard">
                <div className="controls">
                  <h1 style={{margin:"3rem 0 3rem"}}>Basis Simulator</h1>
                  <Parameters setParam={this.setParam} />
                  <Button style={{ width: "100%" }} variant="contained" color="primary" onClick={this.run} size="large">Run</Button>
                  <img src={logo} style={{width:"10rem", position:"relative", top: "5rem"}}/>
                </div>
                <Graph marketXDomain={this.state.params.NUM_ORDERS_LIVE/this.state.params.TRACK_FREQ} warmupXDomain={this.state.params.NUM_ORDERS_INIT * 100 / this.state.params.TRACK_FREQ} warmupData={this.formatData(this.state.warmupData)} marketData={this.formatData(this.state.marketData)} />
              </div>
            </div>
          )}
        </ThemeProvider>
      </div>
    );
  }
}
