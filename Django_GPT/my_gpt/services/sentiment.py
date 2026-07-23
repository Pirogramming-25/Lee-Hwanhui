from functools import lru_cache

from transformers import pipeline

from .common import get_pipeline_device

MODEL_ID = "cardiffnlp/twitter-roberta-base-sentiment-latest"

MIN_LENGTH = 1
MAX_LENGTH = 1000


@lru_cache(maxsize=1)
def get_sentiment_pipeline():

    return pipeline(
        task="text-classification",
        model=MODEL_ID,
        device=get_pipeline_device(),
        top_k=None,  # 모든 레이블 점수를 함께 반환
    )


def validate_sentiment_input(text):

    if not isinstance(text, str):
        return "잘못된 입력 형식입니다."

    stripped = text.strip()

    if not stripped:
        return "분석할 문장을 입력해주세요."

    if len(stripped) > MAX_LENGTH:
        return f"문장은 {MAX_LENGTH}자 이하로 입력해주세요."

    return None


def run_sentiment(text):
    classifier = get_sentiment_pipeline()

    # top_k=None 이면 결과가 [[{...}, {...}, ...]] 형태로 나옵니다.
    raw_result = classifier(text)
    scores = raw_result[0] if isinstance(raw_result[0], list) else raw_result

    sorted_scores = sorted(scores, key=lambda x: x["score"], reverse=True)
    top = sorted_scores[0]

    return {
        "label": top["label"],
        "score": top["score"],
        "all_scores": sorted_scores,
    }