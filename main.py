from diffusers.knollingcase import Knollingcase


if __name__ == "__main__":
    knollingcase = Knollingcase()

    while True:
        knollingcase.generate_ebook()
