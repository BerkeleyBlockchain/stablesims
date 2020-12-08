import { ArrowForwardIcon } from '@chakra-ui/icons';
import {
  Box,
  Button,
  Container,
  Flex,
  Heading,
  Image,
  Slider,
  SliderFilledTrack,
  SliderThumb,
  SliderTrack,
  Spacer,
  Tag,
  Text,
  Divider,
} from '@chakra-ui/react';
import React, { useEffect, useState } from 'react';
import io from 'socket.io-client';
// import { useParams } from 'react-router-dom';
import { VictoryAxis, VictoryChart, VictoryLine } from 'victory';
import graphData from '../constants/data';

const socket = io('http://localhost:5000');

export default function Experiments() {
  // const { type } = useParams();
  const [data, setData] = useState([]);
  const [slice, setSlice] = useState(100);

  useEffect(() => {
    // socket.on('stream', (stats) => {
    //   setData((d) => [...d, stats]);
    // });
    const slicedData = graphData.slice(0, slice * Math.floor(graphData.length / 100));
    setData(slicedData);
  }, [slice]);

  return (
    <Container maxW="2xl">
      <Box pt="4rem">
        <Flex align="center">
          <Image src="/maker.png" alt="maker" boxSize="100px" mr={6} />
          <Box maxW="18rem">
            <Heading>Black Thursday Simulation</Heading>
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
      <Box>
        <VictoryChart
          theme={{ chart: { padding: 30 } }}
          domain={{ x: [0, 144], y: [100, 200] }}
          domainPadding={20}
          width={700}
          height={300}
          style={{ parent: { background: '#1a202c' } }}
        >
          <VictoryAxis
            style={{
              axis: { stroke: 'transparent' },
              grid: { stroke: 'transparent' },
              ticks: { stroke: 'transparent' },
              tickLabels: { fill: 'transparent' },
            }}
          />
          <VictoryAxis
            dependentAxis
            style={{
              axis: { stroke: 'transparent' },
              grid: { stroke: '##4A5568' },
              ticks: { stroke: 'transparent' },
              tickLabels: { fill: 'white' },
            }}
          />
          <VictoryLine
            style={{
              data: { stroke: '#319795' },
            }}
            data={data.map((t) => t.eth_price)}
          />
        </VictoryChart>
        <Divider />
        <VictoryChart
          theme={{ chart: { padding: 30 } }}
          domain={{ x: [0, 144], y: [0, 100] }}
          domainPadding={20}
          width={700}
          height={300}
          style={{ parent: { background: '#1a202c' } }}
        >
          <VictoryAxis
            style={{
              axis: { stroke: 'transparent' },
              grid: { stroke: 'transparent' },
              ticks: { stroke: 'transparent' },
              tickLabels: { fill: 'transparent' },
            }}
          />
          <VictoryAxis
            dependentAxis
            style={{
              axis: { stroke: 'transparent' },
              grid: { stroke: '##4A5568' },
              ticks: { stroke: 'transparent' },
              tickLabels: { fill: 'white' },
            }}
          />
          <VictoryLine
            style={{
              data: { stroke: '#319795' },
            }}
            data={data.map((t) => t.num_bites)}
          />
        </VictoryChart>
        <Divider />
        <VictoryChart
          theme={{ chart: { padding: 30 } }}
          domain={{ x: [0, 144], y: [0, 180] }}
          domainPadding={20}
          width={700}
          height={300}
          style={{ parent: { background: '#1a202c' } }}
        >
          <VictoryAxis
            style={{
              axis: { stroke: 'transparent' },
              grid: { stroke: 'transparent' },
              ticks: { stroke: 'transparent' },
              tickLabels: { fill: 'transparent' },
            }}
          />
          <VictoryAxis
            dependentAxis
            style={{
              axis: { stroke: 'transparent' },
              grid: { stroke: '##4A5568' },
              ticks: { stroke: 'transparent' },
              tickLabels: { fill: 'white' },
            }}
          />
          <VictoryLine
            style={{
              data: { stroke: '#319795' },
            }}
            data={data.map((t) => t.num_bids)}
          />
        </VictoryChart>
        <Divider />
      </Box>
      <Text my={3}>Use this slider to adjust the data</Text>
      <Slider onChange={(val) => setSlice(val)} defaultValue={100} mb="12rem">
        <SliderTrack>
          <SliderFilledTrack />
        </SliderTrack>
        <SliderThumb />
      </Slider>
    </Container>
  );
}
