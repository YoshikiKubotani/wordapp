import React from "react";
import { Box, Flex, Heading, Button} from '@chakra-ui/react'
import { useNavigate } from "react-router-dom";

export const StartPage = () => {
  const navigate = useNavigate();

  return (
    <Flex minH="100vh" direction="column" align='center' justify='center' gap='30px'>
      <Heading as='h1' size='xl'>英単語アプリ</Heading>
      <Box>
        <Flex minW="100%" direction='row' align='center' gap='10px'>
          <Button size='lg' colorScheme='green' onClick={() => navigate("/mode")}>問題を解く</Button>
          <Button size='lg' colorScheme='green'>成績を見る</Button>
        </Flex>
      </Box>
    </Flex>
  );
};