import React from 'react';
import ReactDOM from 'react-dom/client';
import {
  createBrowserRouter,
  RouterProvider
} from "react-router-dom";
import { ColorModeScript, ChakraProvider } from '@chakra-ui/react'
import ModeSelection from "./pages/ModeSelection";
import Result, { resultLoader } from "./pages/Result";
import Solve, { solveLoader } from "./pages/Solve";
import StartPage from "./pages/StartPage";
import WordLevel from "./pages/WordLevel";
import NoMatch from "./pages/NoMatch";
import reportWebVitals from './reportWebVitals';
import './index.css';
import Root from './Root'
import theme from './theme';

const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    errorElement: <NoMatch />,
    children: [
      {
        index: true,
        element: <StartPage />,
      },
      {
        path: "mode",
        element: <ModeSelection />,
      },
      {
        path: "wordlevel",
        element: <WordLevel />,
      },
      {
        path: "solve",
        element: <Solve />,
        loader: solveLoader,
      },
      {
        path: "result",
        element: <Result />,
        loader: resultLoader,
      },
    ],
  },
]);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <ColorModeScript initialColorMode={theme.config.initialColorMode} />
    <ChakraProvider>
      <RouterProvider router={router} />
    </ChakraProvider>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals(console.log);
