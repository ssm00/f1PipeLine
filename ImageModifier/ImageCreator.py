import cv2
import numpy as np
import os

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
        new_height = target_height
        new_width = int(proportion_h * w)
        resized_image = cv2.resize(image, (new_width, new_height))
        # 사진 스타트 포인트 구하기 (new_width / 2) - (target_with / 2) = (new_width - target_width) / 2
        start_x = (new_width - target_width) // 2
        # 세로 전체, 가로는 start_x 부터 start_x + target_width 까지
        resized_cropped_image = resized_image[:, start_x: start_x + target_width]
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
        resized_cropped_image = resized_image[start_y:start_y+target_height, :]
    cv2.imwrite("../after_processing_image/" + "processing_1" + ".jpg", resized_cropped_image)


def apply_alpha_gradient_to_image(image, start_height):
    """
    이미지의 특정 높이 이후로 선명도를 줄여 검정색으로 변환합니다.

    Parameters:
    - image: 처리할 이미지
    - start_height: 그라데이션 시작 높이

    Returns:
    - 그라데이션 처리가 된 이미지
    """
    h, w = image.shape[:2]

    # 그라데이션 높이 계산
    gradient_height = h - start_height

    # 그라데이션 알파 값 생성
    alpha = np.linspace(1, 0, gradient_height).reshape(-1, 1)
    alpha = np.repeat(alpha, w, axis=1)
    alpha = np.stack([alpha] * 3, axis=2)  # RGB 채널 적용

    # 원본 이미지 복사
    result_image = image.copy()

    # 검정색 배경 생성
    black_background = np.zeros((gradient_height, w, 3), dtype=np.uint8)

    # 원본 이미지의 하단 부분을 알파 블렌딩
    result_image[start_height:h] = (image[start_height:h] * alpha + black_background * (1 - alpha)).astype(np.uint8)

    return result_image

# 이미지 로드
image_path = '../download_image/barcelona-start-2023-1.png.jpg'
image = cv2.imread(image_path, cv2.IMREAD_COLOR)
size = (1050, 1050)
resize_image(image, size)


#
#
# image_path = '../download_image/barcelona-start-2023-1.png.jpg'
# image = cv2.imread(image_path, cv2.IMREAD_COLOR)
# # 그라데이션 처리 적용
# start_height = 1050
# gradient_image = apply_alpha_gradient_to_image(image, start_height)
#
# # 결과 저장
# output_path = '../after_processing_image/processing_2.jpg'
# cv2.imwrite(output_path, gradient_image)