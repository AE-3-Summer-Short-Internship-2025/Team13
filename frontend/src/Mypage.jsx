import { useState } from 'react';
import icon from './assets/icon.svg'

function MyPage() {

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

        <main style = {{display: 'flex', alignItems: 'center', backgroundColor: '#D3D3D3', padding: '.5em 1em', borderRadius: '1em'}}>
            <img src={icon} alt="icon" style={{borderRadius:'10em', backgroundColor:'rgb(210, 230, 225)'}}/>
            <div style = {{marginLeft: '1em'}}>
                <h2>{userData.name}</h2>
                <p>ユーザーID: {userData.user_id}</p>
                <p>ファミリーID: {userData.family_id}</p>
            </div>
        </main>

        <sub>
            <div>
                <h3>家族メンバー</h3>
                <p>大人人数: <span style={{ fontWeight: 'bold', backgroundColor: '#D3D3D3', borderRadius: '0.5em', padding: '.3em 2em'}}>{userData.adult_num}</span>人</p>
                <p>子供人数: <span style={{ fontWeight: 'bold', backgroundColor: '#D3D3D3', borderRadius: '0.5em', padding: '.3em 2em'}}>{userData.child_num}</span>人</p>
            </div>
        </sub>

        <h3>各種設定</h3>
        <div style={{display: 'flex', flexDirection: 'column', backgroundColor: '#D3D3D3', borderRadius: '0.5em'}}>
            <a style={{borderBottom: '.1em solid grey', padding:'.5em'}}>基本情報の編集</a>
            <a style={{borderBottom: '.1em solid grey', padding:'.5em'}}>通知</a>
            <a style={{borderBottom: '.1em solid grey', padding:'.5em'}}>ヘルプ</a>
            <a style={{padding:'.5em'}}>ログアウト</a>
        </div>
    </>
  );
}

export default MyPage;
