from functools import lru_cache

from transformers import pipeline

from .common import get_pipeline_device

MODEL_ID = "sshleifer/distilbart-cnn-6-6"

MIN_LENGTH = 100
MAX_LENGTH = 5000


@lru_cache(maxsize=1)
def get_summarizer_pipeline():

    return pipeline(
        task="summarization",
        model=MODEL_ID,
        device=get_pipeline_device(),
    )


def validate_summary_input(text):

    if not isinstance(text, str):
        return "잘못된 입력 형식입니다."

    stripped = text.strip()

    if not stripped:
        return "요약할 문서를 입력해주세요."

    if len(stripped) < MIN_LENGTH:
        return f"요약할 문서는 {MIN_LENGTH}자 이상 입력해주세요."

    if len(stripped) > MAX_LENGTH:
        return f"문서는 {MAX_LENGTH}자 이하로 입력해주세요."

    return None


def run_summary(text, do_sample=False):

    summarizer = get_summarizer_pipeline()

    generate_kwargs = {"max_length": 180, "min_length": 40}

    if do_sample:
        generate_kwargs.update(
            {"do_sample": True, "top_p": 0.9, "temperature": 0.8}
        )

    result = summarizer(text, **generate_kwargs)
    summary = result[0]["summary_text"].strip()

    original_length = len(text)
    summary_length = len(summary)
    summary_ratio = (
        (summary_length / original_length) * 100 if original_length else 0
    )

    return {
        "summary": summary,
        "original_length": original_length,
        "summary_length": summary_length,
        "summary_ratio": round(summary_ratio, 2),
    }