import { useState } from 'react';

function MyPage() {

  const [timeout, setTimeout] = useState(false);

  const userData = {
    name: "ゲスト",
    user_id: "1",
    family_id: "1",
    adult_num: "2",
    child_num: "1"
    };

  return (
    <>
        <header>
            <h1>My Page</h1>
        </header>

        <h2>{userData.name}</h2>
        <p>ユーザーID: {userData.user_id}</p>
        <p>ファミリーID: {userData.family_id}</p>
        <p>大人の人数: {userData.adult_num}人</p>
        <p>子供の人数: {userData.child_num}人</p>

      {/* <h1></h1>
      <h1>あなたの備蓄</h1>
      <h3 onClick={() => setTimeout(prev => !prev)}>期限切れ</h3>
      <svg style={{ transform: `${timeout ? 'rotate(0deg)' : 'rotate(-90)'}` }} xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="#50b4aa" viewBox="0 0 256 256"><path d="M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm45.66,93.66-40,40a8,8,0,0,1-11.32,0l-40-40a8,8,0,0,1,11.32-11.32L128,140.69l34.34-34.35a8,8,0,0,1,11.32,11.32Z"></path></svg>
      {timeout && fakeData.map(item => {
        return (
          <>
            <div key={item.name}>
              <p>{item.name}</p>
              <p>{item.count}</p>
              <p>{item.date}</p>
            </div>
          </>
        );
      })} */}
    </>
  );
}

export default MyPage;
