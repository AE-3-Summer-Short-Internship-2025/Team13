import { useState } from 'react';
// import goods_icon from ''

function Ranking() {

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

            <div class="ranking-page">
                <header class="app-header">
                    <div class="search-container">
                        <input type="search" class="search-box" placeholder="キーワードを検索"></input>
                        <i class="search-icon">🔍</i>
                    </div>
                </header>

                <main class="main-content">
                    <h1 class="page-title">人気な商品</h1>

                    <section class="ranking-category">
                        <h2 class="category-title">総合</h2>
                        <div class="ranking-list-container" style={{ display: 'flex' }}>
                            <div class="ranking-item rank-1">
                                <div class="item-circle">
                                    <span class="crown-icon">👑</span>
                                    <span class="rank-number">1位</span>
                                </div>
                                <div class="item-name-placeholder"></div>
                            </div>
                            <div class="ranking-item rank-2">
                                <div class="item-circle">
                                    <span class="rank-number">2位</span>
                                </div>
                                <div class="item-name-placeholder"></div>
                            </div>
                            <div class="ranking-item rank-3">
                                <div class="item-circle">
                                    <span class="rank-number">3位</span>
                                </div>
                                <div class="item-name-placeholder"></div>
                            </div>
                        </div>
                    </section>

                    <section class="ranking-category">
                        <h2 class="category-title">新着</h2>
                        <div style={{ display: 'flex' }}>
                            {new_sortData.map(latest => (
                                <div key={latest.rank} className="overall" style={{ width: '80px' }}>
                                    <div style={{ borderRadius: '50em', border: 'solid .2em black' }}><span>{latest.goods_name || latest.foods_name}</span>
                                        <div className="item-card add-item-card"><span>+</span></div>
                                        <p>{latest.rank}位</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </section>

                    <section class="ranking-category">
                        <h2 class="category-title">評価順</h2>
                        <div class="ranking-list-container">
                            <div class="ranking-item rank-1">
                                <div class="item-circle"><span class="crown-icon">👑</span><span class="rank-number">1位</span></div>
                                <div class="item-name-placeholder"></div>
                            </div>
                            <div class="ranking-item rank-2">
                                <div class="item-circle"><span class="rank-number">2位</span></div>
                                <div class="item-name-placeholder"></div>
                            </div>
                            <div class="ranking-item rank-3">
                                <div class="item-circle"><span class="rank-number">3位</span></div>
                                <div class="item-name-placeholder"></div>
                            </div>
                        </div>
                    </section>

                    <section class="ranking-category">
                        <h2 class="category-title">売れ筋</h2>
                        <div class="ranking-list-container">
                            <div class="ranking-item rank-1">
                                <div class="item-circle"><span class="crown-icon">👑</span><span class="rank-number">1位</span></div>
                                <div class="item-name-placeholder"></div>
                            </div>
                            <div class="ranking-item rank-2">
                                <div class="item-circle"><span class="rank-number">2位</span></div>
                                <div class="item-name-placeholder"></div>
                            </div>
                            <div class="ranking-item rank-3">
                                <div class="item-circle"><span class="rank-number">3位</span></div>
                                <div class="item-name-placeholder"></div>
                            </div>
                        </div>
                    </section>

                </main>
            </div>

        </>
    );
}

export default Ranking;