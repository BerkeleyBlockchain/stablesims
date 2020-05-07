import React from "react";
import TextField from "@material-ui/core/TextField";
import Grid from "@material-ui/core/Grid";

const divStyle = {
  display: "flex",
  flexDirection: "column",
};

export default function Parameters(props) {
  const textHandler = (paramKey) => (event) => {
    props.setParam(paramKey, parseFloat(event.target.value))
  }
  return (
    <div>
      <Grid container direction="row" justify="center" alignItems="center">
        <div style={divStyle}>
          <TextField label="Trades per Day" onChange={textHandler("TRADES_PER_DAY")} defaultValue={15000} style={{ marginBottom: "1rem", marginRight: "1rem" }} type="number" variant="outlined"/>
          <TextField label="Warmup Length" onChange={textHandler("NUM_ORDERS_INIT")} defaultValue={3000} style={{ marginBottom: "1rem", marginRight: "1rem" }} type="number" variant="outlined"/>
          <TextField label="Trade Length" onChange={textHandler("NUM_ORDERS_LIVE")} defaultValue={600000} style={{ marginBottom: "1rem", marginRight: "1rem" }} type="number" variant="outlined"/>
          <TextField label="Tracking Freq" onChange={textHandler("TRACK_FREQ")} defaultValue={1000} style={{ marginBottom: "1rem", marginRight: "1rem" }} type="number" variant="outlined"/>
          <TextField label="Market Speed" onChange={textHandler("MARKET_SPEED")} defaultValue={0.2} style={{ marginBottom: "1rem", marginRight: "1rem" }} type="number" variant="outlined"/>
          <TextField label="Base Spread" onChange={textHandler("BASE_SPREAD")} defaultValue={0.001} style={{ marginBottom: "1rem", marginRight: "1rem" }} type="number" variant="outlined"/>
        </div>
        <div style={divStyle}>
          <TextField label="Price Noise" onChange={textHandler("PRICE_NOISE")} defaultValue={0.0001} style={{ marginBottom: "1rem" }} type="number" variant="outlined"/>
          <TextField label="Basic Trader Threshold" onChange={textHandler("BASIC_TRADER_THRESHOLD")} style={{ marginBottom: "1rem" }} defaultValue={0.02} type="number" variant="outlined"/>
          <TextField label="Level Effect" onChange={textHandler("PRICE_SCALE")} defaultValue={0.0001} style={{ marginBottom: "1rem" }} type="number" variant="outlined"/>
          <TextField label="Variance Effect" onChange={textHandler("VAR_SCALE")} defaultValue={0.00001} style={{ marginBottom: "1rem" }} type="number" variant="outlined"/>
          <TextField label="Bond Expiry" onChange={textHandler("BOND_EXPIRY")} defaultValue={60 * (30 * 24 * 60 * 60)} style={{ marginBottom: "1rem" }} type="number" variant="outlined"/>
          <TextField label="Bond Delay" onChange={textHandler("BOND_DELAY")} defaultValue={15000} style={{ marginBottom: "1rem" }} type="number" variant="outlined"/>
          {/* <TextField label="Bond Range" onChange={textHandler("BOND_RANGE")} defaultValue={0.001} type="number" variant="outlined"/> */}
        </div>
      </Grid>
    </div>
  );
}
