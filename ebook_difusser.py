import os
from abc import ABC, abstractmethod
import json

from PIL import Image
from reportlab.pdfgen import canvas
from rich.console import Console

from webuiapi import WebUIApi
from configs import *

console = Console()


class EBookDiffuser(ABC):
    def __init__(self, **kwargs):
        self.sd = StableDiffusionConfig
        self.book = BookConfig
        self.story = StoryConfig
        self.name = self.__class__.__name__

        self.profiles_dir = os.path.join(os.getcwd(), "profiles")
        self.profile_dir = os.path.join(self.profiles_dir, self.name)
        self.books_dir = os.path.join(self.profile_dir, "books")
        self.config_path = os.path.join(self.profile_dir, "config.json")

        self.api = WebUIApi(**kwargs)

    def init_profile(self):
        for path in [self.profiles_dir, self.profile_dir, self.books_dir]:
            os.makedirs(path, exist_ok=True)

        if not os.path.exists(self.config_path):
            with open(self.config_path, "w") as f:
                json.dump(default_profile_config, f)

        with open(self.config_path, "r") as f:
            config = json.load(f)
            self.sd = StableDiffusionConfig(*config["stable_diffusion"].values())
            self.book = BookConfig(*config["book"].values())
            self.story = StoryConfig(*config["story"].values())
            console.print(self.sd, self.book, self.story)

    @abstractmethod
    def generate_theme(self) -> str:
        # implement logic for generating theme
        pass

    @abstractmethod
    def generate_page_prompt(self, theme) -> str:
        # implement logic for generating SD prompt for each page image from the theme
        pass

    @abstractmethod
    def generate_page_image(self, prompt) -> Image:
        # implement logic for generating SD image for each page from the prompt
        pass

    def generate_ebook(self, theme=None):
        if self.sd.model != self.api.get_working_model():
            self.api.set_working_model(self.sd.model)

        if not theme:
            theme = self.generate_theme()

        book_dir = os.path.join(self.books_dir, theme)
        os.makedirs(book_dir, exist_ok=True)

        book = canvas.Canvas(os.path.join(book_dir, f"{theme}.pdf"))
        book.setPageSize((self.book.width, self.book.height))

        for page in range(1, self.book.num_pages + 1):
            prompt = self.generate_page_prompt(theme)
            console.print(f"Generating page {page}: ", prompt)

            img = self.generate_page_image(prompt)
            assert isinstance(img, Image.Image)

            destination = os.path.join(book_dir, f"page_{page}_{prompt}.jpg")
            img.save(destination)

            book.drawImage(
                destination,
                0,
                0,
                width=self.book.width,
                height=self.book.height,
                preserveAspectRatio=True,
            )
            book.showPage()

        book.save()

        # reset prompts in preperation for new theme
        with open(self.config_path, "r") as f:
            config = json.load(f)
            self.story = StoryConfig(*config["story"].values())
