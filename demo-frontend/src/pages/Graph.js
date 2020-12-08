import {
  Flex,
  Box,
  Container,
  Heading,
  Slider,
  SliderTrack,
  SliderFilledTrack,
  SliderThumb,
  Button,
  Image,
} from '@chakra-ui/react';
import React, { useState, useEffect } from 'react';
// import { useParams } from 'react-router-dom';
import { VictoryChart, VictoryAxis, VictoryLine } from 'victory';
import io from 'socket.io-client';

const socket = io('http://localhost:5000');

export default function Experiments() {
  // const { type } = useParams();
  const [data, setData] = useState([]);

  useEffect(() => {
    socket.on('stream', (stats) => {
      setData((d) => [...d, stats]);
    });
  }, []);

  return (
    <Container maxW="xl">
      <Box pt="4rem">
        <Flex align="center">
          <Image src="/maker.png" alt="maker" boxSize="100px" mr={6} />

          <Heading>Black Thursday Simulation</Heading>
        </Flex>
      </Box>
      <Button onClick={() => socket.emit('run')}>Run</Button>
      <Box bg="white" mb={6}>
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
      </Box>
      <Slider defaultValue={30}>
        <SliderTrack>
          <SliderFilledTrack />
        </SliderTrack>
        <SliderThumb />
      </Slider>
    </Container>
  );
}
