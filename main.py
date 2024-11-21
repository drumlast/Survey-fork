from app import create_app, db
from app.database import import_survey_data, import_iogv_data
from app.models import create_admin_user

app = create_app()

with app.app_context():
    db.create_all()
    with open("app/static/json/surveyv2.json", "r", encoding="utf-8") as file:
        data = file.read()
        import_survey_data(data)

    with open("app/static/json/iogv.json", "r", encoding="utf-8") as file:
        data = file.read()
        import_iogv_data(data)
    create_admin_user()

if __name__ == '__main__':
    app.run(debug=True)
