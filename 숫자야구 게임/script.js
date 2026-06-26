let attemptsLeft = 9; //남은 횟수 설정
let answer = [] //답안 공간 생성

window.onload = function () {

    let attempts = document.querySelector("#attempts")
    attempts.textContent = attemptsLeft;

    while (answer.length < 3) {
        let random = Math.floor(Math.random() * 10) //숫자 랜덤 생성ㅇ

        if (!answer.includes(random)) {
            answer.push(random);
        }
    }
    console.log(answer)

    let number1 = document.querySelector("#number1") //입력값태그 가져오기
    let number2 = document.querySelector("#number2")
    let number3 = document.querySelector("#number3")
    number1.value = "" //입력값(value)일단 빈칸 설정
    number2.value = ""
    number3.value = ""

    let results = document.querySelector("#results") //결과값태그 가져오기
    results.textContent = ""; //일단 빈칸 설정
}

function check_numbers() {
    let number1 = document.querySelector("#number1")
    let number2 = document.querySelector("#number2")
    let number3 = document.querySelector("#number3")

    let input1 = number1.value //첫 번째 입력칸 안에 적혀 있는 숫자를 가져오는 것
    let input2 = number2.value
    let input3 = number3.value

    if (input1 == "" || input2 == "" || input3 == "") {
        number1.value = ""
        number2.value = ""
        number3.value = ""
        return //함수 종료, 하나라도 빈칸인지 점검
    }

    attemptsLeft = attemptsLeft - 1 //시도 횟수 차감

    let attempts = document.querySelector("#attempts")
    attempts.textContent = attemptsLeft

    let strike = 0
    let ball = 0
    let input = [input1, input2, input3]

    for (let i = 0; i < 3; i++) {
        if (input[i] == answer[i]) {
            strike = strike + 1
        }

        else {
            for (let j = 0; j < 3; j++) {
                if (input[i] == answer[j]) {
                    ball = ball + 1
                }
            }
        }
    }

    let results = document.querySelector("#results")

    if (strike == 0 && ball == 0) {
        results.innerHTML += `
        <div style="display:flex; align-items:center; width:100%; margin-bottom:17px;">
            <div style="margin-right:120px;">
            ${input1} ${input2} ${input3}
            </div>
            <div>
                <span class="out num-result">O</span>
            </div>
        </div>`
    }
    else {
        results.innerHTML += `
        <div style="display:flex; align-items:center; width:100%; margin-bottom:17px;">
            <div style="margin-right:120px;">
                ${input1} ${input2} ${input3}
            </div>
            <div>
                ${strike}
                <span class="strike num-result">S</span>
                ${ball}
                <span class="ball num-result">B</span>
            </div>
        </div>`
    }


    if (strike == 3) {
        let resultImg = document.querySelector("#game-result-img")
        resultImg.src = "success.png"
        let button = document.querySelector(".submit-button")
        button.disabled = true
    }

    if (attemptsLeft == 0 && strike != 3) {
        let resultImg = document.querySelector("#game-result-img")
        resultImg.src = "fail.png"
        let button = document.querySelector(".submit-button")
        button.disabled = true
    }

    number1.value = ""
    number2.value = ""
    number3.value = ""
}
