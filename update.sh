source venv/bin/activate
git pull
venv/bin/pip install --upgrade pip
venv/bin/pip install --ignore-installed -r requirements.txt
supervisorctl restart tools
deactivate
