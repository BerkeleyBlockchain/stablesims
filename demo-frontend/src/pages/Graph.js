import { Box, Container, Heading } from '@chakra-ui/react';
import React from 'react';
import { useParams } from 'react-router-dom';
import { VictoryBar, VictoryChart } from 'victory';
import { Slider, SliderTrack, SliderFilledTrack, SliderThumb } from '@chakra-ui/react';

const data = [
  { quarter: 1, earnings: 13000 },
  { quarter: 2, earnings: 16500 },
  { quarter: 3, earnings: 14250 },
  { quarter: 4, earnings: 19000 },
];

export default function Experiments() {
  const { type } = useParams();
  return (
    <Container maxW="xl" centerContent>
      <Heading>{type} Graph</Heading>
      <Box bg="white" mb={6}>
        <VictoryChart domainPadding={20}>
          <VictoryBar
            data={data}
            // data accessor for x values
            x="quarter"
            // data accessor for y values
            y="earnings"
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
