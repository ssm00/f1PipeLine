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


def apply_alpha_gradient_to_image(image):
    """
    이미지의 특정 높이 이후로 선명도를 줄여 검정색으로 변환하고 footer 이미지를 추가합니다.

    Parameters:
    - image: 처리할 1080x1080 이미지
    - footer_image: 추가할 1080x270 footer 이미지

    Returns:
    - 그라데이션 처리가 된 1080x1350 이미지
    """
    footer_image = cv2.imread("../after_processing_image/background_1_resize.jpg")
    h, w = image.shape[:2]
    footer_h, footer_w = footer_image.shape[:2]

    assert h == 1080 and w == 1080, "입력 이미지 크기는 1080x1080이어야 합니다."
    assert footer_h == 270 and footer_w == 1080, "footer 이미지 크기는 1080x270이어야 합니다."

    start_height = 1030
    gradient_height = 50

    # 그라데이션 알파 값 생성
    alpha = np.linspace(1, 0, gradient_height).reshape(-1, 1)
    alpha = np.repeat(alpha, w, axis=1)
    alpha = np.stack([alpha] * 3, axis=2)

    # 원본 + footer 크기 추가한 이미지 생성
    result_image = np.zeros((h + footer_h, w, 3), dtype=np.uint8)
    result_image[:h, :] = image
    result_image[h:, :] = footer_image

    # 원본 이미지의 하단 부분을 알파 블렌딩
    result_image[start_height:start_height + gradient_height] = (
        image[start_height:start_height + gradient_height] * alpha + footer_image[:gradient_height, :] * (1 - alpha)
    ).astype(np.uint8)

    return result_image

# # 이미지 로드
# image_path = '../download_image/barcelona-start-2023-1.png.jpg'
# image = cv2.imread(image_path, cv2.IMREAD_COLOR)
# size = (1080, 1080)
# resize_image(image, size)


image_path = '../after_processing_image/processing_1.jpg'
image = cv2.imread(image_path, cv2.IMREAD_COLOR)
# 그라데이션 처리 적용
gradient_image = apply_alpha_gradient_to_image(image)

# 결과 저장
output_path = '../after_processing_image/processing_2.jpg'
cv2.imwrite(output_path, gradient_image)