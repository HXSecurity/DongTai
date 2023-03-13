git config --global user.name "$GITHUB_ACTOR-bot"
git config --global user.email "$GITHUB_ACTOR-bot@dongtai.io"

cp -r dongtai_conf/conf/config.ini.example deploy/docker-compose/config-tutorial.ini

git add .
git commit -m "Update: change config file"

git push "https://$GITHUB_ACTOR:$GITHUB_TOKEN@github.com/$GITHUB_REPOSITORY.git"
