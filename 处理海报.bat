@echo off
chcp 65001 >nul
echo ========================================
echo 海报导入和处理工具
echo ========================================
echo.

echo [1/2] 导入桌面 Posters 文件夹中的图片...
python import_posters.py
echo.

echo [2/2] 更新 index.html...
python update_index_html.py
echo.

echo ========================================
echo 处理完成！
echo ========================================
echo.
pause

