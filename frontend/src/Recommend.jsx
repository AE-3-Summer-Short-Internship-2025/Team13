import { Routes, Route, Link, useLocation } from 'react-router-dom';
import crown from './assets/crown.svg';
import ranking from './Ranking';
import cart from './assets/cart.svg';

function Recommend() {

    const location = useLocation();

    const goodsData = [
    {goods_id: "1", goods_name: "カバン"},
    {goods_id: "2", goods_name: "懐中電灯"},
    {goods_id: "3", goods_name: "水"}
    ];

    const expired_foodsData = [
    {foods_id: "1", foods_name: "乾パン"},
    {foods_id: "2", foods_name: "缶詰"}
    ];

    const oneweek_foodsData = [
    {foods_id: "3", foods_name: "米"}
    ];


    return (
    <>
        <header class="app-header">
            <div class="search-container" style={{display: 'flex', justifyContent: 'center'}}>
                <input type="search" class="search-box" style={{width: '200px'}}></input>
                <i class="search-icon">🔍</i>
            </div>
        </header>

        <h1 class="page-title">あなたへのおすすめ</h1>
        <main class="main-content">

            <section class="recommend-section insufficient-items">
                <div class="section-title-wrapper">
                    <h3 class="section-title"><span class="icon warning-icon">⚠️</span>足りていない防災グッズ</h3>
                </div>
                <div class="progress-bar-container">
                    <span class="progress-percentage">0%</span>
                    <progress class="progress-bar" max="100" value="0"></progress>
                    <span class="progress-percentage">100%</span>
                </div>
                <div class="item-list-container" style={{display: 'flex'}}>
                    {goodsData.map(good => (
                        <div key={good.goods_id} className="item-card">
                            <span>{good.goods_name}</span>
                            <div className="item-card add-item-card"><span>+</span></div>
                        </div>
                    ))}

                </div>
            </section>

            <section class="recommend-section expired-items">
                <div class="section-title-wrapper">
                    <h3 class="section-title"><span class="icon error-icon">❗</span>期限切れの食品({expired_foodsData.length})</h3>
                </div>
                <div className="item-list-container" style={{display: 'flex'}}>
                    {expired_foodsData.map(food => (
                        <div key={food.foods_id} className="item-card">
                            <span>{food.foods_name}</span>
                            <div className="item-card add-item-card"><span>+</span></div>
                        </div>
                    ))}
                </div>
            </section>

            <section class="recommend-section expiring-soon-items">
                <div class="section-title-wrapper">
                    <h3 class="section-title"><span class="icon alert-icon">🔼</span>期限一週間前({oneweek_foodsData.length})</h3>
                </div>
                <div className="item-list-container">
                    {oneweek_foodsData.map(food => (
                        <div key={food.foods_id} className="item-card">
                            <span>{food.foods_name}</span>
                            <div className="item-card add-item-card"><span>+</span></div>
                        </div>
                    ))}
                </div>
            </section>
        </main>
        <div>
            {location.pathname !== '/ranking' && 
            <Link to={'/ranking'}><img src={crown} alt="crown icon" width={'50em'} /></Link>}
        </div>
    </>
    );
}

export default Recommend;