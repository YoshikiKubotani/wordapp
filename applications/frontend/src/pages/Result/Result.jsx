import React from "react";
import { useLoaderData } from "react-router-dom";
import {
  Box,
  Flex,
  Heading,
  Stack,
  StackDivider,
  Text,
  Icon,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  StatArrow,
  StatGroup,
  Card,
  CardHeader,
  CardBody
} from '@chakra-ui/react';
import { GiSandsOfTime } from "react-icons/gi";
import { GoCheck } from "react-icons/go";

export async function loader() {
  // const res = await fetch(``)
  console.log("solve")
  return "dummy";
}

export const Result = () => {
  const { dummyData } = useLoaderData();
  console.log(dummyData)
  return (
    <Flex minH="100vh" direction="column" align='center' justify='center' gap='30px'>
      <Heading as='h1' size='md'>テスト結果</Heading>
      <Flex minW="80%" direction='row' align='center' gap='50px'>
        <Stat minW="40%">
          <StatLabel>正答数</StatLabel>
          <StatNumber>
            <Flex minW="80%" direction='row' align='center' gap='10px'>
              <GoCheck />
              <Text display="inline-block"> 6/20</Text>
            </Flex>
          </StatNumber>
          <StatHelpText>
            <StatArrow type='increase' />
            23%
          </StatHelpText>
        </Stat>

        <Stat minW="40%">
          <StatLabel>かかった時間</StatLabel>
          <StatNumber>
            <Flex minW="80%" direction='row' align='center' gap='10px'>
              <GiSandsOfTime />
              <Text display="inline-block"> 45 s</Text>
            </Flex>
          </StatNumber>
          <StatHelpText>
            <StatArrow type='decrease' />
            9.05%
          </StatHelpText>
        </Stat>
      </Flex>
      <Card minW="80%">
        <CardHeader>
          <Heading size='md'>結果詳細</Heading>
        </CardHeader>

        <CardBody>
          <Stack divider={<StackDivider />} spacing='4'>
            <Flex minW="80%" direction='row' align='center' justify="space-between" gap='10px'>
              <Box>
                <Heading size='xs' textTransform='uppercase'>
                  Summary
                </Heading>
                <Text pt='2' fontSize='sm'>
                  View a summary of all your clients over the last month.
                </Text>
              </Box>
              <Icon as={GoCheck} color="green.600" bg="green.200" borderRadius="50%" width="5%" height="5%" />
            </Flex>
            <Box>
              <Heading size='xs' textTransform='uppercase'>
                Overview
              </Heading>
              <Text pt='2' fontSize='sm'>
                Check out the overview of your clients.
              </Text>
            </Box>
            <Box>
              <Heading size='xs' textTransform='uppercase'>
                Analysis
              </Heading>
              <Text pt='2' fontSize='sm'>
                See a detailed analysis of all your business clients.
              </Text>
            </Box>
          </Stack>
        </CardBody>
      </Card>
    </Flex>
  );
};