import json
import logging

from django.http import JsonResponse
from django.shortcuts import render

from .decorators import model_login_required
from .models import InferenceHistory
from .services.sentiment import run_sentiment, validate_sentiment_input
from .services.summarizer import run_summary, validate_summary_input
from .services.moderator import run_moderation, validate_moderation_input

logger = logging.getLogger(__name__)


def _recent_histories(request, task):
    if not request.user.is_authenticated:
        return []

    histories = InferenceHistory.objects.filter(
        user=request.user,
        task=task,
    ).order_by("-created_at")[:5]

    return [
        {
            "input_text": h.input_text,
            "output_text": h.output_text,
            "result_data": h.result_data,
            "created_at": h.created_at.strftime("%Y-%m-%d %H:%M"),
        }
        for h in histories
    ]


def sentiment_view(request):
    recent_histories = _recent_histories(request, InferenceHistory.Task.SENTIMENT)
    return render(
        request,
        "my_gpt/sentiment.html",
        {"recent_histories": recent_histories},
    )


def sentiment_run(request):
    if request.method != "POST":
        return JsonResponse({"error": "잘못된 요청 방식입니다."}, status=405)

    try:
        body = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "올바른 요청 형식이 아닙니다."}, status=400)

    text = str(body.get("text") or "")

    error_message = validate_sentiment_input(text)
    if error_message:
        return JsonResponse({"error": error_message}, status=400)

    try:
        result = run_sentiment(text.strip())
    except Exception:
        logger.exception("Sentiment model inference failed.")
        return JsonResponse(
            {"error": "모델 실행에 실패했습니다.\n잠시 후 다시 시도해주세요."},
            status=502,
        )

    if request.user.is_authenticated:
        InferenceHistory.objects.create(
            user=request.user,
            task=InferenceHistory.Task.SENTIMENT,
            input_text=text.strip(),
            output_text=result["label"],
            result_data=result,
        )

    return JsonResponse(result)


@model_login_required
def summarize_view(request):
    recent_histories = _recent_histories(request, InferenceHistory.Task.SUMMARIZE)
    return render(
        request,
        "my_gpt/summarize.html",
        {"recent_histories": recent_histories},
    )


@model_login_required
def summarize_run(request):
    if request.method != "POST":
        return JsonResponse({"error": "잘못된 요청 방식입니다."}, status=405)

    try:
        body = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "올바른 요청 형식이 아닙니다."}, status=400)

    text = str(body.get("text") or "")

    error_message = validate_summary_input(text)
    if error_message:
        return JsonResponse({"error": error_message}, status=400)

    try:
        result = run_summary(text.strip())
    except Exception:
        logger.exception("Summarization model inference failed.")
        return JsonResponse(
            {"error": "모델 실행에 실패했습니다.\n잠시 후 다시 시도해주세요."},
            status=502,
        )

    InferenceHistory.objects.create(
        user=request.user,
        task=InferenceHistory.Task.SUMMARIZE,
        input_text=text.strip(),
        output_text=result["summary"],
        result_data=result,
    )

    return JsonResponse(result)


@model_login_required
def moderate_view(request):
    recent_histories = _recent_histories(request, InferenceHistory.Task.MODERATE)
    return render(
        request,
        "my_gpt/moderate.html",
        {"recent_histories": recent_histories},
    )


@model_login_required
def moderate_run(request):
    if request.method != "POST":
        return JsonResponse({"error": "잘못된 요청 방식입니다."}, status=405)

    try:
        body = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "올바른 요청 형식이 아닙니다."}, status=400)

    text = str(body.get("text") or "")

    error_message = validate_moderation_input(text)
    if error_message:
        return JsonResponse({"error": error_message}, status=400)

    try:
        result = run_moderation(text.strip())
    except Exception:
        logger.exception("Moderation model inference failed.")
        return JsonResponse(
            {"error": "모델 실행에 실패했습니다.\n잠시 후 다시 시도해주세요."},
            status=502,
        )

    InferenceHistory.objects.create(
        user=request.user,
        task=InferenceHistory.Task.MODERATE,
        input_text=text.strip(),
        output_text=result["highest_label"],
        result_data=result,
    )

    return JsonResponse(result)


@model_login_required
def combo_view(request):
    recent_histories = _recent_histories(request, InferenceHistory.Task.COMBO)
    return render(
        request,
        "my_gpt/combo.html",
        {"recent_histories": recent_histories},
    )