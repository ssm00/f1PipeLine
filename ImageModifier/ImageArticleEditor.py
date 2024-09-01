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
main_content_line_spacing = 15
main_content_font_size = 40

type2_size = (2160, 1350)

type1_text_length = 160
type2_text_length = 220

def select_article_line(article_type, line_type):
    if line_type == "type1":
        if article_type == "Information":
            line_path = '../prefab/information_line_440.png'
        elif article_type == "Breaking":
            line_path = '../prefab/breaking_line_440.png'
        elif article_type == "Official":
            line_path = '../prefab/official_line_440.png'
        elif article_type == "Tech":
            line_path = '../prefab/tech_line_440.png'
        elif article_type == "Rumor":
            line_path = '../prefab/rumor_line_440.png'
    elif line_type == "type2":
        if article_type == "Information":
            line_path = '../prefab/information_line_1050.png'
        elif article_type == "Breaking":
            line_path = '../prefab/breaking_line_1050.png'
        elif article_type == "Official":
            line_path = '../prefab/official_line_1050.png'
        elif article_type == "Tech":
            line_path = '../prefab/tech_line_1050.png'
        elif article_type == "Rumor":
            line_path = '../prefab/rumor_line_1050.png'
    return line_path

# def add_icon_to_image(image_path, icon_path, position):
#     """
#     이미지에 아이콘을 추가
#
#     Parameters:
#     - image_path: 기본 이미지 경로
#     - icon_path: 추가할 아이콘 이미지 경로
#     - position: 아이콘을 추가할 위치 (x, y)
#
#     Returns:
#     - 아이콘이 추가된 이미지
#     """
#     # 기본 이미지 로드 (OpenCV 사용)
#     image = cv2.imread(image_path, cv2.IMREAD_COLOR)
#     if image is None:
#         raise FileNotFoundError(f"Image at path '{image_path}' not found.")
#
#     # 아이콘 이미지 로드 (Pillow 사용)
#     icon = Image.open(icon_path)
#     if icon is None:
#         raise FileNotFoundError(f"Icon at path '{icon_path}' not found.")
#
#     # 기본 이미지를 Pillow 이미지로 변환
#     image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
#
#     # 아이콘 이미지의 크기 얻기
#     icon_width, icon_height = icon.size
#
#     # 아이콘을 추가할 위치 (x, y) 설정
#     x, y = position
#
#     # 아이콘을 기본 이미지에 붙여넣기
#     image_pil.paste(icon, (x, y), icon.convert('RGBA'))
#
#     # 결과 이미지를 다시 OpenCV 이미지로 변환
#     result_image = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)
#     return result_image
#
#
# # article_type은
# # Information, Breaking, Official, Tech, Rumor 다섯가지
# def add_title_icon_to_image(image_path, article_type):
#     image_name = os.path.splitext(os.path.basename(image_path))[0]
#     if article_type == "Information":
#         icon_path = '../prefab/information_icon.png'
#         line_path = '../prefab/information_line_440.png'
#     elif article_type == "Breaking":
#         icon_path = '../prefab/breaking_icon.png'
#         line_path = '../prefab/breaking_line_440.png'
#     elif article_type == "Official":
#         icon_path = '../prefab/official_icon.png'
#         line_path = '../prefab/official_line_440.png'
#     elif article_type == "Tech":
#         icon_path = '../prefab/tech_icon.png'
#         line_path = '../prefab/tech_line_440.png'
#     elif article_type == "Rumor":
#         icon_path = '../prefab/rumor_icon.png'
#         line_path = '../prefab/rumor_line_440.png'
#     icon_position = (50, 700)  # (x, y)
#     line_position = (50, 780)  # (x, y)
#
#     image_with_icon = add_icon_to_image(image_path, icon_path, icon_position)
#     output_path = prefix_after_processing_path + image_name + ".png"
#     cv2.imwrite(output_path, image_with_icon)
#
#     image_with_line = add_icon_to_image(output_path, line_path, line_position)
#     output_path = prefix_after_processing_path + image_name + ".png"
#     cv2.imwrite(output_path, image_with_line)

