import React from "react";
import {
  VictoryChart,
  VictoryAxis,
  VictoryTheme,
  VictoryArea,
} from "victory";
import _ from "lodash";

const divStyle = {
  display: "flex",
  flexDirection: "column",
};

function Graph(props) {
  return (
    <div style={divStyle}>
      <svg style={{ position: "absolute" }}>
        <defs>
          <linearGradient id="graphGradient" 
            x1="0%" y1="0%" x2="0%" y2="100%"
          >
            <stop offset="0%"   stopColor="rgba(254, 203, 51, 0.5)"/>
            <stop offset="100%" stopColor="rgba(254, 203, 51, 0)"/>
          </linearGradient>
        </defs>
      </svg>

      <VictoryChart
        theme={VictoryTheme.material}
        domainPadding={20}
        width={800}
        height={325}
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
            data: { fill: "url(#graphGradient)", stroke: "rgba(254, 203, 51, 1)", strokeWidth: 3 },
          }}
          data={props.warmupData}
        />
      </VictoryChart>

      <VictoryChart
        theme={VictoryTheme.material}
        domainPadding={20}
        width={800}
        height={425}
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
            data: { fill: "url(#graphGradient)", stroke: "rgba(254, 203, 51, 1)", strokeWidth: 3 },
          }}
          data={props.marketData}
        />
      </VictoryChart>
    </div>
  );
}

export default Graph;