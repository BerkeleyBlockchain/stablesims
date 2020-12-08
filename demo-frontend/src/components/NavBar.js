import { Box, Flex, Heading, Link } from '@chakra-ui/react';
import React from 'react';

export default function NavBar() {
  return (
    <Flex>
      <Box p="2">
        <Link href="/">
          <Heading size="md">StableSims</Heading>
        </Link>
      </Box>
    </Flex>
  );
}
