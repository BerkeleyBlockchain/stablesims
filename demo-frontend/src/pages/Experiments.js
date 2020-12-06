import { Button } from '@chakra-ui/react';
import React from 'react';
import { Link } from 'react-router-dom';

export default function Experiments() {
  return (
    <>
      <Link to="/graphs/blackthursday">
        <Button>Black Thursday</Button>
      </Link>
      <Link to="/graphs/keepers">
        <Button>B@bies Keeper Competition</Button>
      </Link>
    </>
  );
}
