import React from "react";
import "./LandingPage.css";
import { createMuiTheme, makeStyles } from "@material-ui/core/styles";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import Typography from "@material-ui/core/Typography";
import CardActionArea from "@material-ui/core/CardActionArea";
import basis from "./../images/basis.jpg";
import dai from "./../images/dai.jpg";
import bab from "./../images/bablogo.png";
import CardMedia from "@material-ui/core/CardMedia";

const useStyles = makeStyles({
  root: {
    minWidth: 500,
    minHeight: 500,
  },
  text: {
    textAlign: "center",
  },
});

export default function LandingPage(props) {
  console.log(props);
  const classes = useStyles();
  return (
    <div className="main">
      <h1>Choose a simulator</h1>
      <div
        style={{
          width: "100%",
          display: "flex",
          flexDirection: "row",
          justifyContent: "space-around",
        }}
      >
        <Card className={classes.root}>
          <CardActionArea onClick={() => props.onClick()}>
            <CardMedia style={{ height: 500 }} image={basis} />
          </CardActionArea>
        </Card>
        <Card className={classes.root}>
          <CardActionArea onClick={() => console.log("PRESSED")}>
            <CardMedia style={{ height: 500 }} image={dai} />
          </CardActionArea>
        </Card>
      </div>
      <div style={{ width: "100%" }}>
        <img
          src={bab}
          style={{
            height: 100,
            width: 100,
            paddingLeft: 100,
            paddingTop: 20,
            paddingBottom: 0,
          }}
        />
      </div>
    </div>
  );
}
