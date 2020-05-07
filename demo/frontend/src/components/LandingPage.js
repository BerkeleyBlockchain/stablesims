import React from "react";
import "./LandingPage.css";
import { makeStyles } from "@material-ui/core/styles";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import Typography from "@material-ui/core/Typography";
import CardActionArea from "@material-ui/core/CardActionArea";

const useStyles = makeStyles({
  root: {
    minWidth: 275,
  },
  text: {
    textAlign: "center",
  },
});

export default function LandingPage(props) {
  const classes = useStyles();
  return (
    <div className="main">
      <h1>Choose a simulator</h1>

      <Card className={classes.root}>
        <CardActionArea onClick={() => console.log("PRESSED")}>
          <CardContent>
            <Typography variant="h3" className={classes.text}>
              Basis
            </Typography>
          </CardContent>
        </CardActionArea>
      </Card>
    </div>
  );
}
