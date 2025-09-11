from flask import jsonify, request

def register_mypage_routes(app, SessionLocal, Families, Users, Items):
    @app.get("/api/mypage/summary")
    def get_mypage_summary():
        user_id = request.args.get("user_id", type=int, default=1)
        with SessionLocal() as s:
            user = s.get(Users, user_id)
            if not user:
                return jsonify({"error": "user not found"}), 404

            family_id = user.family_id
            family_member_count = 1
            if family_id:
                family = s.get(Families, family_id)
                if family and (family.kids is not None or family.adults is not None):
                    family_member_count = (family.kids or 0) + (family.adults or 0)
                else:
                    family_member_count = s.query(Users).filter(Users.family_id == family_id).count()

            username = f"{(user.lastname or '').strip()} {(user.firstname or '').strip()}".strip()

            return jsonify({
                "username": username,
                "user_id": user.id,
                "family_id": family_id,
                "family_member_count": family_member_count
            })