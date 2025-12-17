#!/bin/bash
echo "================================"
echo "🚀 開始清理舊的步態輸出檔案..."

# cd All-in-one-Gait/OpenGait
# ./clean.sh

rm -rf ./output/GaitFeatures/*
rm -rf ./output/GaitSilhouette/*
rm -rf ./output/OutputVideos/*

echo "🧹 清理完成！舊的步態輸出檔案已刪除。"
echo "================================"