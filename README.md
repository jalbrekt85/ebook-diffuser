# Ebook-Diffuser
An end to end, customizable, ebook automation tool leveraging Stable Diffusion and GPT-3, built on Automatic1111's Stable Diffusion API to create beautiful books in `PDF` format

# Prerequisites

### Install  AUTOMATIC1111's stable diffusion
First you'll need to run AUTOMATIC1111's stable diffusion web UI in API mode.
Follow setup instructions [here](https://github.com/AUTOMATIC1111/stable-diffusion-webui#installation-and-running)
if you haven't yet installed it
> Install Python 3.10.6, checking "Add Python to PATH"<br>Install git.<br><br>Download the stable-diffusion-webui repository, for example by running git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git.<br><br>Place model.ckpt in the models directory (see dependencies for where to get it).<br><br>(Optional) Place GFPGANv1.4.pth in the base directory, alongside webui.py (see dependencies for where to get it).<br><br>Run webui-user.bat from Windows
 Explorer as normal, non-administrator, user.<br>

### Add the `api` flag
add the `--api` flag to your `webui-user.bat` to run in API mode:
```
set COMMANDLINE_ARGS=--api
```
If you are using a 2.X model, make sure to follow the additional instructions [here](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Features#stable-diffusion-20)

Finally, run `webui-user.bat`

`EbookDiffuser` will connect to `127.0.0.1` by default once your local server is running. You can modify this by passing in the `host`/`port` kwargs in your diffuser instantiation

If you plan on using the OpenAI API in your `diffusers` you will need add your API key to a `.env` following the `example.env`:
```sh
cp .example.env .env
```

## Installing

### Clone the repository
Independent of AUTOMATIC1111's repo, clone this repo
```sh
git clone https://github.com/jalbrekt85/ebook-diffuser.git
```

### Navigate to the project directory

```sh
cd ebook-diffuser
```

### Install the dependencies
```sh
pip install -r requirements.txt
```

## Usage
Books are generated from `diffusers`, custom classes that define the logic for generating ebooks. `diffusers` derive from `EbookDiffuser` and must implement the following methods:

- `generate_theme()`: logic to return the general theme of the book to guide page image generation
- `generate_page_prompt()`: logic to generate the prompt to pass to stable diffusion for each page image, usually involving the `theme` and `GPT-3`
- `generate_page_image()`: logic to generate each page image, returning a `PIL.Image` representing the image for that page

Take a look at `ebook_diffuser.py` to get an intuition on building a `diffuser`. An example `diffuser`,  `Knollingcase` is provided, using `GPT-3` to generate a *random* theme, `GPT-3` is then used to generate an object/setting for each page relating to that theme then a dynamic prompt is built and passed into stable diffusion for image generation.

After building a diffuser, you can instantiate it like in the following example using the `Knollingcase` diffuser
```py
from diffusers.knollingcase import Knollingcase

knollingcase = Knollingcase()
```
A directory, `profiles/{diffuser name}` will automatically be generated. Inside you find a config file, `config.json` with default configuration data. The configuration data should be edited to your specific use cases. In you `diffuser` class you can reference this data as follows:

-`self.sd`: a dataclass, `StableDiffusionConfig`:
```py
model: str
prompt_template: str
steps: int
cfg_scale: float
sampler: str
negative_prompt: str
width: str
height: str
```
- `self.book`: a dataclass, `BookConfig`:
```py
    num_pages: int
    width: int
    height: int
```
- `self.story`: a dataclass, `StoryConfig`:
```py
    gpt_theme_prompt: str
    gpt_page_prompt: str
```
- `self.api`: an instantiation of [WebUIApi](https://github.com/mix1009/sdwebuiapi), containing an interface for all of the functionality from the AUTOMATIC1111 web ui. Notable methods include:
    - `txt2img`
    - `img2img`
    - `extra_single_image` (upscaling)


After instantiating your diffusser, generate an ebook with the `generate_ebook` method:
```py
 knollingcase.generate_ebook()
 ```

 A directory, `profiles/{diffuser name}/books/{theme}`, will be created containing the final result, `{theme}.pdf` and all generated images

The PDF can be directly uploaded to self publishing sites like Amazon to turn your AI generation into a physical book

## Using the Knollingcase Diffuser
This repo is configured to work with the `Knollingcase` diffuser by default. To use it, you'll just need to install the model & embeddings:
- **model**: [SD 2.0](https://huggingface.co/stabilityai/stable-diffusion-2):  ([download](https://huggingface.co/stabilityai/stable-diffusion-2/blob/main/768-v-ema.ckpt)) /([install guide](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Features#stable-diffusion-20))
- **embeddings**: [ProGamerGov/knollingcase-embeddings-sd-v2-0](https://huggingface.co/ProGamerGov/knollingcase-embeddings-sd-v2-0):  ([download](https://huggingface.co/ProGamerGov/knollingcase-embeddings-sd-v2-0/blob/main/kc32-v4-5000.pt))/([install guide](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Textual-Inversion#using-pre-trained-embeddings))

Then simply run `main.py`
```sh
python main.py
```