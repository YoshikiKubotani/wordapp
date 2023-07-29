import React from "react";
import { Box, Flex, Heading} from '@chakra-ui/react'
import { useNavigate } from "react-router-dom";

import SelectionCard from '../../components/SelectionCard'

const WordLevel = ({}) => {
  const navigate = useNavigate();

  return (
    <Flex minH="100vh" direction="column" align='center' justify='center' gap='30px'>
      <Heading as='h1' size='md'>学年を選択する</Heading>
      <Box>
        <Flex minW="100%" direction='row' align='center' gap='10px'>
          <SelectionCard
            image_source="nazotoki.jpg"
            title="test"
            description="これはサンプルテキストです。"
            trial="4"
            selection_text="選択"
          />
          <SelectionCard
            image_source="nazotoki.jpg"
            title="test"
            description="これはサンプルテキストです。"
            trial="4"
            selection_text="選択"
          />
          <SelectionCard
            image_source="nazotoki.jpg"
            title="test"
            description="これはサンプルテキストです。"
            trial="4"
            selection_text="選択"
          />
        </Flex>
      </Box>
    </Flex>
  );
};

export default WordLevel;