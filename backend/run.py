from api import create_app
from settings import TEST_DB_NAME, TEST_DB_USER, TEST_DB_PASSWORD

app = create_app(TEST_DB_NAME, TEST_DB_USER, TEST_DB_PASSWORD)

app.run(debug = True)
