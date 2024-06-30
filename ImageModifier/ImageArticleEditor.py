import cv2
from PIL import Image
import numpy as np

def add_title_to_image(image_path, icon_path, position):
    pass

# article_type은
# Information, Breaking, Official, Tech, Rumor 다섯가지로
def add_basic_image(image_path, article_type):
    if article_type == "Information":
        icon_path = '../prefab/information_icon.png'
        line_path = '../prefab/information_line_440.png'
    elif article_type == "Breaking":
        icon_path = '../prefab/breaking_icon.png'
        line_path = '../prefab/breaking_line_440.png'
    elif article_type == "Official":
        icon_path = '../prefab/official_icon.png'
        line_path = '../prefab/official_line_440.png'
    elif article_type == "Tech":
        icon_path = '../prefab/tech_icon.png'
        line_path = '../prefab/tech_line_440.png'
    elif article_type == "Rumor":
        icon_path = '../prefab/rumor_icon.png'
        line_path = '../prefab/rumor_line_440.png'
    icon_position = (50, 700)  # (x, y)
    line_position = (50, 780)  # (x, y)

    image_with_icon = add_icon_to_image(image_path, icon_path, icon_position)
    output_path = '../after_processing_image/' + image_path + ".png"
    cv2.imwrite(output_path, image_with_icon)

    image_with_line = add_icon_to_image(output_path, line_path, line_position)
    output_path = '../after_processing_image/' + image_path + ".png"
    cv2.imwrite(output_path, image_with_line)


def add_icon_to_image(image_path, icon_path, position):
    """
    이미지에 특정 아이콘을 추가합니다.

    Parameters:
    - image_path: 기본 이미지 경로
    - icon_path: 추가할 아이콘 이미지 경로
    - position: 아이콘을 추가할 위치 (x, y)

    Returns:
    - 아이콘이 추가된 이미지
    """
    # 기본 이미지 로드 (OpenCV 사용)
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError(f"Image at path '{image_path}' not found.")

    # 아이콘 이미지 로드 (Pillow 사용)
    icon = Image.open(icon_path)
    if icon is None:
        raise FileNotFoundError(f"Icon at path '{icon_path}' not found.")

    # 기본 이미지를 Pillow 이미지로 변환
    image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # 아이콘 이미지의 크기 얻기
    icon_width, icon_height = icon.size

    # 아이콘을 추가할 위치 (x, y) 설정
    x, y = position

    # 아이콘을 기본 이미지에 붙여넣기
    image_pil.paste(icon, (x, y), icon.convert('RGBA'))

    # 결과 이미지를 다시 OpenCV 이미지로 변환
    result_image = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)

    return result_image


# 이미지 및 아이콘 경로
image_path = '../after_processing_image/processing_2.jpg'
icon_path = '../prefab/information_icon.png'
line_path = '../prefab/information_line_440.png'

# 아이콘을 추가할 위치
icon_position = (50, 700)  # (x, y)
line_position = (50, 780)  # (x, y)

# 아이콘이 추가된 이미지 얻기
image_with_icon = add_icon_to_image(image_path, icon_path, icon_position)
# 결과 저장
output_path = '../after_processing_image/processing_3.jpg'
cv2.imwrite(output_path, image_with_icon)

image_with_line = add_icon_to_image(output_path, line_path, line_position)
output_path = '../after_processing_image/processing_4.jpg'
cv2.imwrite(output_path, image_with_line)
