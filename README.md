# StableSims

StableSims is an open-source research project aimed at optimizing [MakerDAO](https://makerdao.com/en/) Liquidations 2.0 incentive parameters (`chip` and `tip`).

This project is conducted through [Blockchain @ Berkeley](http://blockchain.berkeley.edu/), and TAKES NO CREDIT FOR THE MAKER PROTOCOL LOGIC THAT WAS COPIED VERBATIM FROM THE [SOURCE CODE](https://github.com/makerdao/dss).

You can find the summary of our findings in our [research paper](https://arxiv.org/abs/2201.03519).

## Getting started
1. Make sure you have Docker installed.
2. Clone the repo
3. Create a docker container to run the simulations in:
  ```bash
  docker run -it -v PATH_TO_REPO:/stablesims python:3.9 bash
  ```
4. Inside the docker shell, run:
  ```bash
  cd stablesims
  pip install -r requirements.txt
  ```
5. To run the simulation, run:
  ```bash
  python run.py
  ```
