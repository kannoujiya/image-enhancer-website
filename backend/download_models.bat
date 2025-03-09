@echo off
echo Downloading RealESRGAN model...
curl -o backend\models\RealESRGAN_x4plus.pth "https://drive.google.com/file/d/1X1oLnl5vgtdVzxLGSxGUW_YjkOjalwna/view?usp=drive_link"

echo Downloading GFPGAN model...
curl -o backend\models\GFPGANv1.3.pth "https://drive.google.com/file/d/1ySSattZX_NUDMEq_7ntVeHfrQg_hemaO/view?usp=drive_link"

echo Models downloaded successfully.