def add_icon_to_image(image, icon_path, position):
    """
    이미지에 아이콘을 추가

    Parameters:
    - image_path: 기본 이미지 경로
    - icon_path: 추가할 아이콘 이미지 경로
    - position: 아이콘을 추가할 위치 (x, y)

    Returns:
    - 아이콘이 추가된 이미지
    """

    # 아이콘 이미지 로드
    icon = Image.open(icon_path).convert("RGBA")
    if icon is None:
        raise FileNotFoundError(f"Icon at path '{icon_path}' not found.")
    icon_width, icon_height = icon.size
    image.paste(icon, position, icon)
    return image

# article_type은 Information, Breaking, Official, Tech, Rumor 다섯가지
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
    # 기본 이미지 로드
    image = Image.open(image_path).convert("RGBA")
    # 기본 이미지에 아이콘 추가
    image_with_icon = add_icon_to_image(image, icon_path, icon_position)
    image_with_line = add_icon_to_image(image_with_icon, line_path, line_position)
    # 최종 결과 저장
    output_path = os.path.join(prefix_after_processing_path, image_name + ".png")
    image_with_line.save(output_path, "PNG")

def resize_image_type1(image_path, image_id):
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    image = Image.open(image_path)
    w, h = image.size
    target_size = (1080, 1350)
    target_height = target_size[1]
    target_width = target_size[0]
    proportion_h = target_size[1] / h
    proportion_w = target_size[0] / w

    # 가로가 긴 사진인 경우
    if w > h:
        new_height = target_height + 100
        new_width = int(proportion_h * w)
        resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)
        start_x = (new_width - target_width) // 2
        resized_cropped_image = resized_image.crop((start_x, 100, start_x + target_width, new_height))
    # 세로가 긴 사진인 경우
    else:
        new_height = int(proportion_w * h)
        new_width = target_width
        resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)
        start_y = (new_height - target_height) // 2
        resized_cropped_image = resized_image.crop((0, start_y + 100, new_width, start_y + target_height + 100))

    save_dir = os.path.join(prefix_after_processing_path, str(image_id))
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, image_name + ".png")
    resized_cropped_image.save(save_path)
    return save_path


def resize_image_type2(image_path, image_id):
    """
        가로로 긴 사진 생성 사진이 새로 형식 사진이라면 이미지 비율이 너무 안맞아서 불가능 그냥 return 하기
        2160, 1350 resize
    """
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    image = Image.open(image_path)
    w, h = image.size
    target_size = (2160, 1350)
    target_height = target_size[1]
    target_width = target_size[0]
    proportion_h = target_size[1] / h
    proportion_w = target_size[0] / w

    # 가로가 긴 사진인 경우
    if w > h:
        new_height = target_height
        new_width = int(proportion_h * w)
        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        start_x = (new_width - target_width) // 2
        resized_cropped_image = resized_image.crop((start_x, 0, start_x + target_width, new_height))
    # 세로가 긴 사진인 경우
    else:
        raise CustomException.SizeNotFitType2(image.size)

    save_dir = os.path.join(prefix_after_processing_path, str(image_id))
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, image_name + ".png")
    resized_cropped_image.save(save_path)
    return save_path

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

def apply_alpha_gradient_type1(image_path, image_id):
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

    save_dir = os.path.join(prefix_after_processing_path, str(image_id))
    save_path = os.path.join(save_dir, image_name + ".png")
    result_image.save(save_path)
    return save_path

