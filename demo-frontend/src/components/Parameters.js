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
  const classes = useStyles();
  return (
    <div>
      <Grid container direction="column" justify="center" alignItems="center">
        <form className={classes.root} noValidate autoComplete="off">
          <TextField id="standard-basic" label="Steps" />
          <TextField id="filled-basic" label="Steps Per Day" variant="filled" />
          <TextField
            id="outlined-basic"
            label="Bond Delay"
            variant="outlined"
          />
        </form>
        <form className={classes.root} noValidate autoComplete="off">
          <TextField id="standard-basic" label="Bond Delay" />
          <TextField id="filled-basic" label="Bond Range" variant="filled" />
          <TextField
            id="outlined-basic"
            label="Base Spread"
            variant="outlined"
          />
        </form>
        <form className={classes.root} noValidate autoComplete="off">
          <TextField id="standard-basic" label="Steps" />
          <TextField id="filled-basic" label="Price Spread" variant="filled" />
          <TextField
            id="outlined-basic"
            label="Price Noise"
            variant="outlined"
          />
        </form>
        <form className={classes.root} noValidate autoComplete="off">
          <TextField id="standard-basic" label="Market Speed" />
          <TextField id="filled-basic" label="Level Effect" variant="filled" />
          <TextField
            id="outlined-basic"
            label="Variance Effect"
            variant="outlined"
          />
        </form>
      </Grid>
    </div>
  );
}
