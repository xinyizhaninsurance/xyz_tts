#!/bin/bash

# 用你的实际值替换以下变量
DOCKER_REGISTRY_URL="替换为你的仓库URL"    # 替换为你的仓库URL
DOCKER_REGISTRY_USERNAME="替换为你的仓库用户名"   # 替换为你的仓库用户名
DOCKER_REGISTRY_PASSWORD="替换为你的仓库密码或访问令牌"     # 替换为你的仓库密码或访问令牌
IMAGE_NAME="xyz_tts"               # 替换为你的Docker镜像名称
PROJECT="替换为你的仓库的项目"

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
if ! docker login -u "$DOCKER_REGISTRY_USERNAME" -p "$DOCKER_REGISTRY_PASSWORD" "$DOCKER_REGISTRY_URL";then
    echo "登录到docker仓库失败"
  exit 1
fi

# 构建Docker镜像
echo "构建Docker镜像..."
docker build -t "$IMAGE_NAME:$IMAGE_TAG" .

# 使用仓库URL标记镜像
echo "给Docker镜像打上仓库URL的标签..."
docker tag "$IMAGE_NAME:$IMAGE_TAG" "$DOCKER_REGISTRY_URL/$PROJECT/$IMAGE_NAME:$IMAGE_TAG"

# 推送镜像到私有Docker仓库
echo "推送Docker镜像到私有仓库..."
docker push "$DOCKER_REGISTRY_URL/$PROJECT/$IMAGE_NAME:$IMAGE_TAG"

# 清理（可选）
echo "清理..."
docker logout "$DOCKER_REGISTRY_URL"

echo "镜像构建和推送过程完成！"
