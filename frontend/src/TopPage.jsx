import React from 'react';
import { useState } from 'react';
import camera from './assets/camera.svg';

export default function () {
    const [timeout, setTimeout] = useState(true);
    const [oneWeek, setOneWeek] = useState(true);

    const fakeData = [
        {
            name: "かんぱん",
            count: 2,
            date: "2025-7-6"
        },
        {
            name: "鯖缶",
            count: 3,
            date: "2025-7-5"
        }
    ];
    const fakeData2 = [
        {
            name: "牛飯缶",
            count: 2,
            date: "2025-7-6"
        },
        {
            name: "トロ鯖缶",
            count: 3,
            date: "2025-7-5"
        }
    ];

    const survivalDate = 3;

    const ItemList = ({ condition, items, bg }) => {
        return (
            condition && items.map(item => {
                return (
                    <div key={item.name} style={{ backgroundColor: bg, color: 'white', borderRadius: '0.5em', padding: '.5em 2em' }}>
                        <p style={{ textAlign: 'center', fontWeight: 'bold' }}>{item.name}</p>
                        <div style={{ display: 'flex', gap: '1em' }}>
                            <p>x{item.count}</p>
                            <p>{item.date}</p>
                        </div>
                    </div>
                );
            })
        );

    };

    return (
        <>
            <h1 className='text-gray'>今日の伝言板</h1>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <h1 className='text-gray'>あなたの備蓄</h1>
                <h2 className='text-gray' style={{ backgroundColor: '#D9D9D9', padding: '.5em 1em', borderRadius: '1em' }}>{survivalDate}日間持つ</h2>
            </div>
            <div onClick={() => setTimeout(prev => !prev)} style={{ display: 'flex', alignItems: 'center', gap: '0.5em' }} className='text-gray unselectable-text'>
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 18 18" fill="none">
                    <g filter="url(#filter0_iii_1_364)">
                        <path d="M15.8926 8.96216C15.8926 13.0698 12.5627 16.3997 8.45508 16.3997C4.34746 16.3997 1.01758 13.0698 1.01758 8.96216C1.01758 4.85454 4.34746 1.52466 8.45508 1.52466C12.5627 1.52466 15.8926 4.85454 15.8926 8.96216Z" fill="url(#paint0_linear_1_364)" />
                    </g>
                    <g filter="url(#filter1_f_1_364)">
                        <path d="M3.14258 8.43091C3.14258 8.1375 3.38043 7.89966 3.67383 7.89966H13.2363C13.5297 7.89966 13.7676 8.1375 13.7676 8.43091V9.49341C13.7676 9.78682 13.5297 10.0247 13.2363 10.0247H3.67383C3.38043 10.0247 3.14258 9.78682 3.14258 9.49341V8.43091Z" fill="#FF4D76" />
                    </g>
                    <g filter="url(#filter2_i_1_364)">
                        <path d="M3.14258 8.43091C3.14258 8.1375 3.38043 7.89966 3.67383 7.89966H13.2363C13.5297 7.89966 13.7676 8.1375 13.7676 8.43091V9.49341C13.7676 9.78682 13.5297 10.0247 13.2363 10.0247H3.67383C3.38043 10.0247 3.14258 9.78682 3.14258 9.49341V8.43091Z" fill="#F6EEFF" />
                    </g>
                    <defs>
                        <filter id="filter0_iii_1_364" x="0.805078" y="1.25903" width="15.3531" height="15.3531" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
                            <feFlood flood-opacity="0" result="BackgroundImageFix" />
                            <feBlend mode="normal" in="SourceGraphic" in2="BackgroundImageFix" result="shape" />
                            <feColorMatrix in="SourceAlpha" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0" result="hardAlpha" />
                            <feOffset dx="-0.2125" dy="0.2125" />
                            <feGaussianBlur stdDeviation="0.132812" />
                            <feComposite in2="hardAlpha" operator="arithmetic" k2="-1" k3="1" />
                            <feColorMatrix type="matrix" values="0 0 0 0 1 0 0 0 0 0.466667 0 0 0 0 0.666667 0 0 0 1 0" />
                            <feBlend mode="normal" in2="shape" result="effect1_innerShadow_1_364" />
                            <feColorMatrix in="SourceAlpha" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0" result="hardAlpha" />
                            <feOffset dx="0.345312" />
                            <feGaussianBlur stdDeviation="0.132812" />
                            <feComposite in2="hardAlpha" operator="arithmetic" k2="-1" k3="1" />
                            <feColorMatrix type="matrix" values="0 0 0 0 0.784314 0 0 0 0 0.160784 0 0 0 0 0.34902 0 0 0 1 0" />
                            <feBlend mode="normal" in2="effect1_innerShadow_1_364" result="effect2_innerShadow_1_364" />
                            <feColorMatrix in="SourceAlpha" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0" result="hardAlpha" />
                            <feOffset dy="-0.345312" />
                            <feGaussianBlur stdDeviation="0.132812" />
                            <feComposite in2="hardAlpha" operator="arithmetic" k2="-1" k3="1" />
                            <feColorMatrix type="matrix" values="0 0 0 0 0.913725 0 0 0 0 0.121569 0 0 0 0 0.309804 0 0 0 1 0" />
                            <feBlend mode="normal" in2="effect2_innerShadow_1_364" result="effect3_innerShadow_1_364" />
                        </filter>
                        <filter id="filter1_f_1_364" x="2.61133" y="7.36841" width="11.6875" height="3.1875" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
                            <feFlood flood-opacity="0" result="BackgroundImageFix" />
                            <feBlend mode="normal" in="SourceGraphic" in2="BackgroundImageFix" result="shape" />
                            <feGaussianBlur stdDeviation="0.265625" result="effect1_foregroundBlur_1_364" />
                        </filter>
                        <filter id="filter2_i_1_364" x="2.87695" y="7.89966" width="10.8906" height="2.39062" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
                            <feFlood flood-opacity="0" result="BackgroundImageFix" />
                            <feBlend mode="normal" in="SourceGraphic" in2="BackgroundImageFix" result="shape" />
                            <feColorMatrix in="SourceAlpha" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0" result="hardAlpha" />
                            <feOffset dx="-0.265625" dy="0.265625" />
                            <feGaussianBlur stdDeviation="0.265625" />
                            <feComposite in2="hardAlpha" operator="arithmetic" k2="-1" k3="1" />
                            <feColorMatrix type="matrix" values="0 0 0 0 0.905882 0 0 0 0 0.858824 0 0 0 0 0.980392 0 0 0 1 0" />
                            <feBlend mode="normal" in2="shape" result="effect1_innerShadow_1_364" />
                        </filter>
                        <linearGradient id="paint0_linear_1_364" x1="8.45508" y1="2.88599" x2="8.45508" y2="16.3997" gradientUnits="userSpaceOnUse">
                            <stop stop-color="#FE4E8E" />
                            <stop offset="1" stop-color="#FF4C57" />
                        </linearGradient>
                    </defs>
                </svg>
                <h3>期限切れ</h3>
                <p>{fakeData.length}個</p>
                <svg style={{ transform: `${timeout ? 'rotate(0)' : 'rotate(-90deg)'}`, transitionProperty: 'transform', transitionDuration: '200ms' }} xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="#50b4aa" viewBox="0 0 256 256"><path d="M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm45.66,93.66-40,40a8,8,0,0,1-11.32,0l-40-40a8,8,0,0,1,11.32-11.32L128,140.69l34.34-34.35a8,8,0,0,1,11.32,11.32Z"></path></svg>
            </div>
            <div style={{ display: 'flex', gap: '2em', }}>
                <ItemList condition={timeout} items={fakeData} bg={'#d34d4d'} />
            </div>
            <div onClick={() => setOneWeek(prev => !prev)} style={{ display: 'flex', alignItems: 'center', gap: '0.5em' }} className='text-gray unselectable-text'>
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 18 18" fill="none">
                    <g clip-path="url(#clip0_1_1127)">
                        <g filter="url(#filter0_iii_1_1127)">
                            <path d="M7.76507 4.18884L1.03942 15.8392C0.768486 16.312 1.10849 16.907 1.65567 16.907H15.1069C15.6541 16.907 15.9941 16.3173 15.7232 15.8392L8.99757 4.18884C8.72132 3.71603 8.04132 3.71603 7.76507 4.18884Z" fill="url(#paint0_linear_1_1127)" />
                        </g>
                        <g filter="url(#filter1_i_1_1127)">
                            <path d="M7.6377 12.4967C7.6377 12.9057 7.96707 13.2404 8.38145 13.2404C8.79582 13.2404 9.1252 12.9057 9.1252 12.4913V7.6251C9.1252 7.21603 8.79582 6.88135 8.38145 6.88135C7.97238 6.88135 7.6377 7.21072 7.6377 7.6251V12.4967Z" fill="#4A4351" />
                            <path d="M9.1252 14.6109C9.1252 15.0217 8.79221 15.3547 8.38145 15.3547C7.97068 15.3547 7.6377 15.0217 7.6377 14.6109C7.6377 14.2002 7.97068 13.8672 8.38145 13.8672C8.79221 13.8672 9.1252 14.2002 9.1252 14.6109Z" fill="#4A4351" />
                        </g>
                    </g>
                    <defs>
                        <filter id="filter0_iii_1_1127" x="0.705273" y="3.62173" width="15.4318" height="13.2853" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
                            <feFlood flood-opacity="0" result="BackgroundImageFix" />
                            <feBlend mode="normal" in="SourceGraphic" in2="BackgroundImageFix" result="shape" />
                            <feColorMatrix in="SourceAlpha" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0" result="hardAlpha" />
                            <feOffset dx="-0.239063" />
                            <feGaussianBlur stdDeviation="0.159375" />
                            <feComposite in2="hardAlpha" operator="arithmetic" k2="-1" k3="1" />
                            <feColorMatrix type="matrix" values="0 0 0 0 1 0 0 0 0 0.996078 0 0 0 0 0.458824 0 0 0 1 0" />
                            <feBlend mode="normal" in2="shape" result="effect1_innerShadow_1_1127" />
                            <feColorMatrix in="SourceAlpha" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0" result="hardAlpha" />
                            <feOffset dx="0.31875" dy="-0.2125" />
                            <feGaussianBlur stdDeviation="0.2125" />
                            <feComposite in2="hardAlpha" operator="arithmetic" k2="-1" k3="1" />
                            <feColorMatrix type="matrix" values="0 0 0 0 0.929412 0 0 0 0 0.411765 0 0 0 0 0.313726 0 0 0 1 0" />
                            <feBlend mode="normal" in2="effect1_innerShadow_1_1127" result="effect2_innerShadow_1_1127" />
                            <feColorMatrix in="SourceAlpha" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0" result="hardAlpha" />
                            <feOffset dx="0.159375" />
                            <feGaussianBlur stdDeviation="0.159375" />
                            <feComposite in2="hardAlpha" operator="arithmetic" k2="-1" k3="1" />
                            <feColorMatrix type="matrix" values="0 0 0 0 0.737255 0 0 0 0 0.564706 0 0 0 0 0.239216 0 0 0 1 0" />
                            <feBlend mode="normal" in2="effect2_innerShadow_1_1127" result="effect3_innerShadow_1_1127" />
                        </filter>
                        <filter id="filter1_i_1_1127" x="7.23926" y="6.88135" width="1.88574" height="8.87183" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
                            <feFlood flood-opacity="0" result="BackgroundImageFix" />
                            <feBlend mode="normal" in="SourceGraphic" in2="BackgroundImageFix" result="shape" />
                            <feColorMatrix in="SourceAlpha" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0" result="hardAlpha" />
                            <feOffset dx="-0.398438" dy="0.398438" />
                            <feGaussianBlur stdDeviation="0.31875" />
                            <feComposite in2="hardAlpha" operator="arithmetic" k2="-1" k3="1" />
                            <feColorMatrix type="matrix" values="0 0 0 0 0.180392 0 0 0 0 0.145098 0 0 0 0 0.223529 0 0 0 1 0" />
                            <feBlend mode="normal" in2="shape" result="effect1_innerShadow_1_1127" />
                        </filter>
                        <linearGradient id="paint0_linear_1_1127" x1="8.38132" y1="3.83423" x2="8.38132" y2="16.907" gradientUnits="userSpaceOnUse">
                            <stop stop-color="#FFD758" />
                            <stop offset="1" stop-color="#FFA956" />
                        </linearGradient>
                        <clipPath id="clip0_1_1127">
                            <rect width="17" height="17" fill="white" transform="translate(0.0927734 0.737549)" />
                        </clipPath>
                    </defs>
                </svg>
                <h3>あと一週間</h3>
                <p>{fakeData.length}個</p>
                <svg style={{ transform: `${oneWeek ? 'rotate(0)' : 'rotate(-90deg)'}`, transitionProperty: 'transform', transitionDuration: '200ms' }} xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="#50b4aa" viewBox="0 0 256 256"><path d="M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm45.66,93.66-40,40a8,8,0,0,1-11.32,0l-40-40a8,8,0,0,1,11.32-11.32L128,140.69l34.34-34.35a8,8,0,0,1,11.32,11.32Z"></path></svg>
            </div>
            <div style={{ display: 'flex', gap: '2em', }}>
                <ItemList condition={oneWeek} items={fakeData2} bg={'#ffb056'} />
            </div>
        </>
    );
}
