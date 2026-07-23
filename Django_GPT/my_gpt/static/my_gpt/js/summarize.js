(function () {
    const form = document.getElementById("summarize-form");
    const input = document.getElementById("summarize-input");
    const button = document.getElementById("summarize-run-btn");
    const loading = document.getElementById("summarize-loading");
    const errorBox = document.getElementById("summarize-error");
    const resultBox = document.getElementById("summarize-result");
    const originalLengthEl = document.getElementById("summarize-original-length");
    const summaryLengthEl = document.getElementById("summarize-summary-length");
    const ratioEl = document.getElementById("summarize-ratio");
    const resultTextEl = document.getElementById("summarize-result-text");
    const historyList = document.getElementById("summarize-history-list");

    // summarize는 로그인 필수 페이지라, 여기 오는 사람은 항상 로그인 사용자.
    // 즉 history는 항상 서버(DB) 기록만 사용.
    let history = readInitialHistory("summarize-initial-history");

    function renderHistory() {
        historyList.innerHTML = "";

        history.slice(0, 5).forEach((item) => {
        const li = document.createElement("li");
        const ratio = item.result_data ? item.result_data.summary_ratio : "";
        li.textContent = `[요약비율 ${ratio}%] ${item.output_text}`;
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
        originalLengthEl.textContent = data.original_length;
        summaryLengthEl.textContent = data.summary_length;
        ratioEl.textContent = data.summary_ratio;
        resultTextEl.textContent = data.summary;
    }

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const text = input.value.trim();

        if (text.length < 100) {
        showError("요약할 문서는 100자 이상 입력해주세요.");
        return;
        }

        setSendingState(true);
        errorBox.hidden = true;
        resultBox.hidden = true;

        try {
        const data = await postJSON("/summarize/run/", { text });

        showResult(data);

        history.unshift({
            input_text: text,
            output_text: data.summary,
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