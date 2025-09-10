import React from 'react';
import { useEffect, useState } from "react";

function TopPage() {
  const [items, setItems] = useState([]);
  const [isFood, setIsFood] = useState(true);

  useEffect(() => {
    fetch("http://54.64.250.189:5000/api/items") // Flaskのエンドポイント
      .then(res => res.json())
      .then(data => setItems(data));
  }, []);

  const handleToggle = (bool) => {
    setIsFood(bool);
  };

  return (
    <div>
      <h1 style={{ textAlign: 'center' }} className='text-gray'>備蓄一覧</h1>
      <div>
        <div style={{ display: 'flex', justifyContent: 'center', }}>
          <div style={{ position: 'relative', color: 'white', fontWeight: '500', backgroundColor: '#D9D9D9', display: 'flex', marginTop: '.5em', borderRadius: '1em', gap: '4em', padding: '0 1.5em' }}>
            <div style={{ backgroundColor: '#a39e9e', position: 'absolute', width: isFood ? '6em' : '8em', height: '3.5em', borderRadius: '1em', [isFood ? 'left' : 'right']: '0' }}></div>
            <p style={{ zIndex: '1' }} onClick={() => handleToggle(true)}>食料品</p>
            <p style={{ zIndex: '1' }} onClick={() => handleToggle(false)}>防災グッズ</p>
          </div>
        </div>
      </div>
      {isFood &&
        <div style={{ display: 'flex', justifyContent: 'center', marginTop: '2em', borderRadius: '2em' }}>
          <table style={{ borderCollapse: 'collapse' }} className='text-gray'>
            <thead>
              <tr>
                <th style={{ border: '1px solid #8C8989', padding: '1em' }}>個数</th>
                <th style={{ border: '1px solid #8C8989' }}>防災グッズ</th>
              </tr>
            </thead>
            {items.map(item => {
              return (
                <tbody key={item.id}>
                  <tr>
                    <td style={{ border: '1px solid #8C8989', padding: '.5em' , textAlign: 'center'}}>{item.quantity}</td>
                    <td style={{ border: '1px solid #8C8989', padding: '.5em' }}>{item.name}</td>
                  </tr>
                </tbody>
              );
            })}
          </table>
        </div>
      }

      <ul>
        {items.map(item => (
          <li key={item.id}>
          {item.name} ({item.quantity})
          <img src={item.smallImageUrls} alt="商品画像" />
        </li>
        
        ))}
      </ul>
    </div >
  );
}
export default TopPage;