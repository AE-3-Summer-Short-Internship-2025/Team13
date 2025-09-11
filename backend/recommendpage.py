from flask import Blueprint, jsonify
from datetime import datetime, timedelta
import requests
import time

from app import db, Items 

# 'recommend_api' という名前でBlueprintオブジェクトを作成
recommend_api = Blueprint('recommend_api', __name__)

# 必須防災グッズのチェックリスト
ESSENTIAL_CHECKLIST = [
    "非常食・飲料水", "割りばし・紙皿・紙コップ", "ラップ・アルミホイル", "ヘルメット・防災ずきん",
    "万能ナイフ", "常備薬", "体温計", "ビニールシート", "アルミブランケット",
    "携帯充電器・モバイルバッテリー", "携帯ラジオ", "ヘッドライト・乾電池", "ライター・マッチ",
    "使い捨てカイロ", "ビニール袋・ごみ袋", "ウェットタオル・体拭きシート",
    "マウスウォッシュ・ドライシャンプー", "マスク・消毒液", "ビニール手袋",
    "ティッシュペーパー・トイレットペーパー", "生理用品", "防寒着・雨具", "スリッパ",
    "軍手・皮手袋", "ハンカチ・タオル", "簡易トイレ", "カセットコンロ・ガスボンベ",
    "クーラーボックス・保冷剤", "ポリタンク", "鍋・水筒", "毛布・寝袋", "下着・靴下・着替え"
]

def search_rakuten_for_recommendations(keyword):
    """
    指定されたキーワードで楽天の商品を検索し、おすすめリストを返すヘルパー関数
    """
    REQUEST_URL = 'https://app.rakuten.co.jp/services/api/IchibaItem/Search/20240222'
    APP_ID = '1088027222225008171' 
    params = {
        'applicationId': APP_ID, 'format': 'json', 'keyword': keyword,
        'hits': 3, 'sort': 'standard'
    }
    try:
        time.sleep(1)
        res = requests.get(REQUEST_URL, params=params)
        res.raise_for_status()
        result = res.json()
        if not result.get("Items"): return []

        recommendations = []
        for item in result['Items']:
            item_data = item['Item']
            image_url = (item_data.get('mediumImageUrls', [{}])[0].get('imageUrl') 
                         if item_data.get('mediumImageUrls') else None)
            recommendations.append({
                'itemName': item_data.get('itemName'), 'itemPrice': item_data.get('itemPrice'),
                'itemUrl': item_data.get('itemUrl'), 'imageUrl': image_url
            })
        return recommendations
    except requests.exceptions.RequestException as e:
        print(f"楽天API検索エラー (キーワード: {keyword}): {e}")
        return []

@recommend_api.route("/api/insufficient_items")
def get_insufficient_items():
    """
    不足している防災グッズと、その代替となる楽天おすすめ商品リストを返すAPI
    """
    owned_items = Items.query.filter_by(is_grocery=False).all()
    owned_item_names = [item.item_name for item in owned_items]

    covered_checklist_items = set()
    for checklist_item in ESSENTIAL_CHECKLIST:
        keywords = checklist_item.replace('・', ' ').split()
        
        for owned_name in owned_item_names:
            if any(keyword in owned_name for keyword in keywords):
                covered_checklist_items.add(checklist_item)
                break
    
    missing_items_names = set(ESSENTIAL_CHECKLIST) - covered_checklist_items
    
    preparedness_percentage = 0
    if len(ESSENTIAL_CHECKLIST) > 0:
        preparedness_percentage = round((len(covered_checklist_items) / len(ESSENTIAL_CHECKLIST)) * 100)

    missing_items_with_recs = []
    for item_name in sorted(list(missing_items_names)):
        recommendations = search_rakuten_for_recommendations(f"防災 {item_name}")
        missing_items_with_recs.append({
            "missing_item_name": item_name,
            "recommendations": recommendations
        })

    return jsonify({
        "insufficient_items": missing_items_with_recs,
        "preparedness_percentage": preparedness_percentage
    })

@recommend_api.route("/api/recommendations")
def get_recommendations():
    """
    期限切れ・期限間近の食品と、その代替となる楽天おすすめ商品リストを返すAPI
    """
    today = datetime.now().date()
    one_week_later = today + timedelta(days=7)

    expiring_soon_items = Items.query.filter(
        Items.is_grocery == True, Items.date_expiry != None,
        db.func.date(Items.date_expiry) >= today,
        db.func.date(Items.date_expiry) <= one_week_later
    ).all()

    expired_items = Items.query.filter(
        Items.is_grocery == True, Items.date_expiry != None,
        db.func.date(Items.date_expiry) < today
    ).all()

    response_data = { "expiring_soon": [], "expired": [] }

    for item in expiring_soon_items:
        recs = search_rakuten_for_recommendations(item.item_name)
        response_data["expiring_soon"].append({
            "owned_item": {"id": item.id, "name": item.item_name, "expiry_date": item.date_expiry.strftime('%Y-%m-%d')},
            "recommendations": recs
        })

    for item in expired_items:
        recs = search_rakuten_for_recommendations(item.item_name)
        response_data["expired"].append({
            "owned_item": {"id": item.id, "name": item.item_name, "expiry_date": item.date_expiry.strftime('%Y-%m-%d')},
            "recommendations": recs
        })

    return jsonify(response_data)