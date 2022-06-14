NEW_VERSION=$1

echo "curent path: $(pwd), change version to $NEW_VERSION"

git config --global user.name "$GITHUB_ACTOR-bot"
git config --global user.email "$GITHUB_ACTOR-bot@dongtai.io"
git checkout -b "release-$NEW_VERSION"

sed -i "s/<version_id>/$NEW_VERSION/g" ./deploy/docker-compose/README.MD
sed -i "s/<version_id>/$NEW_VERSION/g" ./deploy/docker-compose/README-zh.md

git add .
git commit -m "Update: change version to $NEW_VERSION"

git push "https://$GITHUB_ACTOR:$GITHUB_TOKEN@github.com/$GITHUB_REPOSITORY.git" HEAD:"release-$NEW_VERSION"
