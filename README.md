## 원본 EasyOCR 링크 => https://github.com/JaidedAI/EasyOCR

# EasyOCR Flask API
**EasyOCR**을 **Flask API**로 구현하여 외부에서 OCR 기능을 사용할 수 있도록 만들었음
- `OCRrun.py` 파일을 통해 EasyOCR을 Flask API로 제공
- 영수증이나 이미지에서 텍스트를 추출하고 결과를 API로 반환함

## 환경 설정
- **Python**: 3.10.14
- **pip list**: `ocrrequirements.txt`

### torch(2.0.1) + cuda(117)
```bash
pip install torch==2.0.1+cu117 torchvision==0.15.2+cu117 torchaudio==2.0.2+cu117 --index-url https://download.pytorch.org/whl/cu117
```

## 참고사항
- **docker 이미지로 업로드시** **torch**와 **cuda** 버전이 다르긴함 작동하는데는 문제 없음
- **docker-compse는** 다른 `process.py`와 `geo.py`를 **같이 사용할시** 사용
- geo.py => https://github.com/bestKUFO/geo_api
- process.py => https://github.com/DotBlossom/flask-api
- **여기에 파일 있음. 도커파일 포함 (Dockerfile.process, process.txt)**
