import {
  Box,
  Container,
  Heading,
  Slider,
  SliderTrack,
  SliderFilledTrack,
  SliderThumb,
  Button,
} from '@chakra-ui/react';
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { VictoryChart, VictoryAxis, VictoryLine, VictoryTheme } from 'victory';
import io from 'socket.io-client';

const socket = io('http://localhost:5000');

export default function Experiments() {
  const { type } = useParams();
  const [data, setData] = useState([]);

  useEffect(() => {
    socket.on('stream', (stats) => {
      setData((d) => [...d, stats]);
    });
  }, []);

  return (
    <Container maxW="xl" centerContent>
      <Heading>{type} Graph</Heading>
      <Button onClick={() => socket.emit('run')}>Run</Button>
      <Box bg="white" mb={6}>
        <VictoryChart theme={VictoryTheme.material} domainPadding={20} width={500} height={500}>
          <VictoryAxis
            domain={{ x: [0, 144], y: [0, 10] }}
          />
          <VictoryAxis
            dependentAxis
          />
          <VictoryLine
            style={{
              data: { stroke: 'red' },
            }}
            data={data.map((t) => t.eth_price)}
          />
          <VictoryLine
            style={{
              data: { stroke: 'green' },
            }}
            data={data.map((t) => t.num_bids)}
          />
          <VictoryLine
            style={{
              data: { stroke: 'blue' },
            }}
            data={data.map((t) => t.num_bites)}
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
