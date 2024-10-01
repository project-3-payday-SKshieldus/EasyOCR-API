원본 EasyOCR 링크 : https://github.com/JaidedAI/EasyOCR

EasyOCR을 flask api로 외부에서 사용하게 만들었음. => OCRrun.py

Python 3.10.14 버전

pip install torch==2.0.1+cu117 torchvision==0.15.2+cu117 torchaudio==2.0.2+cu117 --index-url https://download.pytorch.org/whl/cu117
#docker 이미지로 업로드시 torch와 cuda 버전이 다르긴함 작동하는데는 문제 없음

추가적인 pip list는 ocrrequirements.txt 참조

docker-compse는 다른 process.py와 geo.py를 같이 사용할시 사용

#geo.py => https://github.com/bestKUFO/geo_api

#process.py => https://github.com/DotBlossom/flask-api
여기에 파일 있음. 도커파일 포함 (Dockerfile.process, process.txt)
