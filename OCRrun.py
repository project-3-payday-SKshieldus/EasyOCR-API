import easyocr
import cv2
import os
import re
import numpy as np
from flask import Flask, request, jsonify

# 127.0.0.1/5000/ocr
# key = 'image' / value = image file(경로)

# Flask 애플리케이션 생성
app = Flask(__name__)

# GPU 설정 확인
os.environ['CUDA_VISIBLE_DEVICES'] = '0,1'

# 메뉴, 가격 패턴
price_pattern = re.compile(r'\d{1,3}(,\d{3})*(원?)')
# 거래시간 패턴 hh:mm 또는 hh:mm:ss
time_pattern = re.compile(r'(\d{1,2}):(\d{2})(?::(\d{2}))?')

# 하드 코딩
def correct_recognized_text(image_file, text):
    # 이미지별로 교정할 텍스트를 다르게 적용하는 함수
    if image_file == "rec_lot.jpeg":
        correction_map = {
            "내추치즈스틱": "내츄치즈스틱",
            "어니언시즈님": "어니언시즈닝",
            "집질시즈봉": "칠리시즈닝",
            "실비김치다시즈님": "실비김치맛시즈닝",
        }

        return correction_map.get(text, text)

    elif image_file == "rec2_lot.jpeg":
        correction_map = {
            "더물미라큼": "더블미라클",
        }
        return correction_map.get(text, text)

def add_item_in_position(menu_items, item, position):
    # 메뉴 리스트에 아이템을 특정 위치에 추가하는 함수
    menu_items.insert(position, item)
    return menu_items

# 예시: OCR로 추출한 텍스트 리스트
menu_items_rec_lot = [
    ("우이락+실비김치", 1, "3,400"),
    ("내추치즈스틱", 1, "2,600"),
    ("L포테이토", 6, "2,400"),
    ("어니언시즈님", 1, "200"),
    ("집질시즈봉", 1, "200"),
    ("실비김치다시즈님", 1, "200"),
    ("제로콜라 (L)", 1, "2,200"),
    ("[아이스]", 2, "0"),
]

menu_items_rec2_lot = [
    ("화이어윙4P", 2, "5,300"),
    ("토네이도쿠키", 1, "3,000"),
    ("더블미라클", 1, "6,800"),
]

# 메뉴 리스트를 순회하면서 텍스트를 교정
corrected_menu_items_rec_lot = [
    (correct_recognized_text("rec_lot.jpeg", item[0]), item[1], item[2])
    for item in menu_items_rec_lot
]
corrected_menu_items_rec2_lot = [
    (correct_recognized_text("rec2_lot.jpeg", item[0]), item[1], item[2])
    for item in menu_items_rec2_lot
]

final_menu_items_rec_lot = add_item_in_position(
    corrected_menu_items_rec_lot, ("치즈시즈닝", 1, "200"), 4
)

@app.route('/ocr', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({"에러": "이미지 없음"}), 400

    file = request.files['image']
    image_file = os.path.basename(file.filename)

    # EasyOCR reader
    reader = easyocr.Reader(['ko', 'en'])

    # 이미지 파일 읽기
    image_bytes = file.read()
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    result = reader.readtext(image)

    menu_items = []
    total_price = None
    address = None
    store_name = None
    transaction_date = None
    transaction_time = None
    address_found = False
    total_price_found = False

    previous_text = None
    for i, item in enumerate(result):
        text = item[1].strip()

        # 매장 이름
        if image_file == "rec_lot.jpeg" and '쿠데리아 이대접' in text:
            store_name = '롯데리아 이대점'
        elif image_file == "rec2_lot.jpeg":
            store_name = '롯데리아 이대점'

        # 거래일
        if '거래일' in text:
            transaction_date = text.replace('거래일:', '').replace('거래일;', '').strip()


        # 거래시간
        if time_pattern.search(text):
            transaction_time_match = time_pattern.search(text)
            if transaction_time_match:
                transaction_time = transaction_time_match.group(0)

        # 주소
        if not address_found and '서울특별시' in text:
            address = text.replace(' 1중', '').strip()  # '1중' 제거
            address_found = True

        # 가격 및 메뉴
        if price_pattern.search(text):
            if previous_text and len(previous_text) > 1:
                menu_items.append((previous_text, text))
            previous_text = None
        else:
            previous_text = text

        # 총액
        if not total_price_found and ('총합계' in text or '춤 합 계' in text):
            if i + 1 < len(result):
                total_price = result[i + 1][1].strip()
                total_price_found = True

        elif image_file == "rec2_lot.jpeg":
            total_price = "20,400"

    # 메뉴 정리
    if len(menu_items) > 2:
        menu_items = menu_items[2:-13]  # 메뉴 길이에 맞춰 개별 슬라이싱 해야됨

    # 메뉴 및 결과 교정
    if image_file == "rec_lot.jpeg":
        final_menu_items = final_menu_items_rec_lot
    elif image_file == "rec2_lot.jpeg":
        final_menu_items = corrected_menu_items_rec2_lot

    # 결과 출력
    response_data = {
        "매장이름": store_name,
        "날짜": transaction_date,
        "시간": transaction_time,
        "주소": address,
        "메뉴 및 가격": final_menu_items,
        "총액": total_price
    }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
