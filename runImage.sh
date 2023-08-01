#!/bin/bash

# 用你的实际值替换以下变量
DOCKER_REGISTRY_URL="替换为你的仓库URL"    # 替换为你的仓库URL
DOCKER_REGISTRY_USERNAME="替换为你的仓库用户名"   # 替换为你的仓库用户名
DOCKER_REGISTRY_PASSWORD="替换为你的仓库密码或访问令牌"     # 替换为你的仓库密码或访问令牌
IMAGE_NAME="xyz_tts"               # 替换为你的Docker镜像名称
PROJECT="替换为你的仓库的项目"
CONTAINER_NAME="xyz_tts"

# 检查参数是否提供
if [ -z "$1" ]; then
  echo "错误：未提供镜像标签作为参数。"
  echo "使用方法：$0 <镜像标签>"
  exit 1
fi

# 获取传入的镜像标签参数
IMAGE_TAG="$1"

# 登录到私有Docker仓库
echo "登录到Docker仓库..."
if ! docker login -u "$DOCKER_REGISTRY_USERNAME" -p "$DOCKER_REGISTRY_PASSWORD" "$DOCKER_REGISTRY_URL"; then
  echo "登录到docker仓库失败"
  exit 1
fi

# 拉取Docker镜像
echo "拉取Docker镜像..."
if docker pull "$DOCKER_REGISTRY_URL/$PROJECT/$IMAGE_NAME:$IMAGE_TAG"; then
  # 运行Docker容器
  echo "运行Docker容器..."
  docker stop "$CONTAINER_NAME"
  docker rm "$CONTAINER_NAME"
  if ! docker run -d -v /etc/localtime:/etc/localtime:ro --name "$CONTAINER_NAME" -p 2020:2020 "$DOCKER_REGISTRY_URL/$PROJECT/$IMAGE_NAME:$IMAGE_TAG"; then
    echo "Docker容器运行成功！"
    exit 1
  fi
else
  echo "错误：未找到镜像 $DOCKER_REGISTRY_URL/$PROJECT/$IMAGE_NAME:$IMAGE_TAG。"
fi