def split_apply_alpha_gradient_type2(image_path, image_id):
    """
    이미지의 특정 높이 이후로 선명도를 줄여 검정색으로 변환.

    Parameters:
    - image: 처리할 2160x1350 이미지

    Returns:
    - 그라데이션 처리가 된 2160x1350 이미지
    """
    image = Image.open(image_path).convert("RGB")

    w, h = image.size
    assert h == 1350 and w == 2160, "입력 이미지 크기는 2160x1350이어야 합니다."

    # 구간 설정
    # 왼쪽
    left_first_start_width = 0
    left_first_end_width = 440
    left_second_end_width = 490
    left_third_end_width = 540
    left_fourth_end_width = 590

    #오른쪽
    right_first_start_width = 1570
    right_first_end_width = 1620
    right_second_end_width = 1670
    right_third_end_width = 1720
    right_fourth_end_width = 2160

    left_first_gradient_width = left_first_end_width - left_first_start_width
    left_second_gradient_width = left_second_end_width - left_first_end_width
    left_third_gradient_width = left_third_end_width - left_second_end_width
    left_fourth_gradient_width = left_fourth_end_width - left_third_end_width

    right_first_gradient_width = right_first_end_width - right_first_start_width
    right_second_gradient_width = right_second_end_width - right_first_end_width
    right_third_gradient_width = right_third_end_width - right_second_end_width
    right_fourth_gradient_width = right_fourth_end_width - right_third_end_width

    def create_alpha_array(start, end, width, height):
        alpha = np.linspace(start, end, width).reshape(1, -1)
        alpha = np.repeat(alpha, height, axis=0)
        return alpha

    #검정색 배경과 블렌딩할 알파배열 0인 투명인 상태가 블랜딩 될 시 배경은 검정 붙투명과 합쳐짐
    #왼쪽
    left_alpha1 = create_alpha_array(0, 0.7, left_first_gradient_width, h)
    left_alpha2 = create_alpha_array(0.7, 0.8, left_second_gradient_width, h)
    left_alpha3 = create_alpha_array(0.8, 0.9, left_third_gradient_width, h)
    left_alpha4 = create_alpha_array(0.9, 1, left_fourth_gradient_width, h)
    #오른쪽
    right_alpha1 = create_alpha_array(1, 0.8, right_first_gradient_width, h)
    right_alpha2 = create_alpha_array(0.8, 0.6, right_second_gradient_width, h)
    right_alpha3 = create_alpha_array(0.6, 0.4, right_third_gradient_width, h)
    right_alpha4 = create_alpha_array(0.4, 0, right_fourth_gradient_width, h)

    black_background = Image.new("RGB", (w, h), (0, 0, 0))

    result_image = image.copy()

    def blend_image_section(image, alpha, start_width, end_width):
        section = image.crop((start_width, 0, end_width, h))
        black_section = black_background.crop((start_width, 0, end_width, h))
        alpha_img = Image.fromarray((alpha * 255).astype(np.uint8), mode='L')
        blended_section = Image.composite(section, black_section, alpha_img)
        image.paste(blended_section, (start_width, 0))

    blend_image_section(result_image, left_alpha1, left_first_start_width, left_first_end_width)
    blend_image_section(result_image, left_alpha2, left_first_end_width, left_second_end_width)
    blend_image_section(result_image, left_alpha3, left_second_end_width, left_third_end_width)
    blend_image_section(result_image, left_alpha4, left_third_end_width, left_fourth_end_width)
    blend_image_section(result_image, right_alpha1, right_first_start_width, right_first_end_width)
    blend_image_section(result_image, right_alpha2, right_first_end_width, right_second_end_width)
    blend_image_section(result_image, right_alpha3, right_second_end_width, right_third_end_width)
    blend_image_section(result_image, right_alpha4, right_third_end_width, right_fourth_end_width)

    width = type2_size[0]
    height = type2_size[1]
    left_image = result_image.crop((0, 0, width / 2, height))
    right_image = result_image.crop((width / 2, 0, width, height))

    save_dir = os.path.join(prefix_after_processing_path, str(image_id))
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    left_save_path = os.path.join(save_dir, image_name+"_left.png")
    right_save_path = os.path.join(save_dir, image_name+"_right.png")

    left_image.save(left_save_path)
    right_image.save(right_save_path)
    return left_save_path, right_save_path


def split_text_for_one_page(text, font, line_spacing):
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
        while words and font.getlength(line + words[0]) <= max_width and (font.size + line_spacing) * (len(lines) + 1) <= max_height or line == '':
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

#실제 text를 타입별로 나누기
def extract_text_for_one_page(words, font, line_spacing, textbox_type):
    """
        전체 text를 max_width, max_height 기반으로 나누기
        Returns
        한 페이지에 들어가는 텍스트와 남은 words들
    """
    lines = []
    pages = []
    if textbox_type == "type1":
        max_width = 900
        max_height = 370
    elif textbox_type == "type2":
        max_width = 430
        max_height = 1050
    while words:
        line = ''
        while words and font.getlength(line + words[0]) <= max_width and (font.size + line_spacing) * (len(lines) + 1) <= max_height or line == '':
            if words[0].endswith("."):
                line = line + (words.pop(0) + ' ')
                break
            line = line + (words.pop(0) + ' ')
        lines.append(line.strip())
    return words, lines

