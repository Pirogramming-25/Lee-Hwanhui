(function () {
    const form = document.getElementById("sentiment-form");
    const input = document.getElementById("sentiment-input");
    const button = document.getElementById("sentiment-run-btn");
    const loading = document.getElementById("sentiment-loading");
    const errorBox = document.getElementById("sentiment-error");
    const resultBox = document.getElementById("sentiment-result");
    const resultLabel = document.getElementById("sentiment-result-label");
    const resultScore = document.getElementById("sentiment-result-score");
    const historyList = document.getElementById("sentiment-history-list");

  // 서버(DB)에서 내려온 로그인 사용자의 최근 기록으로 시작.
  // 비로그인 사용자는 항상 빈 배열로 시작 -> 새로고침하면 초기화됨 (과제 18번)
    let history = readInitialHistory("sentiment-initial-history");

    function renderHistory() {
        historyList.innerHTML = "";

        history.slice(0, 5).forEach((item) => {
        const li = document.createElement("li");
        const label = item.result_data ? item.result_data.label : item.output_text;
        const score = item.result_data ? (item.result_data.score * 100).toFixed(2) : "";
        li.textContent = `${item.input_text}  →  ${label} (${score}%)`;
        historyList.appendChild(li);
        });
    }

    function setSendingState(isSending) {
        button.disabled = isSending;
        input.disabled = isSending;
        loading.hidden = !isSending;
    }

    function showError(message) {
        errorBox.textContent = message;
        errorBox.hidden = false;
        resultBox.hidden = true;
    }

    function showResult(data) {
        errorBox.hidden = true;
        resultBox.hidden = false;
        resultLabel.textContent = data.label;
        resultScore.textContent = `${(data.score * 100).toFixed(2)}%`;
    }

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const text = input.value.trim();

        if (!text) {
        showError("분석할 문장을 입력해주세요.");
        return;
        }

        setSendingState(true);
        errorBox.hidden = true;
        resultBox.hidden = true;

        try {
        const data = await postJSON("/sentiment/run/", { text });

        showResult(data);

        // 최근 기록 맨 앞에 추가 (비로그인이면 이 배열만이 유일한 기록 저장소)
        history.unshift({
            input_text: text,
            result_data: data,
        });

        renderHistory();
        } catch (error) {
        showError(error.message);
        } finally {
        setSendingState(false);
        }
    });

    renderHistory();
})();