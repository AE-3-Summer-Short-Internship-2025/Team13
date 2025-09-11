import { Routes, Route, Link, useLocation } from 'react-router-dom';
import { useContext, useEffect, useState } from 'react';
import { MenuContext } from './context/MenuContext';
import MyPage from './Mypage';
import TopPage from './TopPage';
import RegisterPage from './RegisterPage';
import Recommend from './Recommend';
import Overview from './Overview';
import Ranking from './Ranking';
import camera from './assets/camera.svg';
import home from './assets/home.svg';
import calendar from './assets/calendar.svg';
import cart from './assets/cart.svg';
import profile from './assets/profile.svg';


function App() {
  const location = useLocation();
  const { menu, setMenu } = useContext(MenuContext);
  return (
    <div style={{height: '100%' }}>
      {location.pathname !== '/mypage' && <Link to={'/mypage'}><img src={profile} alt="profile icon" style={{ position: 'fixed', right: '1em', zIndex: 10, backgroundColor: 'white', borderRadius: '100px' }} width={'50em'} /></Link>}
      <Routes>
        <Route path='/' element={<TopPage />} />
        <Route path='overview' element={<Overview />} />
        <Route path='mypage' element={<MyPage />} />
        <Route path='register' element={<RegisterPage />} />
        <Route path='recommend' element={<Recommend />} />
        <Route path='ranking' element={<Ranking />} />
      </Routes>
      {
        location.pathname !== '/register' &&
        (
          <div style={{ position: 'fixed', bottom: 0, backgroundColor: '#ededed', padding: '2em', borderRadius: '100px', transform: 'translate(-20%, 20%)' }}>
            <Link to="/register">
              <img src={camera} alt="camera icon" width='80px' />
            </Link>
          </div>
        )
      }
      <div style={{ pointerEvents: menu ? 'none' : 'auto', opacity: menu ? 0 : '100%', transform: menu ? 'translateY(1em)' : '', position: 'fixed', right: 0, bottom: '6em', display: 'flex', flexDirection: 'column', gap: '1em', backgroundColor: '#ededed', padding: '1em .5em', marginRight: '1.25em', borderRadius: '.5em', transitionProperty: 'all', transitionDuration: '300ms' }}>
        <Link to={'/'}>
          <img src={home} alt="home icon" />
        </Link>
        <Link to={'/overview'}>
          <img src={calendar} alt="calendar icon" />
        </Link>
        <Link to={'/recommend'}>
          <img src={cart} alt="cart icon" />
        </Link>
      </div>
      <div onClick={() => setMenu(prev => !prev)} style={{ backgroundColor: '#50b4aa', position: 'fixed', bottom: 0, right: 0, margin: '1em', borderRadius: '100px', width: '4em', height: '4em' }}>
        <svg style={{ transform: `${menu ? 'rotate(-45deg) translateX(-6px)  translateY(20px)' : 'rotate(0) translateX(16px) translateY(16px)'}`, transformOrigin: 'top left', transitionProperty: 'transform', transitionDuration: '300ms' }} xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32" fill="none">
          <path d="M2.3418 2.25293L30.1509 30.062" stroke="white" strokeWidth="3.15189" strokeLinecap="round" />
        </svg>
        <svg style={{ transform: menu ? 'translateY(2px) translateX(-15px)' : 'translateX(-15px)', opacity: menu ? '100%' : '0', transitionProperty: 'all', transitionDuration: '300ms' }} xmlns="http://www.w3.org/2000/svg" width="32" height="4" viewBox="0 0 32 4" fill="none">
          <path d="M1.90723 2.15723H30.1504" stroke="white" strokeWidth="3.15189" strokeLinecap="round" />
        </svg>
        <svg style={{ transform: `${menu ? 'rotate(45deg) translateX(14px) translateY(-32px)' : 'translateY(-20px) translateX(16px)'}`, transformOrigin: 'top left', transitionProperty: 'transform', transitionDuration: '300ms' }} xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32" fill="none">
          <path d="M1.90723 30.062L30.1504 2.25293" stroke="white" strokeWidth="3.15189" strokeLinecap="round" />
        </svg>
      </div>
    </div>
  );
}

export default App;
