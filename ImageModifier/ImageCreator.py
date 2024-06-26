import cv2
import numpy as np
import os
from PIL import Image, ImageDraw, ImageFont

def resize_image(image, target_size):
    h, w = image.shape[:2]
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
    cv2.imwrite("../after_processing_image/" + "processing_1" + ".jpg", resized_cropped_image)


def apply_alpha_gradient_to_image(image):
    """
        이미지의 특정 높이 이후로 선명도를 줄여 검정색으로 변환합니다.

        Parameters:
        - image: 처리할 1080x1350 이미지

        Returns:
        - 그라데이션 처리가 된 1080x1350 이미지
        """
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

    # 첫 번째 그라데이션 알파 값 생성
    alpha1 = np.linspace(1, 0.3, first_gradient_height).reshape(-1, 1)
    alpha1 = np.repeat(alpha1, w, axis=1)
    alpha1 = np.stack([alpha1] * 3, axis=2)  # RGB 채널 적용

    # 두 번째 그라데이션 알파 값 생성
    alpha2 = np.linspace(0.3, 0.2, second_gradient_height).reshape(-1, 1)
    alpha2 = np.repeat(alpha2, w, axis=1)
    alpha2 = np.stack([alpha2] * 3, axis=2)  # RGB 채널 적용

    # 세 번째 그라데이션 알파 값 생성
    alpha3 = np.linspace(0.2, 0.1, third_gradient_height).reshape(-1, 1)
    alpha3 = np.repeat(alpha3, w, axis=1)
    alpha3 = np.stack([alpha3] * 3, axis=2)  # RGB 채널 적용

    # 네 번째 구간 알파 값 생성 (0으로 유지)
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

    return result_image

#이미지 로드
image_path = '../download_image/Jon_Enoch_for_Haas_F1_Feb_2024.jpg'
image = cv2.imread(image_path, cv2.IMREAD_COLOR)
size = (1080, 1350)
resize_image(image, size)


image_path = '../after_processing_image/processing_1.jpg'
image = cv2.imread(image_path, cv2.IMREAD_COLOR)
# 그라데이션 처리 적용
gradient_image = apply_alpha_gradient_to_image(image)

# 결과 저장
output_path = '../after_processing_image/processing_2.jpg'
cv2.imwrite(output_path, gradient_image)