def calculate_type(text, image_count):
    # type1으로 모두 만들수 있는 경우
    text_length = len(text)
    text_type_list = []
    if text_length < image_count * type1_text_length:
        for i in range(image_count):
            text_type_list.append(1)
    else:
        current_sum = 0
        #마지막은 무조건 타입 1로 하기 타입1은 중복 사진 생성 괜찮으나 타입 2 사진 중복 생성 막아둠(이상할듯)
        for _ in range(image_count-1):
            if current_sum + type2_text_length * 2 > text_length:
                break
            text_type_list.append(2)
            # type2는 1번사용시 이미지 2개가 생성되므로 * 2
            current_sum += type2_text_length * 2
        while current_sum < text_length and len(text_type_list) < image_count:
            text_type_list.append(1)
            current_sum += type1_text_length
    print(text_type_list)
    return text_type_list


# 타이틀 이미지를 만드는 경우 text가 너무 긴 경우 font size 조정 해서 무조건 1페이지 안에 넣어야함
def adjust_text_by_textbox_size(text, font, line_spacing, max_size, text_type):
    max_width, max_height = max_size
    words = text.split(' ')
    lines = []
    while words:
        if (font.size + line_spacing) * len(lines) > max_height:
            raise CustomException.OutOfTextBox(font.size, text_type)
        line = ''
        while words and font.getlength(line + words[0]) <= max_width and (font.size + line_spacing) * (len(lines) + 1) <= max_height or line == '':
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
    lines = adjust_text_by_textbox_size(text, font, line_spacing, box_size, text_type)
    for line in lines:
        draw.text((x, y), line, font=font, fill=text_color)
        y += draw.textbbox((0, 0), line, font=font)[3] + line_spacing


def resize_alpha_adjust_type1(image_path, image_id):
    processing1_image_path = resize_image_type1(image_path, image_id)
    apply_alpha_gradient_type1(processing1_image_path, image_id)

def resize_alpha_adjust_type2(image_path, image_id):
    processing1_image_path = resize_image_type2(image_path, image_id)
    left_path, right_path = split_apply_alpha_gradient_type2(processing1_image_path, image_id)

def add_text_type1(image_path, lines, font, line_spacing, article_type, index, image_id):
    """
    이미지에 텍스트 박스를 추가하고 그 안에 텍스트를 작성합니다.
    """
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    position = (120, 810)  # 텍스트를 추가할 위치 (x, y)
    box_size = (900, 370)  # 텍스트 박스 크기 (width, height)
    text_color = (255, 255, 255)  # 흰색
    box_color = (255, 255, 255)

    # 이미지 로드
    image = Image.open(image_path).convert('RGBA')
    draw = ImageDraw.Draw(image)

    line_path = select_article_line(article_type, "type1")
    line_position = (50, 780)  # (x, y)
    image = add_icon_to_image(image, line_path, line_position)

    # 텍스트 줄바꿈 처리
    # lines = []
    # words = text.split(' ')
    max_width, max_height = box_size
    x, y = position

    # draw.rectangle([x, y, x + max_width, y + max_height], fill=box_color)
    # while words:
    #     line = ''
    #     while words and draw.textbbox((0, 0), line + words[0], font=font)[2] <= max_width:
    #         if (words[0].endswith(".")):
    #             line = line + (words.pop(0) + ' ')
    #             break
    #         line = line + (words.pop(0) + ' ')
    #     lines.append(line)

    for line in lines:
        draw.text((x, y), line, font=font, fill=text_color)
        y += draw.textbbox((0, 0), line, font=font)[3] + line_spacing

    result_image = image.convert('RGB')  # RGBA를 RGB로 변환
    # 결과 저장
    save_dir = os.path.join(prefix_after_processing_path, str(image_id))
    output_path = os.path.join(save_dir, image_name + "_index_" + str(index) + ".png")
    result_image.save(output_path)

