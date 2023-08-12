import React, { useState, useEffect} from "react";
import { useLoaderData } from "react-router-dom";
import {
  Box,
  Flex,
  Heading,
  Stack,
  Text,
  Step,
  StepDescription,
  StepIcon,
  StepIndicator,
  StepNumber,
  StepSeparator,
  StepStatus,
  StepTitle,
  Stepper,
  useSteps,
  Progress,
} from '@chakra-ui/react'

import { EventApi } from "../../api";
import AnswerButton from "../../components/AnswerButton";

const defaultTestInfo = {
  test_id: 1,
  test_name: "test",
  test_description: "test",
  test_type: "test",
  test_level: "test",
  test_genre: "test",
  test_question_num: 1,
}

const defaultItemInfo = {
  item_index: 1,
  english: "test",
  op1: "test",
  op2: "test",
  op3: "test",
  op4: "test",
}


export async function loader({ params }) {
  let res;
  try {
    res = await EventApi.makeTest(Number(params.gradeId));
  }
  catch (err) {
    console.log(err);
    window.alert("テストの作成に失敗しました。");
    return;
  }
  const testItemUuidList = await res.json();

  console.log("Item IDs in a created test", testItemUuidList)
  return { testItemUuidList };
}

export const Solve = ({}) => {
  const { testItemUuidList } = useLoaderData();
  const [ itemIndex, setItemIndex] = useState(0);
  const [ isLoading, setIsLoading ] = useState(true);
  const [ itemInfo, setItemInfo ] = useState(defaultItemInfo);
  const [ buttonStatus, setButtonStatus ] = useState({
    'op1': 'default',
    'op2': 'default',
    'op3': 'default',
    'op4': 'default',
  });
  const { activeStep, setActiveStep } = useSteps({
    index: 0,
    count: testItemUuidList.length,
  })

  // 初回のレンダリング時に実行。最初の問題を取得して表示する。
  useEffect(() => {
    const fetchData = async () => {
      const firstItemInfo = await getItemInfo(testItemUuidList[itemIndex]);
      setItemInfo( prevItemInfo => {
        return {
          ...prevItemInfo,
          item_index: itemIndex,
          english: firstItemInfo.english,
          op1: firstItemInfo.op1,
          op2: firstItemInfo.op2,
          op3: firstItemInfo.op3,
          op4: firstItemInfo.op4,
        }
      });
      setIsLoading(false);
    }

    fetchData();
  }, [])

  // 与えられたUUIDの問題を取得する
  const getItemInfo = async (itemUuid) => {
    let res;
    try {
      res = await EventApi.getItemInfo(itemUuid)
    }
    catch (err) {
      console.log(err);
      window.alert("問題の取得に失敗しました。");
      return;
    }
    const itemInfo = await res.json();
    console.log("Item Info", itemInfo);
    return itemInfo;
  }

  // 次の問題へ進むボタンを押したときの挙動
  const onClickNext = async () => {
    // 問題番号を次に進める
    setItemIndex(itemIndex + 1);

    // 次の問題を取得
    const nextItemInfo = await getItemInfo(testItemUuidList[itemIndex]);
    // 取得した問題を表示(stateに反映)
    setItemInfo( prevItemInfo => {
      return {
        ...prevItemInfo,
        item_index: itemIndex,
        english: nextItemInfo.english,
        op1: nextItemInfo.op1,
        op2: nextItemInfo.op2,
        op3: nextItemInfo.op3,
        op4: nextItemInfo.op4,
      }
    });

    // Stepperの表記を更新
    setActiveStep(itemIndex);
  }

  const onClickChoice = async (e) => {
    console.log(e.target.textContent );
    let res;
    try {
      res = await EventApi.getItemAnswer(testItemUuidList[itemIndex])
    }
    catch (err) {
      console.log(err);
      window.alert("問題の取得に失敗しました。");
      return;
    }
    const itemAnswerInfo = await res.json();
    console.log("Answer Info", itemAnswerInfo);

    const userAnswer = e.target.textContent;
    const itemAnswer = itemAnswerInfo.answer;

    let selectedButtonStatus = '';
    if (itemAnswer === userAnswer) {
      selectedButtonStatus = 'correct';
    }
    else {
      selectedButtonStatus = 'incorrect';
    }

    setButtonStatus(prevButtonStatus => {
      let newStatus = {};

      for (let key in prevButtonStatus) {
        // クリックされたボタンのIDと同じ場合、上記で指定したステータスに、それ以外の場合は'disabled'に設定
        newStatus[key] = key === e.target.id ? selectedButtonStatus : 'disabled';
      }

      return newStatus;
    });
  }

  // 初回のレンダリングが終わり、最初の問題が取得＆表示されるまでの間はローディング画面を表示する
  if (isLoading) {
    return (
      <Box>Loading ...</Box>
    )
  }
  console.log("Item Info", itemInfo)

  return (
      <Flex minH="100vh" direction="column" align='center' justify='center' gap='30px'>
        <Heading as='h1' size='xl'>問題を解く</Heading>
        <Stack>
          <Stepper size='xs' index={activeStep} gap='10px'>
            {testItemUuidList.map((_, index) => (
              <Step key={index} gap='0'>
                <StepIndicator>
                  <StepStatus complete={<StepIcon />} />
                </StepIndicator>
                <StepSeparator _horizontal={{ ml: '0' }} />
              </Step>
            ))}
          </Stepper>
          <Text>
            問題 {activeStep + 1} / {testItemUuidList.length} : <b>{itemInfo.english}</b>
          </Text>
        </Stack>
        <Flex direction='row' width="80%" align='center' justify='center' gap='10px'>
          <AnswerButton
            id='op1'
            text={itemInfo.op1}
            onClick={onClickChoice}
            textColor='teal.500'
            bgColor='teal.100'
            hoverBgColor={'teal.200'}
            status={buttonStatus['op1']}
          />
          <AnswerButton
            id='op2'
            text={itemInfo.op2}
            onClick={onClickChoice}
            textColor='teal.500'
            bgColor='teal.100'
            hoverBgColor={'teal.200'}
            status={buttonStatus['op2']}
          />
          <AnswerButton
            id='op3'
            text={itemInfo.op3}
            onClick={onClickChoice}
            textColor='teal.500'
            bgColor='teal.100'
            hoverBgColor={'teal.200'}
            status={buttonStatus['op3']}
          />
          <AnswerButton
            id='op4'
            text={itemInfo.op4}
            onClick={onClickChoice}
            textColor='teal.500'
            bgColor='teal.100'
            hoverBgColor={'teal.200'}
            status={buttonStatus['op4']}
          />
        </Flex>
      </Flex>
    );
};