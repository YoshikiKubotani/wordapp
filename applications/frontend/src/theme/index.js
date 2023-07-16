import { extendTheme } from '@chakra-ui/react'

// Global style overrides
import styles from './styles'

// Component style overrides
import Button from './components/button'

const overrides = {
  config: {
    initialColorMode: 'system',
    useSystemColorMode: true,
  },
  fonts: {
    heading: `'Helvetica Neue', 'Noto Sans JP', sans-serif`,
    body: `'Helvetica Neue', 'Noto Sans JP', sans-serif`,
  },
  styles,
  // Other foundational style overrides go here
  components: {
    // Button,
    // Other components go here
  },
}

export default extendTheme(overrides)