def add_text_type2(image_path, text, font, line_spacing, article_type, index, left_or_right, image_id):
    """
        이미지에 텍스트 박스를 추가하고 그 안에 텍스트를 작성합니다.
    """
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    if left_or_right == "left":
        position = (90, 150)  # 텍스트를 추가할 위치 (x, y)
        line_position = (40, 150)  # (x, y)
    elif left_or_right == "right":
        position = (560, 150)
        line_position = (1020, 150)  # (x, y)
    box_size = (430, 1050)  # 텍스트 박스 크기 (width, height)
    text_color = (255, 255, 255)  # 흰색
    box_color = (255, 255, 255)

    # 이미지 로드
    image = Image.open(image_path).convert('RGBA')
    draw = ImageDraw.Draw(image)

    line_path = select_article_line(article_type, "type2")
    image = add_icon_to_image(image, line_path, line_position)

    # 텍스트 줄바꿈 처리
    max_width, max_height = box_size
    x, y = position
    #draw.rectangle([x, y, x + max_width, y + max_height], fill=box_color)

    lines = []
    words = text.split(' ')
    while words:
        line = ''
        while words and draw.textbbox((0, 0), line + words[0], font=font)[2] <= max_width and (font.size + line_spacing) * (len(lines) + 1) <= max_height or line == '':
            if (words[0].endswith(".")):
                line = line + (words.pop(0) + ' ')
                break
            line = line + (words.pop(0) + ' ')
        lines.append(line)
        if (font.size + line_spacing) * (len(lines) + 1) >= max_height:
            break

    for line in lines:
        if left_or_right == "left":
            draw.text((x, y), line, font=font, fill=text_color)
        else:  # right alignment
            text_width = draw.textbbox((0, 0), line, font=font)[2]
            draw.text((x + max_width - text_width, y), line, font=font, fill=text_color)
        y += draw.textbbox((0, 0), line, font=font)[3] + line_spacing

    result_image = image.convert('RGB')  # RGBA를 RGB로 변환
    # 결과 저장
    save_dir = os.path.join(prefix_after_processing_path, str(image_id))
    output_path = os.path.join(save_dir, image_name + "_index_" + str(index) + ".png")
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
    add_title_icon_to_image(image_path, article_type)
    while title_font_size > min_title_font_size and sub_title_font_size > min_sub_title_font_size:
        try:
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


def divide_image_index(need_page_count, image_count):
    """
    페이지 갯수와 이미지 갯수가 맞지 않는 경우 페이지별로 사용할 이미지 정하기
    페이지 갯수를 이미지 갯수로 나눈 몫만큼 나눈뒤 남은 페이지만큼 앞번호부터 이미지 중복 사용
    Examples image3개 page 5개인 경우
    Returns [2,2,1] 설명 : 1번 이미지 2번사용 2이미지 2번사용 3번 이미지 1번 사용
    """
    select_image_index_list = []
    page_per_image = need_page_count // image_count
    res_image_count = need_page_count % image_count
    for i in range(image_count):
        select_image_index_list.append(page_per_image)
    for i in range(res_image_count):
        select_image_index_list[i] += 1
    return select_image_index_list


### 여기서 다시 시작
def create_content_image_with_text(article_type, divided_text_list, font, image_path_list, select_image_index_list):
    text_num = 0
    for index, image_usage_count in enumerate(select_image_index_list):
        image_path = image_path_list[index]
        for i in range(image_usage_count):
            text = divided_text_list[text_num]
            add_text_type1(image_path, text, font, main_content_line_spacing, article_type, index)
            text_num += 1

def start(text, image_path_list, article_type):
    """
    주어진 사진 갯수와 컨텐츠 내용을 기반으로 이미지 생성
    Args:
        text:
        image_path_list:
        article_type:

    Returns:

    """
    font = ImageFont.truetype(font_path, main_content_font_size)

    divided_text_list = split_text_for_one_page(text, font, main_content_line_spacing)
    need_page_count = len(divided_text_list)
    image_count = len(image_path_list)
    select_image_count_list = divide_image_index(need_page_count, image_count)
    create_content_image_with_text(article_type, divided_text_list, font, image_path_list, select_image_count_list)

    # for index, lines_for_one_page in enumerate(divided_text_list):
    #     image_index = select_image_count_list[index]
    #     add_text_type1(image_path_list[image_index], lines_for_one_page, font, main_content_line_spacing, article_type, index)


# 이미지 경로
image_path = prefix_after_processing_path + 'Carlos_Sainz_and_Charles_Leclerc_of_Ferrari_fter_the_Formula_1_Spanish_Grand_Prix_at_Circuit_de.png'
before_image_path1 = "../download_image/Carlos_Sainz_and_Charles_Leclerc_of_Ferrari_fter_the_Formula_1_Spanish_Grand_Prix_at_Circuit_de.jpg"

#resize_alpha_adjust_type2(before_image_path1, "34")

