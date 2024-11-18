import functools
import jiwer
import os
import requests
import torch

from modules.utils.paths import *
from modules.utils.youtube_manager import *

TEST_FILE_DOWNLOAD_URL = "https://github.com/jhj0517/whisper_flutter_new/raw/main/example/assets/jfk.wav"
TEST_FILE_PATH = os.path.join(WEBUI_DIR, "tests", "jfk.wav")
TEST_ANSWER = "And so my fellow Americans ask not what your country can do for you ask what you can do for your country"
TEST_YOUTUBE_URL = "https://www.youtube.com/watch?v=4WEQtgnBu0I&ab_channel=AndriaFitzer"
TEST_WHISPER_MODEL = "tiny"
TEST_UVR_MODEL = "UVR-MDX-NET-Inst_HQ_4"
TEST_NLLB_MODEL = "facebook/nllb-200-distilled-600M"
TEST_SUBTITLE_SRT_PATH = os.path.join(WEBUI_DIR, "tests", "test_srt.srt")
TEST_SUBTITLE_VTT_PATH = os.path.join(WEBUI_DIR, "tests", "test_vtt.vtt")


@functools.lru_cache
def is_cuda_available():
    return torch.cuda.is_available()


@functools.lru_cache
def is_pytube_detected_bot(url: str = TEST_YOUTUBE_URL):
    try:
        yt_temp_path = os.path.join("modules", "yt_tmp.wav")
        if os.path.exists(yt_temp_path):
            return False
        yt = get_ytdata(url)
        audio = get_ytaudio(yt)
        return False
    except Exception as e:
        print(f"Pytube has detected as a bot: {e}")
        return True


def download_file(url, save_dir):
    if os.path.exists(TEST_FILE_PATH):
        return

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    file_name = url.split("/")[-1]
    file_path = os.path.join(save_dir, file_name)

    response = requests.get(url)

    with open(file_path, "wb") as file:
        file.write(response.content)

    print(f"File downloaded to: {file_path}")


def calculate_wer(answer, prediction):
    return jiwer.wer(answer, prediction)
