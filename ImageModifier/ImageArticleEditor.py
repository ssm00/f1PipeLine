import cv2
import numpy as np
import os
from PIL import Image, ImageDraw, ImageFont
import CustomException

prefix_after_processing_path = "../after_processing_image/"
font_path = "../prefab/Cafe24Ohsquare-v2.0/Cafe24Ohsquare-v2.0.ttf"
breaking_color = "#FB0045"
information_color = "#F38A4A"
official_color = "#c6ff02"
tech_color = "#4AB2F3"
rumor_color = "#f4e04b"
godic_font = "../prefab/Noto_Sans_KR/static/NotoSansKR-Bold.ttf"

doble_size = (2160, 1350)


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
# Information, Breaking, Official, Tech, Rumor 다섯가지
def add_title_icon_to_image(image_path, article_type):
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
    output_path = prefix_after_processing_path + image_name + ".png"
    cv2.imwrite(output_path, image_with_icon)

    image_with_line = add_icon_to_image(output_path, line_path, line_position)
    output_path = prefix_after_processing_path + image_name + ".png"
    cv2.imwrite(output_path, image_with_line)

def resize_image_type1(image_path):
    """
    1080, 1350 resize
    """
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
        resized_cropped_image = resized_image[start_y + 100:start_y + target_height + 100, :]
    cv2.imwrite(prefix_after_processing_path + image_name + ".png", resized_cropped_image)
    return resized_cropped_image

# def apply_alpha_gradient_to_image(image_path):
#     """
#         이미지의 특정 높이 이후로 선명도를 줄여 검정색으로 변환합니다.
#
#         Parameters:
#         - image: 처리할 1080x1350 이미지
#
#         Returns:
#         - 그라데이션 처리가 된 1080x1350 이미지
#         """
#     image_name = os.path.splitext(os.path.basename(image_path))[0]
#     image = cv2.imread(image_path, cv2.IMREAD_COLOR)
#
#     h, w = image.shape[:2]
#     assert h == 1350 and w == 1080, "입력 이미지 크기는 1080x1350이어야 합니다."
#
#     # 구간 설정
#     first_start_height = 700
#     first_end_height = 800
#     second_start_height = 800
#     second_end_height = 1150
#     third_start_height = 1150
#     third_end_height = 1250
#     fourth_start_height = 1250
#     fourth_end_height = 1350
#
#     first_gradient_height = first_end_height - first_start_height
#     second_gradient_height = second_end_height - second_start_height
#     third_gradient_height = third_end_height - third_start_height
#     fourth_gradient_height = fourth_end_height - fourth_start_height
#
#     # 첫 번째 그라데이션 알파 값
#     alpha1 = np.linspace(1, 0.3, first_gradient_height).reshape(-1, 1)
#     alpha1 = np.repeat(alpha1, w, axis=1)
#     alpha1 = np.stack([alpha1] * 3, axis=2)  # RGB 채널 적용
#
#     # 두 번째 그라데이션 알파 값
#     alpha2 = np.linspace(0.3, 0.2, second_gradient_height).reshape(-1, 1)
#     alpha2 = np.repeat(alpha2, w, axis=1)
#     alpha2 = np.stack([alpha2] * 3, axis=2)  # RGB 채널 적용
#
#     # 세 번째 그라데이션 알파 값
#     alpha3 = np.linspace(0.2, 0.1, third_gradient_height).reshape(-1, 1)
#     alpha3 = np.repeat(alpha3, w, axis=1)
#     alpha3 = np.stack([alpha3] * 3, axis=2)  # RGB 채널 적용
#
#     # 네 번째 구간 알파 값
#     alpha4 = np.linspace(0.1, 0, third_gradient_height).reshape(-1, 1)
#     alpha4 = np.repeat(alpha4, w, axis=1)
#     alpha4 = np.stack([alpha4] * 3, axis=2)  # RGB 채널 적용
#
#     # 검정색 배경 생성
#     black_background = np.zeros((h, w, 3), dtype=np.uint8)
#
#     result_image = image.copy()
#
#     # 원본 이미지의 첫 번째 하단 부분을 알파 블렌딩
#     result_image[first_start_height:first_end_height] = (
#             image[first_start_height:first_end_height] * alpha1 + black_background[
#                                                                   first_start_height:first_end_height] * (1 - alpha1)
#     ).astype(np.uint8)
#
#     # 원본 이미지의 두 번째 하단 부분을 알파 블렌딩
#     result_image[second_start_height:second_end_height] = (
#             image[second_start_height:second_end_height] * alpha2 + black_background[
#                                                                     second_start_height:second_end_height] * (
#                     1 - alpha2)
#     ).astype(np.uint8)
#
#     # 원본 이미지의 세 번째 하단 부분을 알파 블렌딩
#     result_image[third_start_height:third_end_height] = (
#             image[third_start_height:third_end_height] * alpha3 + black_background[
#                                                                   third_start_height:third_end_height] * (1 - alpha3)
#     ).astype(np.uint8)
#
#     # 원본 이미지의 네 번째 하단 부분을 알파 블렌딩 (0으로 유지)
#     result_image[fourth_start_height:fourth_end_height] = (
#             image[fourth_start_height:fourth_end_height] * alpha4 + black_background[
#                                                                     fourth_start_height:fourth_end_height] * (
#                     1 - alpha4)
#     ).astype(np.uint8)
#     # 결과 저장
#     cv2.imwrite(prefix_after_processing_path + image_name + ".png", result_image)
#     return result_image

