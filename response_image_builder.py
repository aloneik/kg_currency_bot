from PIL import Image, ImageDraw, ImageFont

class ResponseImageBuilder:
    def __init__(
            self,
            font_path='./fonts/a_AvanteLt_LightItalic.ttf',
            font_size=30,
            fill_color=(0, 0, 0),
            bg_color="white"
        ):
        self.offset_x = 10
        self.offset_y = 10
        self.font_size = font_size
        self.font = ImageFont.truetype(font_path, self.font_size)
        self.fill_color = fill_color
        self.bg_color = bg_color

    def build_image(self, text):
        width, height = self._get_image_size(text)

        image = Image.new('RGB', (width, height), self.bg_color)
        draw = ImageDraw.Draw(image)

        draw.text((self.offset_x, self.offset_y), text, font=self.font, fill=self.fill_color)
        return image

    def _get_image_size(self, text):
        # 'multiline_textbbox' method requires an image bigger than multi line text bounding box 
        temporary_image = Image.new('RGB', (5000, 20000), self.bg_color)
        draw = ImageDraw.Draw(temporary_image)

        left, top, right, bottom = draw.multiline_textbbox((self.offset_x, self.offset_y), text=text, font=self.font)

        width = right - left + self.offset_x * 2
        height = bottom - top + self.offset_y * 2
        return width, height
