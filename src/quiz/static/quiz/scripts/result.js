// const ResultComponent = {
//     template: `
//     <h3> [[ countCorrect ]]/[[ count ]] </h3>
//     `,
//     setup() {
//         const count = Vue.ref(window.sessionStorage.getItem(['count']))
//         const countCorrect = Vue.ref(window.sessionStorage.getItem(['countCorrect']))

//         return {
//             count,
//             countCorrect,
//         };
//     },
//     delimiters: ['[[', ']]'],
// };

// app = Vue.createApp({
//     components: {
//         ResultComponent
//     },
// });
// app.mount('#vue');


let total = window.sessionStorage.getItem(['count']); // 総問題数
let correct = window.sessionStorage.getItem(['countCorrect']); // 正解数

// スコアボードに数値を設定
// document.getElementById('total').textContent = total;
// document.getElementById('correct').textContent = correct;
document.getElementById('result').textContent = `${total}問中${correct}問正解！`;

// 正解数に応じたメッセージを設定
let message = '';
if (correct === total) {
    message = 'Perfect! Great job!';
} else if (correct >= total * 0.8) {
    message = 'Well done! You did pretty good.';
} else {
    message = 'Keep practicing! You can do better.';
}
document.getElementById('score-message').textContent = message;

// 問題リストを動的に生成
let questions = [
    { question: 'Question 1', correct: true },
    { question: 'Question 2', correct: false },
    // ...他の問題
];
let questionList = document.getElementById('question-list');
questions.forEach((q, index) => {
    let listItem = document.createElement('li');
    listItem.textContent = `Question ${index + 1}: ${q.question}`;
    listItem.classList.add(q.correct ? 'correct' : 'incorrect');
    questionList.appendChild(listItem);
});
