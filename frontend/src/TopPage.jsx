import React from 'react';
import { useState, useEffect } from 'react';
import stopSign from './assets/stopSign.svg';
import warning from './assets/warning.svg';

export default function () {
    const [items, setItems] = useState([]);
    useEffect(() => {
        async function getItems() {
            const response = await fetch('http://54.64.250.189:5000/api/items');
            if (response.ok) {
                const data = await response.json();
                setItems(data);
            } else {
                console.log('There was a problem retrieving data');
                console.log(response.text);
            }
        }
        getItems();
    }, []);
    const [timeout, setTimeout] = useState(true);
    const [oneWeek, setOneWeek] = useState(true);

    const fakeData2 = [
        {
            item_name: "牛飯缶",
            quantity: 2,
            date_expiry: "2025-7-6"
        },
        {
            item_name: "トロ鯖缶",
            quantity: 3,
            date_expiry: "2025-7-5"
        }
    ];

    const survivalDate = 3;

    const ItemList = ({ condition, items, bg }) => {
        return (
            condition && items.map(item => {
                return (
                    <div key={item.id} style={{ backgroundColor: bg, color: 'white', borderRadius: '0.5em', padding: '.5em 2em' }}>
                        <img src={item.smallImageUrls} alt="supply thumbnail" width={100} style={{ borderRadius: '10px' }} />
                        <p style={{ textAlign: 'center', fontWeight: 'bold', marginBottom: 0 }}>{item.name && item.name.substring(0, 15) + (item.name.length > 15 ? "..." : "")}</p>
                        <div style={{ display: 'flex', gap: '1em' }}>
                            <p>x{item.quantity}</p>
                            <p>{new Date(item.date_expiry).toLocaleString().substring(0, 8)}</p>
                        </div>
                    </div>
                );
            })
        );

    };
    let timeoutItems = [];
    let closeTimeoutItems = [];
    if (items.length > 0) {
        timeoutItems = items.filter(item => (new Date(item.date_expiry)) < (new Date()));
        closeTimeoutItems = items.filter(item => (((new Date(item.date_expiry)) - new Date()) / (1000 * 60 * 60 * 24)) < 7);
    }

    return (
        <div style={{ paddingBottom: '8em' }}>
            <h1 style={{ marginBottom: 0 }} className='text-gray'>今日の伝言板</h1>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <h1 className='text-gray'>あなたの備蓄</h1>
                <h2 className='text-gray' style={{ backgroundColor: '#D9D9D9', padding: '.5em 1em', borderRadius: '1em' }}>{survivalDate}日間持つ</h2>
            </div>

            <div onClick={() => setTimeout(prev => !prev)} style={{ display: 'flex', alignItems: 'center', gap: '0.5em' }} className='text-gray unselectable-text'>
                <img src={stopSign} alt="stop sign emoji" />
                <h3>期限切れ</h3>
                <p style={{ backgroundColor: '#d9d9d9', padding: '0 .4em', borderRadius: '.4em' }}>{timeoutItems.length}個</p>
                <svg style={{ transform: `${timeout ? 'rotate(0)' : 'rotate(-90deg)'}`, transitionProperty: 'transform', transitionDuration: '200ms' }} xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="#50b4aa" viewBox="0 0 256 256"><path d="M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm45.66,93.66-40,40a8,8,0,0,1-11.32,0l-40-40a8,8,0,0,1,11.32-11.32L128,140.69l34.34-34.35a8,8,0,0,1,11.32,11.32Z"></path></svg>
            </div>
            <div style={{ display: 'flex', gap: '2em', overflowX: 'auto' }}>
                {timeoutItems.length > 0 && <ItemList condition={timeout} items={timeoutItems} bg={'#d34d4d'} />}
            </div>

            <div onClick={() => setOneWeek(prev => !prev)} style={{ display: 'flex', alignItems: 'center', gap: '0.5em' }} className='text-gray unselectable-text'>
                <img src={warning} alt="warning sign" />
                <h3>あと一週間</h3>
                <p style={{ backgroundColor: '#d9d9d9', padding: '0 .4em', borderRadius: '.4em' }}>{closeTimeoutItems.length}個</p>
                <svg style={{ transform: `${oneWeek ? 'rotate(0)' : 'rotate(-90deg)'}`, transitionProperty: 'transform', transitionDuration: '200ms' }} xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="#50b4aa" viewBox="0 0 256 256"><path d="M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm45.66,93.66-40,40a8,8,0,0,1-11.32,0l-40-40a8,8,0,0,1,11.32-11.32L128,140.69l34.34-34.35a8,8,0,0,1,11.32,11.32Z"></path></svg>
            </div>
            <div style={{ display: 'flex', gap: '2em', overflowX: 'auto' }}>
                <ItemList condition={oneWeek} items={closeTimeoutItems} bg={'#ffb056'} />
            </div>
        </div>
    );
}
