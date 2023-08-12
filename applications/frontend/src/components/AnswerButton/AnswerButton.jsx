import { React } from "react";
import {
  Box,
} from '@chakra-ui/react'

const AnswerButton = ({
  id,
  text,
  onClick,
  textColor,
  bgColor,
  hoverBgColor,
  status = 'default',
}) => {
  let isDisabled = false;
  let fontWeight = 'normal';
  let cursorType = 'pointer';
  if (status === 'correct') {
    textColor = 'green.400';
    bgColor = 'green.100';
    hoverBgColor = null;
    isDisabled = true;
    fontWeight = 'bold';
    cursorType = 'default';
  }
  else if (status === 'incorrect') {
    textColor = 'red.400';
    bgColor = 'red.100';
    hoverBgColor = null;
    isDisabled = true;
    fontWeight = 'bold';
    cursorType = 'default';
  }
  else if (status === 'disabled') {
    textColor = 'gray.400';
    bgColor = 'gray.100';
    hoverBgColor = null;
    isDisabled = true;
    cursorType = 'default';
  }
  return (
    <Box
      as='button'
      id={id}
      w='100%'
      h='100%'
      borderRadius='lg'
      bg={bgColor}
      color={textColor}
      _hover={{ bg: hoverBgColor }}
      onClick={onClick}
      disabled={isDisabled}
      fontWeight={fontWeight}
      width="20%"
      height="80px"
      fontSize="15px"
      paddingX="5px"
      paddingY="10px"
      cursor={cursorType}
    >
      {text}
    </Box>
  );
}

export default AnswerButton;