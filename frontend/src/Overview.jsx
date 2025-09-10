import React from 'react'

// export default function Overview() {
//   return (
//     <div>Overview</div>
//   )
// }
import { useEffect, useState } from "react";

function TopPage() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    fetch("http://54.64.250.189:5000/api/items") // Flaskのエンドポイント
      .then(res => res.json())
      .then(data => setItems(data));
  }, []);

  return (
    <div>
      <h1>備蓄一覧</h1>
      <ul>
        {items.map(item => (
          <li key={item.id}>
          {item.name} ({item.quantity})
          <img src={item.smallImageUrlsl} alt="商品画像" />
        </li>
        
        ))}
      </ul>
    </div>
  );
}
export default TopPage;