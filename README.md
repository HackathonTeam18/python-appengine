# HackathonTeam18  


# Test the application  
virtualenv venv  
venv\scripts\activate.bat  
pip install -r requirements.txt  
python main.py  


# Deploy the application  
gcloud app deploy --version=v1 ./app.yaml  