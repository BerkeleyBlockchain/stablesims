import {Heading} from '@chakra-ui/react'
import React from 'react'
import {useParams} from 'react-router-dom'

export default function Experiments() {
  const {type} = useParams()
  return (
    <>
      <Heading>{type} Graph</Heading>
    </>
  )
}
