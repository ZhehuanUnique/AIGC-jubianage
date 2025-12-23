#!/bin/bash
# RAG API 测试脚本

BASE_URL="http://localhost:8001"

echo "=========================================="
echo "RAG API 测试脚本"
echo "=========================================="
echo ""

# 1. 健康检查
echo "1. 测试健康检查接口..."
curl -s "$BASE_URL/health" | python3 -m json.tool
echo ""
echo ""

# 2. 获取统计信息
echo "2. 获取统计信息..."
curl -s "$BASE_URL/api/v1/rag/stats" | python3 -m json.tool
echo ""
echo ""

# 3. 上传视频（如果有视频文件）
if [ -f "../index.mp4" ]; then
    echo "3. 上传视频 (index.mp4)..."
    curl -X POST "$BASE_URL/api/v1/rag/video/upload" \
        -F "file=@../index.mp4" \
        -F "video_id=test_video_$(date +%s)" \
        -F "method=interval" \
        -F "interval_seconds=2.0" | python3 -m json.tool
    echo ""
    echo ""
fi

# 4. 文本搜索
echo "4. 测试文本搜索..."
curl -s -X POST "$BASE_URL/api/v1/rag/search" \
    -H "Content-Type: application/json" \
    -d '{"query": "视频画面", "n_results": 3}' | python3 -m json.tool
echo ""
echo ""

# 5. 提示词增强
echo "5. 测试提示词增强..."
curl -s -X POST "$BASE_URL/api/v1/rag/enhance-prompt" \
    -H "Content-Type: application/json" \
    -d '{"prompt": "一个快速移动的镜头", "n_references": 2}' | python3 -m json.tool
echo ""
echo ""

# 6. 再次获取统计信息
echo "6. 获取更新后的统计信息..."
curl -s "$BASE_URL/api/v1/rag/stats" | python3 -m json.tool
echo ""
echo ""

echo "=========================================="
echo "测试完成！"
echo "=========================================="


