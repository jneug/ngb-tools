source venv/bin/activate
git pull
pip install --ignore-installed -r requirements.txt
supervisorctl restart tools
