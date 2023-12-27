import { mode } from '@chakra-ui/theme-tools'

const Styles = {
  global: (props) => ({
    body: {
      fontFamily: 'body',
      color: mode('teal.600', 'teal.50')(props),
      bg: mode('teal.50', 'teal.900')(props),
      lineHeight: 'base',
    },
    '*::placeholder': {
      color: mode('gray.400', 'whiteAlpha.400')(props),
    },
    '*, *::before, &::after': {
      borderColor: mode('gray.200', 'whiteAlpha.300')(props),
      wordWrap: 'break-word',
    },
  }),
}

export default Styles