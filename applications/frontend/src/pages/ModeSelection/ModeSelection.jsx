import React from "react";
import { Box, Flex, Heading, Button, Spacer} from '@chakra-ui/react'

const ModeSelection = ({}) => {
  return (
    <Flex minH="100vh" direction="column" align='center' gap='30px'>
      <Spacer />
      <Heading as='h1' size='xl'>英単語アプリ</Heading>
      <Box>
        <Flex minW="100%" flexDirection='row' gap='10px'>
          <Spacer />
          <Button size='lg' colorScheme='green'>学年</Button>
          <Button size='lg' colorScheme='green'>ジャンル</Button>
          <Spacer />
        </Flex>
      </Box>
      <Spacer />
    </Flex>
  );
};

export default ModeSelection;