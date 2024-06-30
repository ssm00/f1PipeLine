import cv2
from PIL import Image

def add_title_to_image(image_path, icon_path, position):
    pass



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
image_path = 'path/to/your/image.jpg'
icon_path = 'path/to/your/icon.png'

# 아이콘을 추가할 위치
position = (50, 50)  # (x, y)

# 아이콘이 추가된 이미지 얻기
image_with_icon = add_icon_to_image(image_path, icon_path, position)

# 결과 저장
output_path = 'path/to/output_image.jpg'
cv2.imwrite(output_path, image_with_icon)