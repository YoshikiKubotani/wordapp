import React from "react";
import { Box, Flex, Heading, Button} from '@chakra-ui/react'
import { useNavigate } from "react-router-dom";

export const ModeSelection = ({}) => {
  const navigate = useNavigate();

  return (
    <Flex minH="100vh" direction="column" align='center' justify='center' gap='30px'>
      <Heading as='h1' size='xl'>英単語アプリ</Heading>
      <Box>
        <Flex minW="100%" direction='row' align='center' gap='10px'>
          <Button size='lg' colorScheme='green'onClick={() => navigate("/grade")}>学年</Button>
          <Button size='lg' colorScheme='green'>ジャンル</Button>
        </Flex>
      </Box>
    </Flex>
  );
};