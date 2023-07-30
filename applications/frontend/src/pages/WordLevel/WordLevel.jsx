import React from "react";
import { Box, Flex, Heading, SimpleGrid } from '@chakra-ui/react'
import { useNavigate } from "react-router-dom";

import SelectionCard from '../../components/SelectionCard'

export const WordLevel = ({}) => {
  const navigate = useNavigate();

  return (
    <Flex minH="100vh" direction="column" align='center' justify='center' gap='30px'>
      <Heading as='h1' size='md'>どの学年の単語を勉強する？</Heading>
      <Box marginX="30px">
        <SimpleGrid minChildWidth='xs' spacing='10px'>
          <SelectionCard
            imageSource="nazotoki.jpg"
            title="中学３年生"
            description="これはサンプルテキストです。"
            trial="4"
            selectionText="選択"
            navigateTo="/grade/3"
          />
          <SelectionCard
            imageSource="nazotoki.jpg"
            title="高校１年生"
            description="これはサンプルテキストです。"
            trial="4"
            selectionText="選択"
            navigateTo="/grade/4"
          />
          <SelectionCard
            imageSource="nazotoki.jpg"
            title="高校２年生"
            description="これはサンプルテキストです。"
            trial="4"
            selectionText="選択"
            navigateTo="/grade/5"
          />
          <SelectionCard
            imageSource="nazotoki.jpg"
            title="高校３年生"
            description="これはサンプルテキストです。"
            trial="4"
            selectionText="選択"
            navigateTo="/grade/6"
          />
        </SimpleGrid>
      </Box>
    </Flex>
  );
};