def apply_alpha_gradient_to_image_type1(image_path):
    """
    이미지의 특정 높이 이후로 선명도를 줄여 검정색으로 변환.

    Parameters:
    - image: 처리할 1080x1350 이미지

    Returns:
    - 그라데이션 처리가 된 1080x1350 이미지
    """
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    image = Image.open(image_path).convert("RGB")

    w, h = image.size
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

    # 알파 값 생성
    def create_alpha_array(start, end, height, width):
        alpha = np.linspace(start, end, height).reshape(-1, 1)
        alpha = np.repeat(alpha, width, axis=1)
        return alpha

    alpha1 = create_alpha_array(1, 0.3, first_gradient_height, w)
    alpha2 = create_alpha_array(0.3, 0.2, second_gradient_height, w)
    alpha3 = create_alpha_array(0.2, 0.1, third_gradient_height, w)
    alpha4 = create_alpha_array(0.1, 0, fourth_gradient_height, w)

    black_background = Image.new("RGB", (w, h), (0, 0, 0))

    result_image = image.copy()

    def blend_image_section(image, alpha, start_height, end_height):
        section = image.crop((0, start_height, w, end_height))
        black_section = black_background.crop((0, start_height, w, end_height))
        alpha_img = Image.fromarray((alpha * 255).astype(np.uint8), mode='L')
        blended_section = Image.composite(section, black_section, alpha_img)
        image.paste(blended_section, (0, start_height))

    blend_image_section(result_image, alpha1, first_start_height, first_end_height)
    blend_image_section(result_image, alpha2, second_start_height, second_end_height)
    blend_image_section(result_image, alpha3, third_start_height, third_end_height)
    blend_image_section(result_image, alpha4, fourth_start_height, fourth_end_height)

    output_path = os.path.join(prefix_after_processing_path, image_name + ".png")
    result_image.save(output_path)
    return result_image

def divide_text_for_one_page(text, font, line_spacing):
    """
        전체 text를 max_width, max_height 기반으로 나누기
    """
    lines = []
    pages = []
    max_width = 900
    max_height = 370
    words = text.split(' ')
    while words:
        line = ''
        while words and font.getlength(line + words[0]) <= max_width and (font.size + line_spacing) * (
                len(lines) + 1) <= max_height:
            if words[0].endswith("."):
                line = line + (words.pop(0) + ' ')
                break
            line = line + (words.pop(0) + ' ')
        lines.append(line.strip())
        if (font.size + line_spacing) * (len(lines) + 1) >= max_height:
            pages.append(lines.copy())
            lines.clear()
    pages.append(lines)
    return pages


# 타이틀 이미지를 만드는 경우 text가 너무 긴 경우 font size 조정 해서 무조건 1페이지 안에 넣어야함
def split_text_by_textboxsize(text, font, line_spacing, max_size, text_type):
    max_width, max_height = max_size
    words = text.split(' ')
    lines = []
    while words:
        if (font.size + line_spacing) * len(lines) > max_height:
            raise CustomException.OutOfTextBox(font.size, text_type)
        line = ''
        while words and font.getlength(line + words[0]) <= max_width and (font.size + line_spacing) * (
                len(lines) + 1) <= max_height:
            if words[0].endswith("."):
                line = line + (words.pop(0) + ' ')
                break
            line = line + (words.pop(0) + ' ')
        lines.append(line.strip())
    return lines


def add_text_to_image(image, text, position, font, box_size, text_color, line_spacing, text_type=None):
    """
    이미지에 텍스트 박스를 추가하고 그 안에 텍스트를 작성합니다.
    """
    # 이미지 로드
    draw = ImageDraw.Draw(image)

    # 텍스트 줄바꿈 처리
    x, y = position
    max_width, max_height = box_size
    # draw.rectangle([x, y, x + max_width, y + max_height], fill=(1,1,1))
    lines = split_text_by_textboxsize(text, font, line_spacing, box_size, text_type)
    for line in lines:
        draw.text((x, y), line, font=font, fill=text_color)
        y += draw.textbbox((0, 0), line, font=font)[3] + line_spacing


