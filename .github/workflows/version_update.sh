NEW_VERSION=$1

echo "curent path: $(pwd), change version to $NEW_VERSION"

git config --global user.name "$GITHUB_ACTOR"
git config --global user.email "$GITHUB_ACTOR@bot.noreplay.dongtai.io"
git checkout -b "release-$NEW_VERSION"

sed -i "s/:latest/:$NEW_VERSION/g" README.md
sed -i "s/:latest/:$NEW_VERSION/g" README_CN.md
sed -i "s/dongtai-mysql:latest/dongtai-mysql:$NEW_VERSION/g" .github/workflows/deploy_test.yml

git add .
git commit -m "Update: change version to $NEW_VERSION"

git push "https://$GITHUB_ACTOR:$GITHUB_TOKEN@github.com/$GITHUB_REPOSITORY.git" HEAD:"release-$NEW_VERSION"
