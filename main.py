from diffusers.knollingcase import Knollingcase


if __name__ == "__main__":
    knollingcase = Knollingcase(host='127.0.0.1', port=7860)

    while True:
        knollingcase.generate_ebook()
