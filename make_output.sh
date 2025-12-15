#!/bin/bash
#chmod +x make_output.sh && ./make_output.sh

# 建立 output 資料夾（若不存在）
if [ ! -d "output" ]; then
    mkdir output
    echo "output built"
else
    echo "output exist"
fi

# 檢查並建立資料夾
for dir in OutputVideos GaitSilhouette GaitFeatures; do
    if [ ! -d "output/$dir" ]; then
        mkdir "output/$dir"
        echo "output/$dir built"
    else
        echo "output/$dir exist"
    fi
done

echo "finished"
