function getCookie(name) {
    const cookies = document.cookie ? document.cookie.split(";") : [];

    for (const cookieValue of cookies) {
        const cookie = cookieValue.trim();
        if (cookie.startsWith(`${name}=`)) {
        return decodeURIComponent(cookie.substring(name.length + 1));
        }
    }

    return null;
    }

    async function postJSON(url, data) {
    const response = await fetch(url, {
        method: "POST",
        headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify(data),
    });

    const body = await response.json().catch(() => ({}));

    if (!response.ok) {
        throw new Error(body.error || `요청에 실패했습니다. (${response.status})`);
    }

    return body;
    }

    function readInitialHistory(elementId) {
    const el = document.getElementById(elementId);
    if (!el) {
        return [];
    }
    try {
        return JSON.parse(el.textContent);
    } catch {
        return [];
    }
}