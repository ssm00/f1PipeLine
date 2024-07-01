import cv2
import numpy as np
import os
from PIL import Image, ImageDraw, ImageFont

font_path = "../prefab/SB_Window_Font/SB_agro_M.ttf"

def add_title_to_image(image_path, icon_path, position):
    pass

def add_icon_to_image(image_path, icon_path, position):
    """
    이미지에 아이콘을 추가

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

# article_type은
# Information, Breaking, Official, Tech, Rumor 다섯가지로
def add_basic_icon_to_image(image_path, article_type):
    image_name = os.path.splitext(os.path.basename(image_path))[0]
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
    output_path = '../after_processing_image/' + image_name + ".png"
    cv2.imwrite(output_path, image_with_icon)

    image_with_line = add_icon_to_image(output_path, line_path, line_position)
    output_path = '../after_processing_image/' + image_name + ".png"
    cv2.imwrite(output_path, image_with_line)

def resize_image(image_path):
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    h, w = image.shape[:2]
    target_size = (1080, 1350)
    target_height = target_size[1]
    target_width = target_size[0]
    proportion_h = target_size[1] / h
    proportion_w = target_size[0] / w
    # 먼저 가로 세로 중 작은 부분을 target_size에 맞게 사진을 늘려야함
    # 가로나 세로중 하나를 항상 기준으로 하면 크기가 큰 사진이 줄어드는 경우 가로 세로중 더 짧은 쪽은 검정 target보다 작아 공백이 되는 경우가 발생할 수 있음. 케이스 분리필요함
    # 가로가 긴 사진인 경우
    if w > h:
        # 세로를 정해진 비율 만큼 늘리거나 줄이기 가로는 어차피 target_w 넘어감
        new_height = target_height + 100
        new_width = int(proportion_h * w)
        resized_image = cv2.resize(image, (new_width, new_height))
        # 사진 스타트 포인트 구하기 (new_width / 2) - (target_with / 2) = (new_width - target_width) / 2
        start_x = (new_width - target_width) // 2
        # 세로 전체, 가로는 start_x 부터 start_x + target_width 까지
        resized_cropped_image = resized_image[100:new_height, start_x: start_x + target_width]
    # 세로가 긴 사진인 경우
    else:
        # 가로를 정해진 비율 만큼 늘리거나 줄이기 세로는 어차피 target_h 넘어감
        new_height = int(proportion_w * h)
        new_width = target_width
        resized_image = cv2.resize(image, (new_width, new_height))
        # 사진 스타트 포인트 구하기 (new_width / 2) - (target_with / 2) = (new_width - target_width) / 2
        start_y = (new_height - target_height) // 2
        # 세로 전체, 가로는 start_x 부터 start_x + target_width 까지
        # 사진은 0,0 이 우상단임
        resized_cropped_image = resized_image[start_y+100:start_y+target_height+100, :]
    cv2.imwrite("../after_processing_image/" + image_name + ".png", resized_cropped_image)
    return resized_cropped_image

def apply_alpha_gradient_to_image(image_path):
    """
        이미지의 특정 높이 이후로 선명도를 줄여 검정색으로 변환합니다.

        Parameters:
        - image: 처리할 1080x1350 이미지

        Returns:
        - 그라데이션 처리가 된 1080x1350 이미지
        """
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)

    h, w = image.shape[:2]
    assert h == 1350 and w == 1080, "입력 이미지 크기는 1080x1350이어야 합니다."

    # 구간 설정
    first_start_height = 700
    first_end_height = 800
    second_start_height = 800
    second_end_height = 1150
    third_start_height = 1150
    third_end_height = 1250
    fourth_start_height = 1250
    fourth_end_height = 1350

    first_gradient_height = first_end_height - first_start_height
    second_gradient_height = second_end_height - second_start_height
    third_gradient_height = third_end_height - third_start_height
    fourth_gradient_height = fourth_end_height - fourth_start_height

    # 첫 번째 그라데이션 알파 값
    alpha1 = np.linspace(1, 0.3, first_gradient_height).reshape(-1, 1)
    alpha1 = np.repeat(alpha1, w, axis=1)
    alpha1 = np.stack([alpha1] * 3, axis=2)  # RGB 채널 적용

    # 두 번째 그라데이션 알파 값
    alpha2 = np.linspace(0.3, 0.2, second_gradient_height).reshape(-1, 1)
    alpha2 = np.repeat(alpha2, w, axis=1)
    alpha2 = np.stack([alpha2] * 3, axis=2)  # RGB 채널 적용

    # 세 번째 그라데이션 알파 값
    alpha3 = np.linspace(0.2, 0.1, third_gradient_height).reshape(-1, 1)
    alpha3 = np.repeat(alpha3, w, axis=1)
    alpha3 = np.stack([alpha3] * 3, axis=2)  # RGB 채널 적용

    # 네 번째 구간 알파 값
    alpha4 = np.linspace(0.1, 0, third_gradient_height).reshape(-1, 1)
    alpha4 = np.repeat(alpha4, w, axis=1)
    alpha4 = np.stack([alpha4] * 3, axis=2)  # RGB 채널 적용

    # 검정색 배경 생성
    black_background = np.zeros((h, w, 3), dtype=np.uint8)

    result_image = image.copy()

    # 원본 이미지의 첫 번째 하단 부분을 알파 블렌딩
    result_image[first_start_height:first_end_height] = (
            image[first_start_height:first_end_height] * alpha1 + black_background[
                                                                  first_start_height:first_end_height] * (1 - alpha1)
    ).astype(np.uint8)

    # 원본 이미지의 두 번째 하단 부분을 알파 블렌딩
    result_image[second_start_height:second_end_height] = (
            image[second_start_height:second_end_height] * alpha2 + black_background[
                                                                    second_start_height:second_end_height] * (
                        1 - alpha2)
    ).astype(np.uint8)

    # 원본 이미지의 세 번째 하단 부분을 알파 블렌딩
    result_image[third_start_height:third_end_height] = (
            image[third_start_height:third_end_height] * alpha3 + black_background[
                                                                  third_start_height:third_end_height] * (1 - alpha3)
    ).astype(np.uint8)

    # 원본 이미지의 네 번째 하단 부분을 알파 블렌딩 (0으로 유지)
    result_image[fourth_start_height:fourth_end_height] = (
            image[fourth_start_height:fourth_end_height] * alpha4 + black_background[
                                                                    fourth_start_height:fourth_end_height] * (
                        1 - alpha4)
    ).astype(np.uint8)
    # 결과 저장
    cv2.imwrite("../after_processing_image/" + image_name + ".png", result_image)
    return result_image

def processing(image_path):
    p1_image = resize_image(image_path)
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    p1_path = "../after_processing_image/"+image_name+".png"
    apply_alpha_gradient_to_image(p1_path)
    add_basic_icon_to_image(p1_path, "Information")

def add_text_to_image_with_box(image_path, text, position, box_size, font_path, font_size, text_color=(255, 255, 255), box_color=(0, 0, 0)):
    """
    이미지에 텍스트 박스를 추가하고 그 안에 텍스트를 작성합니다.

    Parameters:
    - image_path: 기본 이미지 경로
    - text: 추가할 텍스트
    - position: 텍스트 박스를 추가할 위치 (x, y)
    - box_size: 텍스트 박스의 크기 (width, height)
    - font_path: 사용할 TTF 폰트 파일 경로
    - font_size: 폰트 크기
    - text_color: 텍스트 색상 (기본값: 흰색)
    - box_color: 텍스트 박스 색상 (기본값: 검정색)

    Returns:
    - 텍스트 박스와 텍스트가 추가된 이미지
    """
    # 이미지 로드
    image = Image.open(image_path).convert('RGBA')
    draw = ImageDraw.Draw(image)

    # 폰트 로드
    font = ImageFont.truetype(font_path, font_size)

    # 텍스트 줄바꿈 처리
    lines = []
    words = text.split(' ')
    max_width, max_height = box_size

    while words:
        line = ''
        while words and draw.textbbox((0, 0), line + words[0], font=font)[2] <= max_width:
            line = line + (words.pop(0) + ' ')
        lines.append(line)

    # 텍스트 박스 그리기
    x, y = position

    # 텍스트 추가
    current_y = y
    for line in lines:
        draw.text((x, current_y), line, font=font, fill=text_color)
        current_y += draw.textbbox((0, 0), line, font=font)[3]

    # 결과 이미지 저장
    result_image = image.convert('RGB')  # RGBA를 RGB로 변환
    return result_image

# 이미지 경로
image_path = '../after_processing_image/Carlos_Sainz_and_Charles_Leclerc_of_Ferrari_fter_the_Formula_1_Spanish_Grand_Prix_at_Circuit_de.png'

# 이미지 로드
image = cv2.imread(image_path, cv2.IMREAD_COLOR)

# 텍스트 추가
text = "베르스타펜은 '차를 커브에 올리기 힘들어 시간 손실이 크다'고 말했는데요, 중고속 구간에서는 편안함을 느꼈지만 저속 구간에서 시간 손실이 컸다고 덧붙였습니다. 일요일 레이스에서 78랩의 경주를 치르며 drama를 대비할 계획이라고 밝혔습니다."
position = (120, 870)  # 텍스트를 추가할 위치 (x, y)
font_size = 40
box_size = (900, 300)  # 텍스트 박스 크기 (width, height)
text_color = (255, 255, 255)  # 흰색
box_color = (0, 0, 0)  # 검정색


# 텍스트 박스와 텍스트가 추가된 이미지 생성
result_image = add_text_to_image_with_box(image_path, text, position, box_size, font_path, font_size, text_color, box_color)

# 결과 저장
output_path = '../after_processing_image/processing_5.png'
result_image.save(output_path)

