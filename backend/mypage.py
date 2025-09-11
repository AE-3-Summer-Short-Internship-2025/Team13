"""
提供エンドポイント:
GET /api/mypage/summary?user_id=<int>

成功時の返り値:
- name       : Users.lastname + " " + Users.firstname（前後空白はトリム）
- user_id    : Users.id
- family_id  : Users.family_id（無い場合は null）
- adult_num  : Families.adults（無い/None は 0）
- child_num  : Families.kids（無い/None は 0）

エラー時の返り値（統一フォーマット）:
{ "error": { "code": "<CODE>", "message": "<説明>", "details": <任意> } }
"""
from typing import Optional, Union
from flask import jsonify, request
from sqlalchemy.exc import SQLAlchemyError


def register_mypage_routes(app, Families, Users):
    # 統一エラーレスポンス
    def error_response(
        code: str,
        message: str,
        http_status: int,
        details: Optional[Union[dict, str]] = None
    ):
        payload = {"error": {"code": code, "message": message}}
        if details is not None:
            payload["error"]["details"] = details
        return jsonify(payload), http_status

    @app.get("/api/mypage/summary")
    def get_mypage_summary():
        """
        指定ユーザーのサマリーを返す（表示用の取得API）。
        クエリ: ?user_id=<int>（暫定。将来は認証でサーバ側特定に置換）
        """
        # 1) user_id の厳密検証（無効値は 400）
        raw_user_id = request.args.get("user_id", default="1")
        try:
            user_id = int(raw_user_id)
        except (ValueError, TypeError):
            return error_response(
                code="INVALID_USER_ID",
                message="user_id must be an integer",
                http_status=400,
                details={"received": raw_user_id}
            )

        try:
            # 2) ユーザー取得（無ければ 404）
            user = Users.query.get(user_id)
            if not user:
                return error_response(
                    code="USER_NOT_FOUND",
                    message="user not found",
                    http_status=404,
                    details={"user_id": user_id}
                )

            # 3) 家族情報取得＆人数
            family_id = user.family_id
            adult_num = 0
            child_num = 0
            if family_id is not None:
                family = Families.query.get(family_id)
                if family:
                    adult_num = family.adults or 0
                    child_num = family.kids or 0

            # 4) ユーザー名整形（姓 名）
            lastname = (user.lastname or "").strip()
            firstname = (user.firstname or "").strip()
            name = f"{lastname} {firstname}".strip()

            # 5) 正常レスポンス
            return jsonify({
                "name": name,
                "user_id": user.id,
                "family_id": user.family_id,
                "adult_num": adult_num,
                "child_num": child_num
            }), 200

        except SQLAlchemyError as e:
            return error_response(
                code="DB_ERROR",
                message="database error",
                http_status=500,
                details=str(e)
            )

        except Exception as e:
            return error_response(
                code="INTERNAL_ERROR",
                message="unexpected error",
                http_status=500,
                details=str(e)
            )