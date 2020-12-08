import { Box, Flex, Heading, Link, Button, Spacer } from '@chakra-ui/react';
import React from 'react';
import { Link as RouterLink } from 'react-router-dom';

export default function NavBar() {
  return (
    <Flex>
      <Box p="2">
        <Link as={RouterLink} to="/">
          <Heading size="md">StableSims</Heading>
        </Link>
      </Box>
      <Spacer />
      <Link href="https://github.com/akirillo/bab-stablesims" isExternal>
        <Button>View on Github</Button>
      </Link>
    </Flex>
  );
}
