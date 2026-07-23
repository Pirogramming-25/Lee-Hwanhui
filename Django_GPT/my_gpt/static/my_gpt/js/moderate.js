(function () {
    const form = document.getElementById("moderate-form");
    const input = document.getElementById("moderate-input");
    const button = document.getElementById("moderate-run-btn");
    const loading = document.getElementById("moderate-loading");
    const errorBox = document.getElementById("moderate-error");
    const resultBox = document.getElementById("moderate-result");
    const highestLabelEl = document.getElementById("moderate-highest-label");
    const highestScoreEl = document.getElementById("moderate-highest-score");
    const allScoresEl = document.getElementById("moderate-all-scores");
    const historyList = document.getElementById("moderate-history-list");

    // moderate도 로그인 필수 페이지 -> history는 항상 서버(DB) 기록만 사용.
    let history = readInitialHistory("moderate-initial-history");

    function renderHistory() {
        historyList.innerHTML = "";

        history.slice(0, 5).forEach((item) => {
        const li = document.createElement("li");
        const score = item.result_data
            ? (item.result_data.highest_score * 100).toFixed(2)
            : "";
        li.textContent = `${item.input_text}  →  ${item.output_text} (${score}%)`;
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

        highestLabelEl.textContent = data.highest_label;
        highestScoreEl.textContent = `${(data.highest_score * 100).toFixed(2)}%`;

        allScoresEl.innerHTML = "";
        data.all_scores.forEach((item) => {
        const li = document.createElement("li");
        li.textContent = `${item.label}: ${(item.score * 100).toFixed(2)}%`;
        allScoresEl.appendChild(li);
        });
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
        const data = await postJSON("/moderate/run/", { text });

        showResult(data);

        history.unshift({
            input_text: text,
            output_text: data.highest_label,
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