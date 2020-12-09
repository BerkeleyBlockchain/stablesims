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
  NumberInput,
  NumberInputField,
  Text,
} from '@chakra-ui/react';
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { VictoryChart, VictoryAxis, VictoryLine, VictoryHistogram } from 'victory';
import io from 'socket.io-client';

const socket = io('http://localhost:5000');

export default function Graphs() {
  const { type } = useParams();
  const [data, setData] = useState([]);
  const [slice, setSlice] = useState([]);
  const [sliderPos, setSliderPos] = useState(0);
  const [histStart, setHistStart] = useState(1);
  const [histEnd, setHistEnd] = useState(500);

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

  const makeChartProps = (y) => ({
    theme: { chart: { padding: { left: 30, right: 0, top: 30, bottom: 0 } } },
    domain: { x: [0, 144], y },
    domainPadding: 20,
    width: 700,
    height: 225,
    style: { parent: { background: '#1a202c', marginBottom: 10 } },
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
      title: 'ETH Price ($)',
      makeLinePropsArgs: [slice.map((t) => t.eth_price)],
    },
    {
      makeChartPropsArgs: [[0, 120]],
      title: 'Number of Liquidations',
      makeLinePropsArgs: [slice.map((t) => t.num_bites)],
    },
    {
      makeChartPropsArgs: [[0, 180]],
      title: 'Number of Bids',
      makeLinePropsArgs: [slice.map((t) => t.num_bids)],
    },
  ];

  const lineCharts = chartArgs.map((argsObj) => (
    <>
      <Heading size="md">{argsObj.title}</Heading>
      <VictoryChart key={argsObj.id} {...makeChartProps(...argsObj.makeChartPropsArgs)}>
        <VictoryAxis {...xAxisProps} />
        <VictoryAxis {...yAxisProps} />
        <VictoryLine {...makeLineProps(...argsObj.makeLinePropsArgs)} />
      </VictoryChart>
    </>
  ));

  const makeHistogramProps = () => ({
    style: { data: { fill: '#319795' } },
    data: data[sliderPos - 1]
      ? Object.values(data[sliderPos - 1].balances)
          .filter((x) => !['cat', 'flipper_eth'].includes(x))
          .map((x) => ({ x }))
      : [],
    bins: [...Array(21).keys()].map((i) => histStart + i * ((histEnd - histStart) / 20)),
    binSpacing: 5,
  });

  const histogram = (
    <>
      <Heading size="md">Keeper Balance Distribution (ETH)</Heading>
      <Flex mt={4}>
        <NumberInput width={32} value={histStart} onChange={(_, value) => setHistStart(value)}>
          <NumberInputField />
        </NumberInput>
        <Text mx={4}> - </Text>
        <NumberInput width={32} value={histEnd} onChange={(_, value) => setHistEnd(value)}>
          <NumberInputField />
        </NumberInput>
      </Flex>
      <VictoryChart
        {...makeChartProps()}
        domain={undefined}
        theme={{ chart: { padding: { left: 30, right: 0, top: 30, bottom: 30 } } }}
      >
        <VictoryAxis {...yAxisProps} dependentAxis={undefined} />
        <VictoryHistogram {...makeHistogramProps()} />
      </VictoryChart>
    </>
  );

  return (
    <HStack spacing={12}>
      <Box mt={6} ml={12} alignSelf="start">
        <Flex mb={24} align="center">
          <Image src="/maker.png" alt="maker" boxSize="100px" mr={6} />
          <Box maxW="18rem">
            <Heading>{titleMap[type]}</Heading>
          </Box>
        </Flex>
        <Button
          background="teal.400"
          width={100}
          rightIcon={<ArrowForwardIcon />}
          onClick={() => socket.emit('run')}
        >
          Run
        </Button>
        <Slider
          mt={12}
          onChange={(val) => setSliderPos(val)}
          value={sliderPos}
          max={143}
          mb="12rem"
        >
          <SliderTrack>
            <SliderFilledTrack />
          </SliderTrack>
          <SliderThumb />
        </Slider>
      </Box>
      <Box p={6} pb={16} maxH="90vh" overflowY="scroll" overflowX="hidden">
        {lineCharts}
        {histogram}
      </Box>
    </HStack>
  );
}
