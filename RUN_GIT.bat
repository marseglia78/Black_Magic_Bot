git init
git add .
git commit -m "commit"
#git remote add origin https://github.com/marseglia78/Black_Magic_Bot.git
git remote -v
git push origin master
heroku logs --tail -a black-magic-bot