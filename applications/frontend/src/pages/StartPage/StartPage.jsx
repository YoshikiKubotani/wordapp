import React from "react";
import "./StartPage.css";
import { Box, Flex, Heading, Button, Spacer} from '@chakra-ui/react'
import theme from "../../theme";

export const StartPage = ({}) => {
  console.log(theme.config.initialColorMode)
  return (
    // <Box minH="100vh">
      <Flex minH="100vh" direction="column" align='center' gap='30px'>
        <Spacer />
        <Heading as='h1' size='xl'>英単語アプリ</Heading>
        <Box>
          <Flex minW="100%" flexDirection='row' gap='10px'>
            <Spacer />
            <Button size='lg' colorScheme='green'>問題を解く</Button>
            <Button size='lg' colorScheme='green'>成績を見る</Button>
            <Spacer />
          </Flex>
        </Box>
        <Spacer />
      </Flex>
    // </Box>
  );
};