def resize_alpha_adjust_type1(image_path):
    processing1_image = resize_image_type1(image_path)
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    processing1_path = prefix_after_processing_path + image_name + ".png"
    apply_alpha_gradient_to_image_type1(processing1_path)

# def resize_alpha_adjust_type2(image_path):
#     p1_image = resize_image_type1(image_path)
#     image_name = os.path.splitext(os.path.basename(image_path))[0]
#     p1_path = prefix_after_processing_path + image_name + ".png"
#     apply_alpha_gradient_to_image(p1_path)


def create_main_content_type1(image_path, text, font, line_spacing):
    """
    이미지에 텍스트 박스를 추가하고 그 안에 텍스트를 작성합니다.
    """
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    position = (120, 800)  # 텍스트를 추가할 위치 (x, y)
    box_size = (900, 370)  # 텍스트 박스 크기 (width, height)
    text_color = (255, 255, 255)  # 흰색
    box_color = (255, 255, 255)

    # 이미지 로드
    image = Image.open(image_path).convert('RGBA')
    draw = ImageDraw.Draw(image)

    # 텍스트 줄바꿈 처리
    lines = []
    words = text.split(' ')
    max_width, max_height = box_size
    x, y = position

    # draw.rectangle([x, y, x + max_width, y + max_height], fill=box_color)
    while words:
        line = ''
        while words and draw.textbbox((0, 0), line + words[0], font=font)[2] <= max_width:
            if (words[0].endswith(".")):
                line = line + (words.pop(0) + ' ')
                break
            line = line + (words.pop(0) + ' ')
        lines.append(line)

    for line in lines:
        draw.text((x, y), line, font=font, fill=text_color)
        y += draw.textbbox((0, 0), line, font=font)[3] + line_spacing

    result_image = image.convert('RGB')  # RGBA를 RGB로 변환
    # 결과 저장
    output_path = prefix_after_processing_path + image_name + ".png"
    result_image.save(output_path)

def create_main_content_type2(image_path, text, font, line_spacing):
    """
        이미지에 텍스트 박스를 추가하고 그 안에 텍스트를 작성합니다.
        """
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    position = (120, 800)  # 텍스트를 추가할 위치 (x, y)
    box_size = (900, 370)  # 텍스트 박스 크기 (width, height)
    text_color = (255, 255, 255)  # 흰색
    box_color = (255, 255, 255)

    # 이미지 로드
    image = Image.open(image_path).convert('RGBA')
    draw = ImageDraw.Draw(image)

    # 텍스트 줄바꿈 처리
    lines = []
    words = text.split(' ')
    max_width, max_height = box_size
    x, y = position

    # draw.rectangle([x, y, x + max_width, y + max_height], fill=box_color)
    while words:
        line = ''
        while words and draw.textbbox((0, 0), line + words[0], font=font)[2] <= max_width:
            if (words[0].endswith(".")):
                line = line + (words.pop(0) + ' ')
                break
            line = line + (words.pop(0) + ' ')
        lines.append(line)

    for line in lines:
        draw.text((x, y), line, font=font, fill=text_color)
        y += draw.textbbox((0, 0), line, font=font)[3] + line_spacing

    result_image = image.convert('RGB')  # RGBA를 RGB로 변환
    # 결과 저장
    output_path = prefix_after_processing_path + image_name + ".png"
    result_image.save(output_path)


def create_title_image(image_path, title, sub_title, article_type):
    title_box_size = (900, 174)
    sub_title_box_size = (850, 116)
    title_position = (120, 870)
    sub_title_position = (120, 1113)
    title_font_size = 64
    sub_title_font_size = 48
    title_color = (255, 255, 255)
    min_title_font_size = 36
    min_sub_title_font_size = 30
    fix_size_value = 3
    while title_font_size > min_title_font_size and sub_title_font_size > min_sub_title_font_size:
        try:
            add_title_icon_to_image(image_path, article_type)
            image = Image.open(image_path).convert('RGBA')
            title_font = ImageFont.truetype(godic_font, title_font_size)
            sub_title_font = ImageFont.truetype(godic_font, sub_title_font_size)
            add_text_to_image(image, title, title_position, title_font, title_box_size, title_color, 10, "title")
            add_text_to_image(image, sub_title, sub_title_position, sub_title_font, sub_title_box_size,
                              information_color, 7, "sub_title")
            result_image = image.convert('RGB')
            result_image.save(image_path)
            break
        except CustomException.OutOfTextBox as e:
            if e.type == "title":
                title_font_size -= fix_size_value
                print(f"{title_font_size} , title 사이즈 조정")
            elif e.type == "sub_title":
                sub_title_font_size -= fix_size_value
                print(f"{sub_title_font_size} , sub title 사이즈 조정")
    if title_font_size <= min_title_font_size or sub_title_font_size <= min_sub_title_font_size:
        print("최소 폰트 크기 도달: title_font_size={}, sub_title_font_size={}".format(title_font_size, sub_title_font_size))
    else:
        print("타이틀 이미지 저장 성공")