left_path = "../after_processing_image/34/Carlos_Sainz_and_Charles_Leclerc_of_Ferrari_fter_the_Formula_1_Spanish_Grand_Prix_at_Circuit_de_left.png"
right_path = "../after_processing_image/34/Carlos_Sainz_and_Charles_Leclerc_of_Ferrari_fter_the_Formula_1_Spanish_Grand_Prix_at_Circuit_de_right.png"
font = ImageFont.truetype(font_path, main_content_font_size)
text ="막스 베르스타펜은 F1 역사상 가장 많은 연속 폴 포지셔닝 기록을 갱신하고자 했습니다. 그러나 베르스타펜의 RB20 차는 모나코 서킷에서의 불안정한 밸런스로 인해 어려움을 겪었습니다. 연습 세션에서 연속적으로 주행 및 밸런스 문제를 보고한 베르스타펜은 최종 예선 라운드에서 예상을 뛰어넘는 성과를 보였습니다. 하지만 세인트 데보트 코너를 탈출하는 과정에서 벽에 부딪히며 6위로 예선을 마무리했습니다. 베르스타펜은 '차를 커브에 올리기 힘들어 시간 손실이 크다'고 말했는데요, 중고속 구간에서는 편안함을 느꼈지만 저속 구간에서 시간 손실이 컸다고 덧붙였습니다. 일요일 레이스에서 78랩의 경주를 치르며 drama를 대비할 계획이라고 밝혔습니다. 베르스타펜은 '모든 차들이 조금씩 여유를 가질 것'이라며 '기적을 기대하지 않는다'고 말했습니다. 베르스타펜의 모나코 대첩에 대해 여러분은 어떻게 생각하시나요? 베르스타펜의 모나코 대첩에 대해 여러분은 어떻게 생각하시나요? 베르스타펜의 모나코 대첩에 대해 여러분은 어떻게 생각하시나요? 베르스타펜의 모나코 대첩에 대해 여러분은 어떻게 생각하시나요? , 중고속 구간에서는 편안함을 느꼈지만 저속 구간에서 시간 손실이 컸다고 덧붙였습니다. 일요일 레이스에서 78랩의 경주를 치르며 drama를 대비할 계획이라고 밝혔습니다. 베르스타펜은 '모든 차들이 조금씩 여유를 가질 것'이라며 '기적을 기대하지 않는다'고 말했습니다. 베르스타펜의 모나코 대첩에 대해 여러분은 어떻게 생각하시나요? 베르스타펜의 모나코 대첩에 대해 여러분은 어떻게 생각하시나요? 베르스타펜의 모나코 대첩에 대해 여러분은 어떻게 생각하시나요? 베르스타펜의 모나코 대첩에 대해 여러분은 어떻게 생각하시나요? , 중고속 구간에서는 편안함을 느꼈지만 저속 구간에서 시간 손실이 컸다고 덧붙였습니다. 일요일 레이스에서 78랩의 경주를 치르며 drama를 대비할 계획이라고 밝혔습니다. 베르스타펜은 '모든 차들이 조금씩 여유를 가질 것'이라며 '기적을 기대하지 않는다'고 말했습니다. 베르스타펜의 모나코 대첩에 대해 여러분은 어떻게 생각하시나요? 베르스타펜의 모나코 대첩에 대해 여러분은 어떻게 생각하시나요? 베르스타펜의 모나코 대첩에 대해 여러분은 어떻게 생각하시나요? 베르스타펜의 모나코 대첩에 대해 여러분은 어떻게 생각하시나요?"
add_text_type2(right_path, text, font, main_content_line_spacing,  "Information", 2, "right", 34)
calculate_type(text, 3)

#adjust_text_by_textbox_size(text, font, main_content_line_spacing, (430, 1050))

#start()
# resize_alpha_adjust_type1(before_image_path1)
# img_list = []
# img_list.append(image_path)
#
# create_content_image(text,img_list, "Information")
# title = "막스 베르스타펜, 모나코 그랑프리 예선에서 6위로 출발! 막스 베르스타펜, 모나코 그랑프리 예선에서 6위로 출발!"
# sub_title = "베르스타펜, 모나코에서 충돌! 그 이유는?, 베르스타펜, 모나코에서 충돌! 그 이유는?, 베르스타펜, 모나코에서 충돌! ?"
# create_title_image(image_path, title, sub_title, "Information")

# 이미지 로드
# image = cv2.imread(image_path, cv2.IMREAD_COLOR)
# # 텍스트 추가
# image_paths = []
# image_paths.append(before_image_path1)
# create_content_image(image_paths, text)

# 텍스트 박스와 텍스트가 추가된 이미지 생성
# add_text_to_image(image_path, text)

