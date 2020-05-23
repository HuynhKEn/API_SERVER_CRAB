from back_end import app
from flask_ngrok import run_with_ngrok
run_with_ngrok(app)
app.run()