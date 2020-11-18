find . -name '*.pyc' -delete
find . -name '*.pyo' -delete
find . -name '.DS_Store' -delete

# update info

git config --global credential.helper store

git add --all
git commit -m "coding"

git pull
git push