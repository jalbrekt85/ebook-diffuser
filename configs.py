from dataclasses import dataclass


@dataclass
class StableDiffusionConfig:
    model: str
    prompt_template: str
    steps: int
    cfg_scale: float
    sampler: str
    negative_prompt: str


@dataclass
class BookConfig:
    num_pages: int
    width: int
    height: int


@dataclass
class StoryConfig:
    gpt_theme_prompt: str
    gpt_page_prompt: str


default_profile_config = {
    "stable_diffusion": {
        "model": "768-v-ema",
        "prompt_template": "{}, intricate,  micro-details, realistic, transparent case, knollingcase",
        "steps": 15,
        "cfg_scale": 6.0,
        "sampler": "DPM++ SDE Karras",
        "negative_prompt": "blurry, grainy, cartoon, animated, photoshop, underwater",
    },
    "book": {"num_pages": 75, "width": 550, "height": 800},
    "story": {
        "gpt_theme_prompt": "Generate a random broad theme/setting. be as creative as possible\n\ntheme: cyberpunk\ntheme: cloud kingdom\ntheme: wild west\ntheme: christmas wonderland\ntheme: luxury resort\ntheme: haunted house\ntheme: super mario bros world\ntheme: ancient greek\ntheme: space odyssey\ntheme: victorian-era steampunk\ntheme: 80s mafia\ntheme: skyrim\ntheme: underwater city\ntheme: post apocalyptic wasteland\ntheme: aztec\ntheme: galactic empire\ntheme:",
        "gpt_page_prompt": "given a theme, respond with a short and concise object relating to that theme. keep it short and unique. be as creative as possible.\n\ntheme: christmas\nresponse: tree\ntheme: wild west\nresponse: saloon\ntheme: rainforest\nresponse: canopy\ntheme: cyperpunk\nresponse: city\ntheme: subway\nresponse: rail\ntheme: {}",
    },
}
