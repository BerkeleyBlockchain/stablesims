import {
  Box,
  Heading,
  Slider,
  SliderTrack,
  SliderFilledTrack,
  SliderThumb,
  Button,
  HStack,
} from '@chakra-ui/react';
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { VictoryChart, VictoryAxis, VictoryLine, VictoryLegend } from 'victory';
import io from 'socket.io-client';

const socket = io('http://localhost:5000');

export default function Graphs() {
  const { type } = useParams();
  const [data, setData] = useState([]);

  useEffect(() => {
    socket.on('stream', (stats) => {
      setData((d) => [...d, stats]);
    });
  }, []);

  const titleMap = {
    blackthursday: 'Black Thursday Simulation',
    keepers: 'B@by Keeper Competition',
  };
  const renderCharts = (chartArgs) => {
    const chartProps = {
      theme: { chart: { padding: { left: 30, right: 0, top: 30, bottom: 0 } } },
      domain: { x: [0, 144], y: [100, 200] },
      domainPadding: 20,
      width: 700,
      height: 225,
      style: { parent: { background: '#1a202c', marginBottom: 10 } },
    };
    const makeLegendProps = (title, x, y) => ({
      title,
      x,
      y,
      orientation: 'horizontal',
      style: { title: { fill: 'white', fontSize: 22, fontWeight: 'bold' } },
    });
    const xAxisProps = {
      style: {
        axis: { stroke: 'transparent' },
        grid: { stroke: 'transparent' },
        ticks: { stroke: 'transparent' },
        tickLabels: { fill: 'transparent' },
      },
    };
    const yAxisProps = {
      dependentAxis: true,
      style: {
        axis: { stroke: 'transparent' },
        grid: { stroke: '#4A5568' },
        ticks: { stroke: 'transparent' },
        tickLabels: { fill: 'white', padding: 10 },
      },
    };
    const makeLineProps = (dataArr) => ({
      style: {
        data: { stroke: '#319795', strokeWidth: 2 },
      },
      data: dataArr,
    });

    return chartArgs.map((argsObj) => (
      <VictoryChart {...chartProps}>
        <VictoryLegend {...makeLegendProps(...argsObj.makeLegendPropsArgs)} />
        <VictoryAxis {...xAxisProps} />
        <VictoryAxis {...yAxisProps} />
        <VictoryLine {...makeLineProps(...argsObj.makeLinePropsArgs)} />
      </VictoryChart>
    ));
  };

  return (
    <HStack spacing={24}>
      <Box ml={12} mt={8} maxW="xs" alignSelf="start">
        <Heading>{titleMap[type]}</Heading>
        <Button mt={6} background="teal.500" onClick={() => socket.emit('run')}>
          Run
        </Button>
      </Box>
      <Box pt={8}>
        {renderCharts([
          {
            makeLegendPropsArgs: ['ETH Price', 555, 0],
            makeLinePropsArgs: [data.map((t) => t.eth_price)],
          },
          {
            makeLegendPropsArgs: ['Number of Liquidations', 400, 0],
            makeLinePropsArgs: [data.map((t) => t.num_bites)],
          },
          {
            makeLegendPropsArgs: ['Number of Bids', 490, 0],
            makeLinePropsArgs: [data.map((t) => t.num_bids)],
          },
        ])}
        <Slider defaultValue={30}>
          <SliderTrack>
            <SliderFilledTrack />
          </SliderTrack>
          <SliderThumb />
        </Slider>
      </Box>
    </HStack>
  );
}
