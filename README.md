# install front-end
cd frontend
npm install
npm run build

# install back-end
(windows)
cd ../backend
python -m venv venv
venv/Scripts/activate.bat
pip install -r requirements.txt

# serve back-end at localhost:5000
set FLASK_APP=run.py
flask run