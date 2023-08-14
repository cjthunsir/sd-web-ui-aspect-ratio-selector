import contextlib
import math
import gradio as gr
from modules import scripts
from modules import script_callbacks

ASPECT_RATIO_MAP = {
    'Cinematic (9:21)': (9, 21),
    'Widescreen (9:16)': (9, 16),
    'Landscape (2:3)': (2, 3),
    'Photo (3:4)': (3, 4),
    'Square (1:1)': (1, 1),
    'Portrait (5:4)': (5, 4),
    'Vertical (16:9)': (16, 9),
    'Long Scroll (1:4)': (1, 4),
    'High Scroll (4:1)': (4, 1),
    'Univisium (1:2)': (1, 2),
    'Poster (2:1)': (2, 1),
}


def change_height_width(choice):
    pixels = 1024 * 1024
    tup = ASPECT_RATIO_MAP[choice]
    height_ = int(math.sqrt(pixels / (tup[0] * tup[1]))) * tup[0]
    width_ = int(pixels / height_)
    return height_, width_


class AspectRatioSelectorForSDXL(scripts.Script):
    def __init__(self) -> None:
        super().__init__()

    def title(self):
        return "Aspect Ratio For Selector SDXL"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        with gr.Group():
            with gr.Accordion("Aspect Ratio For Selector SDXL", open=True):
                aspect_ratio = gr.Radio(label='Aspect Ratio (Height/Width)',
                                        choices=list(ASPECT_RATIO_MAP.keys()),
                                        value='Square (1:1)')

        # Ignore the error if the attribute is not present
        with contextlib.suppress(AttributeError):

            if is_img2img:
                # aspect_ratio.click(
                #     fn=change_height_width,
                #     inputs=aspect_ratio,
                #     outputs=[self.i2i_h, self.i2i_w])
                aspect_ratio.change(
                    fn=change_height_width,
                    inputs=aspect_ratio,
                    outputs=[self.i2i_h, self.i2i_w])
            else:
                # aspect_ratio.click(
                #     fn=change_height_width,
                #     inputs=aspect_ratio,
                #     outputs=[self.t2i_h, self.t2i_w])
                aspect_ratio.change(
                    fn=change_height_width,
                    inputs=aspect_ratio,
                    outputs=[self.t2i_h, self.t2i_w])

        return [aspect_ratio]

    def after_component(self, component, **kwargs):
        if kwargs.get("elem_id") == "txt2img_width":
            self.t2i_w = component
        if kwargs.get("elem_id") == "txt2img_height":
            self.t2i_h = component
        if kwargs.get("elem_id") == "img2img_width":
            self.i2i_w = component
        if kwargs.get("elem_id") == "img2img_height":
            self.i2i_h = component
        # if kwargs.get("elem_id") == "txt2img_prompt":
        #     self.boxx = component
        # if kwargs.get("elem_id") == "img2img_prompt":
        #     self.boxxIMG = component
        # if kwargs.get("elem_id") == "txt2img_neg_prompt":
        #     self.neg_prompt_boxTXT = component
        # if kwargs.get("elem_id") == "img2img_neg_prompt":
        #     self.neg_prompt_boxIMG = component
