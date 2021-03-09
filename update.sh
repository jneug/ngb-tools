source venv/bin/activate
git pull
venv/bin/pip install --upgrade pip
venv/bin/pip install -r requirements.txt
supervisorctl restart tools
deactivate
