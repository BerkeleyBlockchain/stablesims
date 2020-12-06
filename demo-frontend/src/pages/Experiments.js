import { Box, Text, Button, Heading, VStack } from '@chakra-ui/react';
import React from 'react';
import { Link } from 'react-router-dom';

export default function Experiments() {
  return (
    <Box textAlign="center" pt="12rem">
      <Heading
        maxW="680px"
        mx="auto"
        fontSize="4rem"
        fontFamily="heading"
        letterSpacing="tight"
        fontWeight="bold"
        mb="6"
        lineHeight="1.2"
      >
        Welcome to StableSims
        <Box as="span" color="teal.500" fontSize="3rem">
          {' '}
          Choose a simulation
        </Box>
      </Heading>

      <Text maxW="560px" mx="auto" opacity={0.7} fontSize="xl" mt="6">
        Brought to you by CK Labs
      </Text>
      <VStack spacing="3" mt="6">
        <Link to="/graphs/blackthursday">
          <Button>Black Thursday</Button>
        </Link>
        <Link to="/graphs/keepers">
          <Button>B@bies Keeper Competition</Button>
        </Link>
      </VStack>
    </Box>
  );
}
