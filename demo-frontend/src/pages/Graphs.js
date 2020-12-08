import { ArrowForwardIcon } from '@chakra-ui/icons';
import {
  Box,
  Button,
  HStack,
  Flex,
  Heading,
  Image,
  Slider,
  SliderFilledTrack,
  SliderThumb,
  SliderTrack,
  Spacer,
  Tag,
} from '@chakra-ui/react';
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { VictoryChart, VictoryAxis, VictoryLine, VictoryLegend } from 'victory';
import io from 'socket.io-client';

const socket = io('http://localhost:5000');

export default function Graphs() {
  const { type } = useParams();
  const [data, setData] = useState([]);
  const [slice, setSlice] = useState([]);
  const [sliderPos, setSliderPos] = useState(0);

  useEffect(() => {
    socket.on('stream', (stats) => {
      setData((d) => [...d, stats]);
      setSliderPos((p) => p + 1);
    });
  }, []);

  useEffect(() => {
    const slicedData = data.slice(0, sliderPos);
    setSlice(slicedData);
  }, [sliderPos]);

  const titleMap = {
    blackthursday: 'Black Thursday Simulation',
    keepers: 'B@by Keeper Competition',
  };
  const renderCharts = () => {
    const makeChartProps = (y) => ({
      theme: { chart: { padding: { left: 30, right: 0, top: 30, bottom: 0 } } },
      domain: { x: [0, 144], y },
      domainPadding: 20,
      width: 700,
      height: 225,
      style: { parent: { background: '#1a202c', marginBottom: 10 } },
    });
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

    const chartArgs = [
      {
        makeChartPropsArgs: [[100, 200]],
        makeLegendPropsArgs: ['ETH Price', 555, 0],
        makeLinePropsArgs: [slice.map((t) => t.eth_price)],
      },
      {
        makeChartPropsArgs: [[0, 120]],
        makeLegendPropsArgs: ['Number of Liquidations', 400, 0],
        makeLinePropsArgs: [slice.map((t) => t.num_bites)],
      },
      {
        makeChartPropsArgs: [[0, 180]],
        makeLegendPropsArgs: ['Number of Bids', 490, 0],
        makeLinePropsArgs: [slice.map((t) => t.num_bids)],
      },
    ];

    return chartArgs.map((argsObj) => (
      <VictoryChart key={argsObj.id} {...makeChartProps(...argsObj.makeChartPropsArgs)}>
        <VictoryLegend {...makeLegendProps(...argsObj.makeLegendPropsArgs)} />
        <VictoryAxis {...xAxisProps} />
        <VictoryAxis {...yAxisProps} />
        <VictoryLine {...makeLineProps(...argsObj.makeLinePropsArgs)} />
      </VictoryChart>
    ));
  };

  return (
    <HStack spacing={24}>
      <Box pt={6} maxW="md" alignSelf="start">
        <Flex align="center" direction="column">
          <Image src="/maker.png" alt="maker" boxSize="100px" mr={6} />
          <Box maxW="18rem">
            <Heading>{titleMap[type]}</Heading>
          </Box>
          <Tag variant="solid" colorScheme="yellow">
            DAI
          </Tag>
          <Spacer />
          <Button rightIcon={<ArrowForwardIcon />} onClick={() => socket.emit('run')}>
            Run
          </Button>
        </Flex>
      </Box>
      <Box pt={6} maxH="100vh">
        {renderCharts()}
        <Slider onChange={(val) => setSliderPos(val)} value={sliderPos} max={144} mb="12rem">
          <SliderTrack>
            <SliderFilledTrack />
          </SliderTrack>
          <SliderThumb />
        </Slider>
      </Box>
    </HStack>
  );
}
