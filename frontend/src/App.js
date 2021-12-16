import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import BaseRouter from './routes';
import 'antd/dist/antd.css';
import CustomLayout from './pages/Layout';

export default function App(props){
  return (
    <div>
      <Router>
        <CustomLayout {...props}>
            <BaseRouter />
        </CustomLayout>
      </Router>
    </div>
  );
}