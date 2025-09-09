import { useState } from 'react';
import { Routes, Route } from 'react-router-dom';
import MyPage from './Mypage';
import TopPage from './TopPage';

function App() {

  return (
    <>
      <Routes>
        <Route path='/' element={<TopPage />} />
        <Route path='mypage' element={<MyPage />} />
      </Routes>
    </>
  );
}

export default App;
