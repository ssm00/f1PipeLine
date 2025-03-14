import numpy as np
from PIL import Image, ImageDraw, ImageFont
from ImageModifier import CustomException
from util.commonException import CommonError, ErrorCode
from aws.s3 import S3Manager

class ImageGenerator:

    def __init__(self, database, image_generator_info, image_save_path, logger):
        self.database = database
        self.s3_manager = S3Manager()
        self.logger = logger
        self.after_processing_image_path = image_save_path.get("s3").get("after_processing_path")
        self.original_image_path = image_save_path.get("local").get("original_image")
        self.font_path = image_generator_info.get("font_path")
        self.logo_path = image_generator_info.get("logo_path")
        self.title_font_size = image_generator_info.get("title_font_size")
        self.sub_title_font_size = image_generator_info.get("sub_title_font_size")
        self.breaking_color = image_generator_info.get("breaking_color")
        self.information_color = image_generator_info.get("information_color")
        self.official_color = image_generator_info.get("official_color")
        self.tech_color = image_generator_info.get("tech_color")
        self.rumor_color = image_generator_info.get("rumor_color")
        self.godic_font = image_generator_info.get("godic_font")
        self.main_content_line_spacing = image_generator_info.get("main_content_line_spacing")
        self.main_content_font_size = image_generator_info.get("main_content_font_size")
        self.type1_image_size_4x5 = image_generator_info.get("type1_image_size_4x5")
        self.type2_image_size_4x5 = image_generator_info.get("type2_image_size_4x5")
        self.type1_image_size_1x1 = image_generator_info.get("type1_image_size_1x1")
        self.type2_image_size_1x1 = image_generator_info.get("type2_image_size_1x1")
        self.type1_text_length = image_generator_info.get("type1_text_length")
        self.type2_text_length = image_generator_info.get("type2_text_length")
        self.type1_textbox_size = image_generator_info.get("type1_textbox_size")
        self.type2_textbox_size = image_generator_info.get("type2_textbox_size")
        self.type2_textbox_size = image_generator_info.get("type2_textbox_size")
        self.type2_textbox_size = image_generator_info.get("type2_textbox_size")
        self.image_ratio = image_generator_info.get("image_ratio")

    def select_article_line(self, article_type, line_type):
        article_type = article_type.lower()
        if line_type == "type1":
            if article_type == "information":
                line_path = './prefab/information_line_440.png'
            elif article_type == "breaking":
                line_path = './prefab/breaking_line_440.png'
            elif article_type == "official":
                line_path = './prefab/official_line_440.png'
            elif article_type == "tech":
                line_path = './prefab/tech_line_440.png'
            elif article_type == "rumor":
                line_path = './prefab/rumor_line_440.png'
        elif line_type == "type2":
            if article_type == "information":
                line_path = './prefab/information_line_1050.png'
            elif article_type == "breaking":
                line_path = './prefab/breaking_line_1050.png'
            elif article_type == "official":
                line_path = './prefab/official_line_1050.png'
            elif article_type == "tech":
                line_path = './prefab/tech_line_1050.png'
            elif article_type == "rumor":
                line_path = './prefab/rumor_line_1050.png'
        return line_path

    def select_subtitle_font_color(self, article_type):
        article_type = article_type.lower()
        if article_type == "information":
            color = self.information_color
        elif article_type == "breaking":
            color = self.breaking_color
        elif article_type == "official":
            color = self.official_color
        elif article_type == "tech":
            color = self.tech_color
        elif article_type == "rumor":
            color = self.rumor_color
        return color

    def add_icon_to_image(self, image, icon_path, position):
        # 아이콘 이미지 로드
        icon = Image.open(icon_path).convert("RGBA")
        if icon is None:
            raise FileNotFoundError(f"Icon at path '{icon_path}' not found.")
        icon_width, icon_height = icon.size
        image.paste(icon, position, icon)
        return image

    # article_type은 Information, Breaking, Official, Tech, Rumor 다섯가지
    def add_title_icon_to_image(self, image, article_type):
        article_type = article_type.lower()
        if article_type == "information":
            icon_path = './prefab/information_icon.png'
            line_path = './prefab/information_line_440.png'
        elif article_type == "breaking":
            icon_path = './prefab/breaking_icon.png'
            line_path = './prefab/breaking_line_440.png'
        elif article_type == "official":
            icon_path = './prefab/official_icon.png'
            line_path = './prefab/official_line_440.png'
        elif article_type == "tech":
            icon_path = './prefab/tech_icon.png'
            line_path = './prefab/tech_line_440.png'
        elif article_type == "rumor":
            icon_path = './prefab/rumor_icon.png'
            line_path = './prefab/rumor_line_440.png'

        icon_position = (50, 700)  # (x, y)
        line_position = (50, 780)  # (x, y)
        # 기본 이미지에 아이콘 추가
        self.add_icon_to_image(image, icon_path, icon_position)
        self.add_icon_to_image(image, line_path, line_position)
        # 최종 결과 저장
        return image

    def resize_image_type1(self, image):
        w, h = image.size
        if self.image_ratio == "1x1":
            target_size = (1080, 1080)
        else:
            target_size = (1080, 1350)
        target_height = target_size[1]
        target_width = target_size[0]
        proportion_h = target_size[1] / h
        proportion_w = target_size[0] / w

        # 가로가 긴 사진인 경우
        if w > h:
            new_height = target_height + 100
            new_width = int(proportion_h * w)
            resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            start_x = (new_width - target_width) // 2
            resized_cropped_image = resized_image.crop((start_x, 100, start_x + target_width, new_height))
        # 세로가 긴 사진인 경우
        else:
            new_height = int(proportion_w * h)
            new_width = target_width
            resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            start_y = (new_height - target_height) // 2
            resized_cropped_image = resized_image.crop((0, start_y + 100, new_width, start_y + target_height + 100))
        return resized_cropped_image

    def resize_image_type2(self, image):
        """
            가로로 긴 사진 생성 사진이 새로 형식 사진이라면 이미지 비율이 너무 안맞아서 불가능 그냥 return 하기
            2160, 1350 resize
        """
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
        return resized_cropped_image

    def apply_alpha_gradient_type1(self, image):
        image = image.convert("RGB")

        w, h = image.size

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

        self.add_icon_to_image(result_image, self.logo_path,(500,1270))
        return result_image

    def split_apply_alpha_gradient_type2(self, image):
        image = image.convert("RGB")

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

        width = self.type2_image_size_4x5[0]
        height = self.type2_image_size_4x5[1]
        left_image = result_image.crop((0, 0, width / 2, height))
        right_image = result_image.crop((width / 2, 0, width, height))
        self.add_icon_to_image(left_image, self.logo_path, (500, 1270))
        self.add_icon_to_image(right_image, self.logo_path, (500, 1270))
        return left_image, right_image

    # type1으로만 페이지 생성하기
    def split_text_type1(self, text, font, line_spacing):
        """
            전체 text를 max_width, max_height 기반으로 나누기
        """
        lines = []
        pages = []
        max_width = self.type1_textbox_size[0]
        max_height = self.type1_textbox_size[0]
        words = text.split(' ')
        while words:
            line = ''
            while words and int(font.getlength(line + words[0])) <= max_width and (font.size + line_spacing) * (len(lines) + 1) <= max_height or line == '':
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
    def extract_text_for_one_page(self, words, font, line_spacing, textbox_type):
        """
            전체 text를 max_width, max_height 기반으로 나누기
            Returns
            한 페이지에 들어가는 텍스트와 남은 words들
        """
        lines = []
        if textbox_type == "type1":
            max_width = self.type1_textbox_size[0]
            max_height = self.type1_textbox_size[1]
        elif textbox_type == "type2":
            max_width = self.type2_textbox_size[0]
            max_height = self.type2_textbox_size[1]
        while words:
            line = ''
            while words and int(font.getlength(line + words[0])) <= max_width and (font.size + line_spacing) * (len(lines) + 1) < max_height or line == '':
                if words[0].endswith("."):
                    line = line + (words.pop(0) + ' ')
                    break
                line = line + (words.pop(0) + ' ')
            lines.append(line.strip())
            if (font.size + line_spacing) * (len(lines) + 1) >= max_height:
                break
        return words, lines

    # 이미지 갯수와 텍스트박스 사이즈를 기반으로 사용할 type1 or type2 예측
    def predict_type_mix(self, text, image_count):
        # type1으로 모두 만들수 있는 경우
        text_length = len(text)
        text_type_list = []
        if text_length < image_count * self.type1_text_length:
            for i in range(image_count):
                text_type_list.append("type1")
        else:
            current_sum = 0
            #마지막은 무조건 타입 1로 하기, 타입1은 중복 사진 생성 괜찮으나 타입 2 사진 중복 생성 막아둠(이상할듯)
            for _ in range(image_count-1):
                if current_sum + self.type2_text_length * 2 > text_length:
                    break
                text_type_list.append("type2")
                # type2는 1번사용시 이미지 2개가 생성되므로 * 2
                current_sum += self.type2_text_length * 2
            while current_sum < text_length and len(text_type_list) < image_count:
                text_type_list.append("type1")
                current_sum += self.type1_text_length
        return text_type_list

    # 타이틀 이미지를 만드는 경우 text가 너무 긴 경우 font size 조정 해서 무조건 1페이지 안에 넣어야함
    def adjust_text_by_textbox_size(self, text, font, line_spacing, max_size, text_type):
        max_width, max_height = max_size
        words = text.split(' ')
        lines = []
        while words:
            if (font.size + line_spacing) * len(lines) > max_height:
                raise CustomException.OutOfTextBox(font.size, text_type)
            line = ''
            while words and int(font.getlength(line + words[0])) <= max_width and (font.size + line_spacing) * (len(lines) + 1) <= max_height or line == '':
                if words[0].endswith("."):
                    line = line + (words.pop(0) + ' ')
                    break
                line = line + (words.pop(0) + ' ')
            lines.append(line.strip())
        return lines


    def add_text_to_image(self, image, text, position, font, box_size, text_color, line_spacing, text_type=None):
        draw = ImageDraw.Draw(image)

        # 텍스트 줄바꿈 처리
        x, y = position
        max_width, max_height = box_size
        # draw.rectangle([x, y, x + max_width, y + max_height], fill=(1,1,1))
        lines = self.adjust_text_by_textbox_size(text, font, line_spacing, box_size, text_type)
        for line in lines:
            draw.text((x, y), line, font=font, fill=text_color)
            y += draw.textbbox((0, 0), line, font=font)[3] + line_spacing

    def resize_alpha_adjust_type1(self, image):
        resized_image = self.resize_image_type1(image)
        result_image = self.apply_alpha_gradient_type1(resized_image)
        return result_image

    def resize_alpha_adjust_type2(self, image):
        resized_image = self.resize_image_type2(image)
        left_image, right_image = self.split_apply_alpha_gradient_type2(resized_image)
        return left_image, right_image

    def add_text_type1(self, image, lines, font, line_spacing, article_type):
        """
        이미지에 텍스트 박스를 추가하고 그 안에 텍스트를 작성합니다.
        """
        position = (120, 810)  # 텍스트를 추가할 위치 (x, y)
        box_size = self.type1_textbox_size  # 텍스트 박스 크기 (width, height)
        text_color = (255, 255, 255)  # 흰색
        box_color = (255, 255, 255)

        # 이미지 로드
        image = image.convert('RGBA')
        draw = ImageDraw.Draw(image)

        line_path = self.select_article_line(article_type, "type1")
        line_position = (50, 780)  # (x, y)
        image = self.add_icon_to_image(image, line_path, line_position)

        # 텍스트 줄바꿈 처리
        # lines = []
        # words = text.split(' ')
        max_width, max_height = box_size
        x, y = position

        for line in lines:
            draw.text((x, y), line, font=font, fill=text_color)
            y += draw.textbbox((0, 0), line, font=font)[3] + line_spacing

        result_image = image.convert('RGB')  # RGBA를 RGB로 변환
        return result_image

    def add_text_type2(self, image, lines, font, line_spacing, article_type, left_or_right):
        """
            이미지에 텍스트 박스를 추가하고 그 안에 텍스트를 작성합니다.
        """
        if left_or_right == "left":
            position = (90, 150)  # 텍스트를 추가할 위치 (x, y)
            line_position = (40, 150)  # (x, y)
        elif left_or_right == "right":
            position = (560, 150)
            line_position = (1020, 150)  # (x, y)
        box_size = self.type2_textbox_size  # 텍스트 박스 크기 (width, height)
        text_color = (255, 255, 255)  # 흰색
        box_color = (255, 255, 255)

        # 이미지 로드
        image = image.convert('RGBA')
        draw = ImageDraw.Draw(image)

        line_path = self.select_article_line(article_type, "type2")
        image = self.add_icon_to_image(image, line_path, line_position)

        # 텍스트 줄바꿈 처리
        max_width, max_height = box_size
        x, y = position
        #draw.rectangle([x, y, x + max_width, y + max_height], fill=box_color)

        for line in lines:
            if left_or_right == "left":
                draw.text((x, y), line, font=font, fill=text_color)
            else:  # right alignment
                text_width = draw.textbbox((0, 0), line, font=font)[2]
                draw.text((x + max_width - text_width, y), line, font=font, fill=text_color)
            y += draw.textbbox((0, 0), line, font=font)[3] + line_spacing

        result_image = image.convert('RGB')
        return result_image

    def create_title_image(self, image_path, title, sub_title, article_type, article_id):
        title_box_size = (900, 170)
        sub_title_box_size = (850, 110)
        title_position = (120, 870)
        sub_title_position = (120, 1113)
        title_font_size = 64
        sub_title_font_size = 48
        title_color = (255, 255, 255)
        min_title_font_size = 36
        min_sub_title_font_size = 30
        fix_size_value = 3
        image = Image.open(image_path)
        resized_image = self.resize_alpha_adjust_type1(image)
        self.add_title_icon_to_image(resized_image, article_type)
        subtitle_color = self.select_subtitle_font_color(article_type)
        while title_font_size > min_title_font_size and sub_title_font_size > min_sub_title_font_size:
            try:
                image = resized_image.convert('RGBA')
                title_font = ImageFont.truetype(self.godic_font, title_font_size)
                sub_title_font = ImageFont.truetype(self.godic_font, sub_title_font_size)
                # 제목 추가
                self.add_text_to_image(image, title, title_position, title_font, title_box_size, title_color, 10, "title")
                # 부제목 추가
                self.add_text_to_image(image, sub_title, sub_title_position, sub_title_font, sub_title_box_size, subtitle_color, 7, "sub_title")
                result_image = image.convert('RGB')
                self.s3_manager.upload_image(result_image, self.after_processing_image_path, article_id, "maincontent_0")
                break
            except CustomException.OutOfTextBox as e:
                if e.type == "title":
                    title_font_size -= fix_size_value
                elif e.type == "sub_title":
                    sub_title_font_size -= fix_size_value
        if title_font_size <= min_title_font_size or sub_title_font_size <= min_sub_title_font_size:
            self.logger.info("최소 폰트 크기 도달: title_font_size={}, sub_title_font_size={}".format(title_font_size, sub_title_font_size))
        else:
            self.logger.info(f"타이틀 이미지 저장 성공 {article_id}")

    # type1 textbox size로 페이지 갯수를 미리 계산할 경우 사용할 이미지 선택
    def select_type1_image_index(self, need_page_count, image_count):
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

    def get_original_image_path_list(self, article_sequence=None, keyword_list=None):
        if article_sequence is not None:
            image_list = self.database.get_images_by_article_sequence(article_sequence)
        elif keyword_list is not None:
            image_list = self.database.get_images_by_keyword_list(keyword_list)
            image_list.extend(self.database.get_pair_images_by_keyword_list(keyword_list))
        if len(image_list) == 0:
            raise CommonError(ErrorCode.NOMATCH_IMAGE, f"메인 컨텐츠 생성 적합한 이미지 없음 seq : {article_sequence} keywordList : {keyword_list}")
        image_path_list = []
        for image in image_list:
            image_path_list.append(f"{self.original_image_path}/{image.get('image_name')}.jpeg")
        return image_path_list

    #type1 으로만 만들기
    def create_main_image_only_type1(self, article_type, divided_text_list, font, image_path_list, select_image_index_list, article_id):
        text_num = 0
        for index, image_usage_count in enumerate(select_image_index_list):
            image_path = image_path_list[index]
            for i in range(image_usage_count):
                text = divided_text_list[text_num]
                image = Image.open(image_path)
                resized_image = self.resize_alpha_adjust_type1(image)
                result_image = self.add_text_type1(resized_image, text, font, self.main_content_line_spacing, article_type)
                self.s3_manager.upload_image(result_image, self.after_processing_image_path, article_id, f"maincontent_{index}")
                text_num += 1

    def _initialize_font(self):
        return ImageFont.truetype(self.font_path, self.main_content_font_size)

    def create_main_content_type1(self, image, words, font, article_type):
        remain_words, text = self.extract_text_for_one_page(words, font, self.main_content_line_spacing, "type1")
        resized_image = self.resize_alpha_adjust_type1(image)
        result_image = self.add_text_type1(resized_image, text, font, self.main_content_line_spacing, article_type)
        return result_image, remain_words

    def create_main_content_type2(self, image, words, font, article_type, left_or_right):
        remain_words, text = self.extract_text_for_one_page(words, font, self.main_content_line_spacing, "type2")
        image = self.add_text_type2(image, text, font, self.main_content_line_spacing, article_type, left_or_right)
        return image, remain_words

    #주어진 사진 갯수와 컨텐츠 내용을 기반으로 이미지 생성
    def create_main_content(self, text, image_path_list, article_type, article_id, only_type1=None):
        font = self._initialize_font()
        # type1으로만 생성
        image_count = len(image_path_list)
        if only_type1:
            divided_type1_pages = self.split_text_type1(text, font, self.main_content_line_spacing)
            need_page_count = len(divided_type1_pages)
            select_image_count_list = self.select_type1_image_index(need_page_count, image_count)
            self.create_main_image_only_type1(article_type, divided_type1_pages, font, image_path_list, select_image_count_list, article_id)
        else:
            # type2 계산
            text_type_list = self.predict_type_mix(text, image_count)
            words = text.split(' ')
            image_index = 1
            for index, text_type in enumerate(text_type_list):
                if text_type == "type1" and len(words) != 0:
                    image = Image.open(image_path_list[index])
                    result_image, words = self.create_main_content_type1(image, words, font, article_type)
                    self.s3_manager.upload_image(result_image, self.after_processing_image_path, article_id, f"maincontent_{image_index}")
                    image_index += 1

                elif text_type == "type2" and len(words) != 0:
                    image = Image.open(image_path_list[index])
                    left_image, right_image = self.resize_alpha_adjust_type2(image)
                    left_main_content, words  = self.create_main_content_type2(left_image, words, font, article_type, "left")
                    right_main_content, words = self.create_main_content_type2(right_image, words, font,article_type, "right")

                    self.s3_manager.upload_image(left_main_content, self.after_processing_image_path, article_id, f"maincontent_{image_index}")
                    image_index += 1
                    self.s3_manager.upload_image(right_main_content, self.after_processing_image_path, article_id, f"maincontent_{image_index}")
                    image_index += 1
            # 예측 후 생성하였는데 text가 남은경우 type1으로 생성
            while len(words) != 0:
                image = Image.open(image_path_list[len(image_path_list)-1])
                result_image, words = self.create_main_content_type1(image, words, font, article_type)
                self.s3_manager.upload_image(result_image, self.after_processing_image_path, article_id, f"maincontent_{image_index}")
                image_index += 1

