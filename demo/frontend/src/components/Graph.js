import React from "react";
import {
  VictoryBar,
  VictoryChart,
  VictoryAxis,
  VictoryTheme,
  VictoryLine,
} from "victory";
import Grid from "@material-ui/core/Grid";

const divStyle = {
  display: "flex",
  flexDirection: "row",
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
  return (
    <div style={divStyle}>
      <VictoryChart
        theme={VictoryTheme.material}
        domainPadding={20}
        width={500}
        height={500}
      >
        <VictoryAxis
          // tickValues specifies both the number of ticks and where
          // they are placed on the axis
          style={{ tickLabels: { fill: "white" } }}
          domain={{ x: [0, 50], y: [0, 10] }}
        />
        <VictoryAxis
          dependentAxis
          // tickFormat specifies how ticks should be displayed
          style={{ tickLabels: { fill: "white" } }}
          tickFormat={(x) => `$${x}`}
        />
        <VictoryLine
          style={{
            data: { stroke: "#c43a31" },
            parent: { border: "1px solid #ccc" },
          }}
          data={props.warmupData}
        />
      </VictoryChart>

      <VictoryChart
        theme={VictoryTheme.material}
        domainPadding={20}
        width={500}
        height={500}
      >
        <VictoryAxis
          // tickValues specifies both the number of ticks and where
          // they are placed on the axis
          style={{ tickLabels: { fill: "white" } }}
          domain={{ x: [0, 100], y: [0, 10] }}
        />
        <VictoryAxis
          dependentAxis
          // tickFormat specifies how ticks should be displayed
          style={{ tickLabels: { fill: "white" } }}
          tickFormat={(x) => `$${x}`}
        />
        <VictoryLine
          style={{
            data: { stroke: "#c43a31" },
            parent: { border: "1px solid #ccc" },
          }}
          data={props.marketData}
        />
      </VictoryChart>
    </div>
  );
}

export default Graph;