import { useState } from 'react';
import icon from './assets/icon.svg';
import save from './assets/save.svg';
import edit from './assets/edit.svg';

function MyPage() {
    const [adults, setAdults] = useState(0);
    const [children, setChildren] = useState(0);
    const [editAdult, setEditAdult] = useState(false);
    const [editChildren, setEditChildren] = useState(false);

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

<<<<<<< HEAD
            <main style={{ display: 'flex', alignItems: 'center', backgroundColor: '#D3D3D3', padding: '.5em 1em', borderRadius: '1em' }}>
                <img src={icon} alt="icon" style={{ borderRadius: '10em', backgroundColor: 'rgb(210, 230, 225)' }} />
                <div style={{ marginLeft: '1em' }}>
                    <h2>{userData.name}</h2>
                    <p>ユーザーID: {userData.user_id}</p>
                    <p>ファミリーID: {userData.family_id}</p>
                </div>
            </main>

            <sub>
                <div>
                    <h3>家族メンバー</h3>
                    <div style={{display: 'flex', paddingRight: '1em', alignItems: 'center', gap: '1em' }}>
                        <p>大人人数:</p>
                        <div style={{ fontWeight: 'bold', backgroundColor: '#D3D3D3', borderRadius: '0.5em', padding: '.3em 2em' }}>{adults}人</div>
                        <img onClick={() => setEditAdult(prev => !prev)} src={editAdult ? save : edit} alt="edit / save icon" />
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', paddingRight: '1em', alignItems: 'center' }}>
                        <div>
                            <p>子供人数:</p><span style={{ fontWeight: 'bold', backgroundColor: '#D3D3D3', borderRadius: '0.5em', padding: '.3em 2em' }}>{adults}人</span>
                            <img onClick={() => setEditChildren(prev => !prev)} src={editChildren ? save : edit} alt="edit / save icon" />
                        </div>
                    </div>
                </div>
            </sub>

            <h3>各種設定</h3>
            <div style={{ display: 'flex', flexDirection: 'column', backgroundColor: '#D3D3D3', borderRadius: '0.5em' }}>
                <a style={{ borderBottom: '.1em solid grey', padding: '.5em' }}>基本情報の編集</a>
                <a style={{ borderBottom: '.1em solid grey', padding: '.5em' }}>通知</a>
                <a style={{ borderBottom: '.1em solid grey', padding: '.5em' }}>ヘルプ</a>
                <a style={{ padding: '.5em' }}>ログアウト</a>
            </div>
        </>
    );
=======
        <main style = {{display: 'flex', alignItems: 'center', backgroundColor: '#D3D3D3', padding: '.5em 1em', borderRadius: '1em', margin:'1em'}}>
            <img src={icon} alt="icon" style={{borderRadius:'10em', backgroundColor:'rgb(210, 230, 225)'}}/>
            <div style = {{marginLeft: '1em'}}>
                <h2>{userData.name}</h2>
                <p>ユーザーID: {userData.user_id}</p>
                <p>ファミリーID: {userData.family_id}</p>
            </div>
        </main>

        <sub>
            <div style={{margin :'.5em'}}>
                <h3>家族メンバー</h3>
                <p>大人人数: <span style={{ fontWeight: 'bold', backgroundColor: '#D3D3D3', borderRadius: '0.5em', padding: '.3em 2em'}}>{userData.adult_num}</span>人</p>
                <p>子供人数: <span style={{ fontWeight: 'bold', backgroundColor: '#D3D3D3', borderRadius: '0.5em', padding: '.3em 2em'}}>{userData.child_num}</span>人</p>
            </div>
        </sub>
        <div style={{margin :'.5em'}}>
            <h3>各種設定</h3>
            <div style={{display: 'flex', flexDirection: 'column', backgroundColor: '#D3D3D3', borderRadius: '0.5em'}}>
                <a style={{borderBottom: '.1em solid grey', padding:'.5em'}}>基本情報の編集</a>
                <a style={{borderBottom: '.1em solid grey', padding:'.5em'}}>通知</a>
                <a style={{borderBottom: '.1em solid grey', padding:'.5em'}}>ヘルプ</a>
                <a style={{padding:'.5em'}}>ログアウト</a>
            </div>
        </div>
    </>
  );
>>>>>>> 025e75b09b81bf1d393730860b1760dc9d987304
}

export default MyPage;
