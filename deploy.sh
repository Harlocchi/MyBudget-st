#!/bin/bash

APP_NAME="budgetlab-app"
PORT="8501"

echo "🔴 Parando container..."
docker stop $APP_NAME
docker rm $APP_NAME

echo "📥 Atualizando projeto com git pull..."
git pull

echo "🔧 Gerando nova imagem Docker..."
docker build -t $APP_NAME .

echo "🚀 Subindo container em segundo plano..."
docker run -d -p $PORT:8501 --name $APP_NAME $APP_NAME

echo "✅ Deploy finalizado!"
