python -m pip install --upgrade pip

pip install PyInstaller
pip install -r requirements.txt

rm ./Windows_Deploy/ -Recurse -Force -Confirm:$false

mkdir ./Windows_Deploy/ExoTool_ControllerEdition

PyInstaller ExoTool_ControllerEdition.py --onefile --hidden-import glcontext

cp ./dist ./Windows_Deploy/ExoTool_ControllerEdition -Recurse
rm ./dist -Recurse -Force -Confirm:$false
cp ./build ./Windows_Deploy/ExoTool_ControllerEdition -Recurse
rm ./build -Recurse -Force -Confirm:$false
cp ./shaders ./Windows_Deploy/ExoTool_ControllerEdition/dist -Recurse

mkdir ./Windows_Deploy/ExoTool

PyInstaller ExoTool.py --onefile --hidden-import glcontext

cp ./dist ./Windows_Deploy/ExoTool -Recurse
rm ./dist -Recurse -Force -Confirm:$false
cp ./build ./Windows_Deploy/ExoTool -Recurse
rm ./build -Recurse -Force -Confirm:$false
cp ./shaders ./Windows_Deploy/ExoTool/dist -Recurse