def select_image_index(need_page_count, image_count):
    """
    페이지 갯수와 이미지 갯수가 맞지 않는 경우 페이지별로 사용할 이미지 정하기
    페이지 갯수를 이미지 갯수로 나눈 몫만큼 나눈뒤 남은 페이지만큼 앞번호부터 이미지 중복 사용
    Examples image3개 page 5개인 경우
    Returns [0,0,1,1,2] 설명 : 1페이지 0번 이미지 2페이지 0번 이미지 3페이지 1번 이미지

    """
    select_image_index_list = []
    page_per_image = need_page_count // image_count
    res_image_count = need_page_count % image_count
    for i in range(image_count):
        count = page_per_image + (1 if i < res_image_count else 0)
        select_image_index_list.extend([i] * count)
    return select_image_index_list

def create_content_image(text, image_path_list):
    font_size = 40
    line_spacing = 20
    font = ImageFont.truetype(font_path, font_size)

    divided_text = divide_text_for_one_page(text, font, line_spacing)
    need_page_count = len(divided_text)
    image_count = len(image_path_list)
    select_image_index_list = select_image_index(need_page_count, image_count)
    for index, text_for_one_page in enumerate(divided_text):
        image_index = select_image_index_list[index]
        create_main_content_type1(image_path_list[image_index], text_for_one_page, font, line_spacing)


# 이미지 경로
image_path = prefix_after_processing_path + 'Carlos_Sainz_and_Charles_Leclerc_of_Ferrari_fter_the_Formula_1_Spanish_Grand_Prix_at_Circuit_de.png'
before_image_path1 = "../download_image/Carlos_Sainz_and_Charles_Leclerc_of_Ferrari_fter_the_Formula_1_Spanish_Grand_Prix_at_Circuit_de.jpg"

resize_alpha_adjust_type1(before_image_path1)

# 이미지 로드
# image = cv2.imread(image_path, cv2.IMREAD_COLOR)
# # 텍스트 추가
# text = "베르스타펜은 '차를 커브에 올리기 힘들어 시간 손실이 크다'고 말했는데요, 중고속 구간에서는 편안함을 느꼈지만 저속 구간에서 시간 손실이 컸다고 덧붙였습니다. 일요일 레이스에서 78랩의 경주를 치르며 drama를 대비할 계획이라고 밝혔습니다. 일요일 레이스에서 78랩의 경주를 치르며 drama를 대비할 계획이라고 밝혔습니다. 일요일 레이스에서 78랩의 경주를 치르며 drama를 대비할 계획이라고 밝혔습니다. 일요일 레이스에서 78랩의 경주를 치르며 drama를 대비할 계획이라고 밝혔습니다. 일요일 레이스에서 78랩의 경주를 치르며 drama를 대비할 계획이라고 밝혔습니다. 일요일 레이스에서 78랩의 경주를 치르며 drama를 대비할 계획이라고 밝혔습니다. 일요일 레이스에서 78랩의 경주를 치르며 drama를 대비할 계획이라고 밝혔습니다. 일요일 레이스에서 78랩의 경주를 치르며 drama를 대비할 계획이라고 밝혔습니다."
# title = "막스 베르스타펜, 모나코 그랑프리 예선에서 6위로 출발! 막스 베르스타펜, 모나코 그랑프리 예선에서 6위로 출발! 막스 베르스타펜  막스 베르 스타펜 막스 베르 스타펜"
# sub_title = "베르스타펜, 모나코에서 충돌! 그 이유는?, 베르스타펜, 모나코에서 충돌! 그 이유는?, 베르스타펜, 모나코에서 충돌! ?"
# create_title_image(image_path, title, sub_title, "Information")
# image_paths = []
# image_paths.append(before_image_path1)
# create_content_image(image_paths, text)

# 텍스트 박스와 텍스트가 추가된 이미지 생성
# add_text_to_image(image_path, text)

