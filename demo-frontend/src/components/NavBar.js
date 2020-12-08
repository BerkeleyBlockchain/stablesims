import { Box, Flex, Heading } from '@chakra-ui/react';
import React from 'react';

export default function NavBar() {
  return (
    <Flex>
      <Box p="2">
        <Heading size="md">StableSims</Heading>
      </Box>
    </Flex>
  );
}
