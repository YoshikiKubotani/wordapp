import React from "react";
import {
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
import { useNavigate } from "react-router-dom";

const SelectionCard = ({
  imageSource,
  title,
  description,
  trial,
  selectionText,
  navigateTo,
}) => {
  const navigate = useNavigate();

  return (
    <Card>
      <CardBody>
        <Image
          src={imageSource}
          borderRadius='lg'
        />
        <Stack mt='6' spacing='3'>
          <Heading size='lg' color='teal.50'>{title}</Heading>
          <Text color='teal.50'>
            {description}
          </Text>
          <Text color='blue.300' fontSize='sm'>
            {trial}回 学習済み
          </Text>
        </Stack>
      </CardBody>
      <Divider />
      <CardFooter justify='space-between'>
          <Button
            variant='solid'
            color='teal.50'
            bg='teal.500'
            _hover={{ bg: 'teal.600' }}
            onClick={() => navigate(navigateTo)}
          >
            {selectionText}
          </Button>
          <IconButton
            isRound={true}
            variant='solid'
            color='yellow.400'
            bg='gray.500'
            _hover={{ bg: 'gray.600' }}
            aria-label='Done'
            fontSize='20px'
            icon={<StarIcon />}
          />
      </CardFooter>
    </Card>
  )
}

export default SelectionCard;