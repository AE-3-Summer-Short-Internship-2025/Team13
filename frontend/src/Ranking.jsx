import { useState, useEffect } from 'react';
// import goods_icon from ''

function Ranking() {

    const [bestSeller, setItems] = useState([]);
    useEffect(() => {
        async function getItems() {
            const response = await fetch('http://54.64.250.189:5000/api/item_ranking', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ sort_key: '-reviewCount', keyword: '防災用品' })
                // -reviewCount
                // -reviewAverage
            });
            if (response.ok) {
                const data = await response.json();
                setItems(data);
                console.log(data);
            } else {
                console.log('There was a problem retrieving data');
                console.log(response.text);
            }
        }
        getItems();
    }, []);

    const [latest, setLatest] = useState(true);



    const sale_sortData = [
        { rank: "1", goods_id: "1", goods_name: "カバン" },
        { rank: "2", goods_id: "2", goods_name: "懐中電灯" },
        { rank: "3", goods_id: "3", goods_name: "水" },
        { rank: "4", foods_id: "4", goods_name: "乾パン" }
    ];

    const new_sortData = [
        { rank: "1", goods_id: "2", goods_name: "懐中電灯" },
        { rank: "2", goods_id: "3", goods_name: "水" },
        { rank: "3", foods_id: "4", foods_name: "乾パン" },
        { rank: "4", goods_id: "1", goods_name: "カバン" }
    ];

    const good_sortData = [
        { rank: "1", foods_id: "3", foods_name: "水" },
        { rank: "2", goods_id: "4", goods_name: "乾パン" },
        { rank: "3", goods_id: "1", goods_name: "カバン" },
        { rank: "4", foods_id: "2", foods_name: "懐中電灯" }
    ];

    const cheap_sortData = [
        { rank: "1", goods_id: "4", goods_name: "乾パン" },
        { rank: "2", goods_id: "1", goods_name: "カバン" },
        { rank: "3", foods_id: "2", foods_name: "懐中電灯" },
        { rank: "4", foods_id: "3", foods_name: "水" }
    ];

    const ItemList = ({ items }) => {
        return (
            items.slice(1, 4).map(item => {
                return (
<<<<<<< HEAD
                    <div key={item.商品名} className="overall">
                        <a href={item.itemURL} target='_blank'>
                            <img src={item.画像[0].imageUrl} alt="goods' thumbnail" style={{ width: '6em', borderRadius: '2em' }} />
                        </a>
                        <div style={{ borderRadius: '50em', border: 'solid .1em lightgrey', aspectRatio: '1' }}>
                            {/* <span>{item.商品名 || item.foods_name}</span> */}
                            <p>{item.商品名.substring(0, 20)}...</p>
=======
                        <div key={item.rank} className="overall" style={{width:'100px', overflowX: 'auto'}}>
                                <div style={{borderRadius:'50em', border: 'solid .1em lightgrey', width:'70px', aspectRatio:'1', alignItems:'center',   display: 'flex', justifyContent: 'center'}}>
                                    <span>{item.goods_name || item.foods_name}</span>
                                </div>
                            <p>{item.rank}位</p>
>>>>>>> 025e75b09b81bf1d393730860b1760dc9d987304
                        </div>
                        <div className="item-card add-item-card"><span>+</span></div>
                        {/* <p>{item.評価点}位</p> */}
                        <p>{item.評価点}</p>
                    </div>
                );
            })
        );
    };

    const SortedItemList = ({ items }) => {
        return (
            items.sort(items)
        );
    };

    return (
        <>

            <div className="ranking-page">
                <header className="app-header">
<<<<<<< HEAD
                    <div className="search-container" style={{ display: 'flex', justifyContent: 'center' }}>
                        <input type="search" className="search-box" style={{ width: '200px' }}></input>
                        <i className="search-icon">🔍</i>
=======
                    <div className="search-container" style={{ display: 'flex',justifyContent: 'center' }}>
                        <input type="search" className="search-box" style={{width:'200px', height:'30px'}}></input>
>>>>>>> 025e75b09b81bf1d393730860b1760dc9d987304
                    </div>
                </header>

                <main className="main-content">
                    <h1 className="page-title">人気な商品</h1>

<<<<<<< HEAD
                    <section className="ranking-category">
                        <h3 className="category-title">売れ筋</h3>
                        <div style={{ display: 'flex', gap: '1em', overflowX: 'auto', width: '350px' }}>
                            <ItemList items={bestSeller} />
=======
            <section className="ranking-category">
                <h3 className="category-title">売れ筋</h3>
                    <div style={{display: 'flex', gap: '2em', overflowX: 'auto'}}>
                        {/* <ItemList condition={sale} items={saleItems} /> */}
                    </div>
            </section>

            <section className="ranking-category">
                <h3 className="category-title">新着</h3>
                    <div style={{display: 'flex'}}>
                    {new_sortData.map(latest => (
                        <div key={latest.rank} className="overall" style={{width:'100px'}}>
                                <div style={{borderRadius:'50em', border: 'solid .1em lightgrey', width:'70px', aspectRatio:'1', alignItems:'center',   display: 'flex', justifyContent: 'center'}}>
                                    <span>{latest.goods_name || latest.foods_name}</span>
                                </div>
                            <p>{latest.rank}位</p>
>>>>>>> 025e75b09b81bf1d393730860b1760dc9d987304
                        </div>
                    </section>

                    {/* <section className="ranking-category">
                        <h3 className="category-title">新着</h3>
                        <div style={{ display: 'flex' }}>
                            {items.map(latest => (
                                <div key={latest.rank} className="overall" style={{ width: '100px' }}>
                                    <div style={{ borderRadius: '50em', border: 'solid .1em lightgrey', width: '70px', aspectRatio: '1', alignItems: 'center', display: 'flex', justifyContent: 'center' }}>
                                        <span>{latest.goods_name || latest.foods_name}</span>
                                    </div>
                                    <div className="item-card add-item-card"><span>+</span></div>
                                    <p>{latest.rank}位</p>
                                </div>
<<<<<<< HEAD
                            ))}
=======
                            <p>{good.rank}位</p>
>>>>>>> 025e75b09b81bf1d393730860b1760dc9d987304
                        </div>
                    </section> */}

                    {/* <section className="ranking-category">
                        <h3 className="category-title">評価順</h3>
                        <div style={{ display: 'flex' }}>
                            {good_sortData.map(good => (
                                <div key={good.rank} className="overall" style={{ width: '100px' }}>
                                    <div style={{ borderRadius: '50em', border: 'solid .1em lightgrey', width: '70px', aspectRatio: '1', alignItems: 'center', display: 'flex', justifyContent: 'center', }}>
                                        <span>{good.goods_name || good.foods_name}</span>
                                    </div>
                                    <div className="item-card add-item-card"><span>+</span></div>
                                    <p>{good.rank}位</p>
                                </div>
<<<<<<< HEAD
                            ))}
=======
                            <p>{cheap.rank}位</p>
>>>>>>> 025e75b09b81bf1d393730860b1760dc9d987304
                        </div>
                    </section> */}

                    {/* <section className="ranking-category">
                        <h3 className="category-title">価格の低い順</h3>
                        <div style={{ display: 'flex' }}>
                            {cheap_sortData.map(cheap => (
                                <div key={cheap.rank} className="overall" style={{ width: '100px' }}>
                                    <div style={{ borderRadius: '50em', border: 'solid .1em lightgrey', width: '70px', aspectRatio: '1', alignItems: 'center', display: 'flex', justifyContent: 'center', }}>
                                        <span>{cheap.goods_name || cheap.foods_name}</span>
                                    </div>
                                    <div className="item-card add-item-card"><span>+</span></div>
                                    <p>{cheap.rank}位</p>
                                </div>
                            ))}
                        </div>
                    </section> */}

                </main>
            </div>

        </>
    );
}

export default Ranking;