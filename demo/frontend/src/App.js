import React from 'react';
import io from 'socket.io-client';
import './App.css';

const endpoint = "http://localhost:5000";

const socket = io.connect(`${endpoint}`);

export default class App extends React.Component {
  constructor(props) {
    super(props);
    
    this.state = {
      warmupData: [],
      marketData: [],
      trackerData: {},
    }

    this.getWarmupData = this.getWarmupData.bind(this);
    this.getMarketData = this.getMarketData.bind(this);
    this.getTrackerData = this.getTrackerData.bind(this);
  }

  componentDidMount = () => {
    this.getWarmupData();
    this.getMarketData();
    this.getTrackerData();
  }
  
  getWarmupData = () => {
    socket.on("warmup", warmupDataObj => {
      const warmupData = Array.from(warmupDataObj);
      this.setState({ warmupData: [...this.state.warmupData, ...warmupData] });
    })
  }
  
  getMarketData = () => {
    socket.on("data", marketDataObj => {
      const marketData = Array.from(marketDataObj);
      this.setState({ marketData: [...this.state.marketData, ...marketData] });
    })
  }

  getTrackerData = () => {
    socket.on("trackers", trackerData => {
      this.setState({ trackerData });
    })
  }
  
  onClick = () => {
    socket.emit("run", {});
    this.setState({ marketData: [] });
  };
  
  render = () => {
    const { marketData } = this.state;
    const { warmupData } = this.state;

    return(
      <div>
        <button onClick={() => this.onClick()}>Run Simulation</button>
        <h1>Warmup Data:</h1>
        <div className="data warmup">
          {warmupData.toString()}
        </div>
        <h1>Full Data:</h1>
        <div className="data market">
          {marketData.toString()}
        </div>
      </div>
    )
  }
}
