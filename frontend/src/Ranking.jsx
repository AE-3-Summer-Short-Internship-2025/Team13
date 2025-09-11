import { useState, useEffect } from 'react';
// import goods_icon from ''

function Ranking() {

    const [sold, set_soldItems] = useState([]);
    useEffect(() => {
        fetch("http://54.64.250.189:5000/api/items") // Flaskのエンドポイント
            .then(res => res.json())
            .then(data => set_soldItems(data));
    }, []);

    console.log(sold);


    const sold_sortData = [
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

    return (
        <>

            <div className="ranking-page">
                <header className="app-header">
                    <div className="search-container" style={{ display: 'flex', justifyContent: 'center' }}>
                        <input type="search" className="search-box" style={{width:'200px'}}></input>
                        <i className="search-icon">🔍</i>
                    </div>
                </header>

                <main className="main-content">
                    <h1 className="page-title">人気な商品</h1>

            <section className="ranking-category">
                <h3 className="category-title">売れ筋</h3>
                    <div style={{display: 'flex'}}>
                    {sold_sortData.map(sold => (
                        <div key={sold.rank} className="overall" style={{width:'100px'}}>
                                <div style={{borderRadius:'50em', border: 'solid .1em lightgrey', width:'70px', aspectRatio:'1', alignItems:'center',   display: 'flex', justifyContent: 'center'}}>
                                    <span>{sold.goods_name || sold.foods_name}</span>
                                </div>
                            <div className="item-card add-item-card"><span>+</span></div>
                            <p>{sold.rank}位</p>
                        </div>
                    ))}
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
                                <div className="item-card add-item-card"><span>+</span></div>
                            <p>{latest.rank}位</p>
                        </div>
                    ))}
                    </div>
            </section>

            <section className="ranking-category">
                <h3 className="category-title">評価順</h3>
                    <div style={{display: 'flex'}}>
                    {good_sortData.map(good => (
                        <div key={good.rank} className="overall" style={{width:'100px'}}>
                                <div style={{borderRadius:'50em', border: 'solid .1em lightgrey', width:'70px', aspectRatio:'1', alignItems:'center',   display: 'flex', justifyContent: 'center',}}>
                                    <span>{good.goods_name || good.foods_name}</span>
                                </div>
                            <div className="item-card add-item-card"><span>+</span></div>
                            <p>{good.rank}位</p>
                        </div>
                    ))}
                    </div>
            </section>

            <section className="ranking-category">
                <h3 className="category-title">価格の低い順</h3>
                    <div style={{display: 'flex'}}>
                    {cheap_sortData.map(cheap => (
                        <div key={cheap.rank} className="overall" style={{width:'100px'}}>
                                <div style={{borderRadius:'50em', border: 'solid .1em lightgrey', width:'70px', aspectRatio:'1', alignItems:'center',   display: 'flex', justifyContent: 'center',}}>
                                    <span>{cheap.goods_name || cheap.foods_name}</span>
                                </div>
                            <div className="item-card add-item-card"><span>+</span></div>
                            <p>{cheap.rank}位</p>
                        </div>
                    ))}
                    </div>
            </section>

                </main>
            </div>

        </>
    );
}

export default Ranking;