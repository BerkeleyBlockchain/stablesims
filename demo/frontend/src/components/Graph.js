import React from "react";
import {
  VictoryChart,
  VictoryAxis,
  VictoryTheme,
  VictoryArea,
  VictoryLine
} from "victory";
import _ from "lodash";

const divStyle = {
  display: "flex",
  flexDirection: "column",
};

function getTicks(data) {
  const ticks = [];
  for (let i = 1; i <= data.length; i++) {
    ticks.push(i);
  }
  console.log(ticks);
  return ticks;
}

function Graph(props) {
  console.log(props.warmupData);
  return (
    <div style={divStyle}>
      <svg style={{ position: "absolute" }}>
        <defs>
          <linearGradient id="graphGradient" 
            x1="0%" y1="0%" x2="0%" y2="100%"
          >
            <stop offset="0%"   stopColor="rgba(62, 81, 181, 0.5)"/>
            <stop offset="50%" stopColor="rgba(62, 81, 181, 0)"/>
          </linearGradient>
        </defs>
      </svg>

      <VictoryChart
        theme={VictoryTheme.material}
        domainPadding={20}
        width={800}
        height={300}
      >
        <VictoryAxis
          style={{ tickLabels: { fill: "white" }, grid: { stroke: "rgba(0, 0, 0, 0)" } }}
          />
        <VictoryAxis
          dependentAxis
          style={{ tickLabels: { fill: "white" }, grid: { stroke: "rgba(0, 0, 0, 0)" } }}
          tickFormat={(y) => `$${y}`}
        />
        <VictoryArea
          domain={ props.warmupData.length <= 0 ? { x : [0, props.warmupXDomain] } :
            { x : [0, props.warmupXDomain],
              y: [_.minBy(props.warmupData, d => d.y).y, _.maxBy(props.warmupData, d => d.y).y] }}
          style={{
            data: { fill: "url(#graphGradient)", stroke: "rgba(62, 81, 181, 1)", strokeWidth: 3 },
          }}
          data={props.warmupData}
        />
      </VictoryChart>

      <VictoryChart
        theme={VictoryTheme.material}
        domainPadding={20}
        width={800}
        height={450}
      >
        <VictoryAxis
          style={{ tickLabels: { fill: "white" }, grid: { stroke: "rgba(0, 0, 0, 0)" } }}
          />
        <VictoryAxis
          dependentAxis
          style={{ tickLabels: { fill: "white" }, grid: { stroke: "rgba(0, 0, 0, 0)" } }}
          tickFormat={(y) => `$${y}`}
        />
        <VictoryArea
          domain={ props.marketData.length <= 0 ? { x : [0, props.marketXDomain] } :
            { x: [0, props.marketXDomain],
              y: [_.minBy(props.marketData, d => d.y).y, _.maxBy(props.marketData, d => d.y).y] }}
          style={{
            data: { fill: "url(#graphGradient)", stroke: "rgba(62, 81, 181, 1)", strokeWidth: 3 },
          }}
          data={props.marketData}
        />
      </VictoryChart>
    </div>
  );
}

export default Graph;