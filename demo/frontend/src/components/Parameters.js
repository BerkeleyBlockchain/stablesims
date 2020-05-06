import React from "react";
import TextField from "@material-ui/core/TextField";
import { createMuiTheme, makeStyles } from "@material-ui/core/styles";
import Grid from "@material-ui/core/Grid";

const useStyles = makeStyles((theme) => ({
  root: {
    "& > *": {
      margin: theme.spacing(1),
      width: "10ch",
    },
  },
  input: {
    color: "white",
  },
}));


export default function Parameters(props) {
  const textHandler = (paramKey) => (event) => {
    props.setParam(paramKey, parseFloat(event.target.value))
  }
  return (
    <div>
      <Grid container direction="column" justify="center" alignItems="center">
          <TextField label="Trades per Day" onChange={textHandler("TRADES_PER_DAY")} defaultValue={15000} type="number" variant="outlined"/>
          <TextField label="Warmup Length" onChange={textHandler("NUM_ORDERS_INIT")} defaultValue={3000} type="number" variant="outlined"/>
          <TextField label="Trade Length" onChange={textHandler("NUM_ORDERS_LIVE")} defaultValue={600000} type="number" variant="outlined"/>
          <TextField label="Tracking Freq" onChange={textHandler("TRACK_FREQ")} defaultValue={1000} type="number" variant="outlined"/>
          <TextField label="Market Speed" onChange={textHandler("MARKET_SPEED")} defaultValue={0.2} type="number" variant="outlined"/>
          <TextField label="Base Spread" onChange={textHandler("BASE_SPREAD")} defaultValue={0.001} type="number" variant="outlined"/>
          <TextField label="Price Noise" onChange={textHandler("PRICE_NOISE")} defaultValue={0.0001} type="number" variant="outlined"/>
          <TextField label="Basic Trader Threshold" onChange={textHandler("BASIC_TRADER_THRESHOLD")} defaultValue={0.02} type="number" variant="outlined"/>
          <TextField label="Level Effect" onChange={textHandler("PRICE_SCALE")} defaultValue={0.0001} type="number" variant="outlined"/>
          <TextField label="Variance Effect" onChange={textHandler("VAR_SCALE")} defaultValue={0.00001} type="number" variant="outlined"/>
          <TextField label="Bond Expiry" onChange={textHandler("BOND_EXPIRY")} defaultValue={60 * (30 * 24 * 60 * 60)} type="number" variant="outlined"/>
          <TextField label="Bond Delay" onChange={textHandler("BOND_DELAY")} defaultValue={15000} type="number" variant="outlined"/>
          {/* <TextField label="Bond Range" onChange={textHandler("BOND_RANGE")} defaultValue={0.001} type="number" variant="outlined"/> */}
      </Grid>
    </div>
  );
}
