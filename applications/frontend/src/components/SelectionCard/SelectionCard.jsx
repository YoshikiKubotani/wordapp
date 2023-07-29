import React from "react";
import {
  Box,
  Flex,
  Heading,
  Button,
  IconButton,
  Card,
  CardBody,
  CardFooter,
  Stack,
  Text,
  Image,
  Divider,
} from '@chakra-ui/react'
import { StarIcon } from '@chakra-ui/icons'

const SelectionCard = ({
  image_source,
  title,
  description,
  trial,
  selection_text,
}) => {
  return (
    <Card maxW='sm'>
    <CardBody>
      <Image
        src={image_source}
        borderRadius='lg'
      />
      <Stack mt='6' spacing='3'>
        <Heading size='md'>{title}</Heading>
        <Text>
          {description}
        </Text>
        <Text color='blue.600' fontSize='2xl'>
          {trial}
        </Text>
      </Stack>
    </CardBody>
    <Divider />
    <CardFooter justify='space-between'>
        <Button variant='solid' color='green.100' bg='green.600'>
          {selection_text}
        </Button>
        <IconButton
          isRound={true}
          variant='solid'
          colorScheme='teal'
          aria-label='Done'
          fontSize='20px'
          icon={<StarIcon />}
        />
    </CardFooter>
  </Card>
  )
}

export default SelectionCard;