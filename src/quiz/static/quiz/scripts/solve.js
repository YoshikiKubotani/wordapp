const QuestionComponent = {
    props: {
        "questionSet": Object,
        "numQuestion": Number,
    },
    template: `
    <h1>👋 問題👋</h1>
    <div class="question"> [[ count+1 ]]. [[ question ]] </div>
    <fieldset>
        <input id="option-1" class="radio-inline__input" type="radio" name="solve-choice[[ count ]]" v-model="radio" v-bind:value="op1" v-bind:disabled="isDisabled" @change="userAttempt"/>
        <label class="radio_label_core" v-bind:class="{radio_label: !isAttempt, disabled: isDisabled && !isOp1, correct: isCorrect && isOp1, wrong: !isCorrect && isOp1}" for="option-1">
            [[ op1 ]]
        </label>
        <input id="option-2" class="radio-inline__input" type="radio" name="solve-choice[[ count ]]" v-model="radio" v-bind:value="op2" v-bind:disabled="isDisabled" @change="userAttempt"/>
        <label class="radio_label_core" v-bind:class="{radio_label: !isAttempt, disabled: isDisabled && !isOp2, correct: isCorrect && isOp2, wrong: !isCorrect && isOp2}" for="option-2">
            [[ op2 ]]
        </label>
        <input id="option-3" class="radio-inline__input" type="radio" name="solve-choice[[ count ]]" v-model="radio" v-bind:value="op3" v-bind:disabled="isDisabled" @change="userAttempt"/>
        <label class="radio_label_core" v-bind:class="{radio_label: !isAttempt, disabled: isDisabled && !isOp3, correct: isCorrect && isOp3, wrong: !isCorrect && isOp3}" for="option-3">
            [[ op3 ]]
        </label>
        <input id="option-4" class="radio-inline__input" type="radio" name="solve-choice[[ count ]]" v-model="radio" v-bind:value="op4" v-bind:disabled="isDisabled" @change="userAttempt"/>
        <label class="radio_label_core" v-bind:class="{radio_label: !isAttempt, disabled: isDisabled && !isOp4, correct: isCorrect && isOp4, wrong: !isCorrect && isOp4}" for="option-4">
            [[ op4 ]]
        </label>
    </fieldset>
    <div id="switch" v-if="showButtons">
        <div id="answer_text" class="center" v-if="isCorrect">
            正解
        </div>
        <div id="display_text" v-if="!isCorrect">
            <div class="left">不正解！正解は</div>
            <div id="answer_text" class="center">
                「[[ answer ]]」
            </div>
            <div class="right">です。</div>
        </div>
        <a href="#" class="btn btn-flat" @click=prevItem><span>前の問題</span></a>
        <a href="#" class="btn btn-flat" @click=nextItem v-if="count < numQuestion-1"><span>次の問題</span></a>
        <a href="result" class="btn btn-finish" @click=Submit v-if="count === numQuestion-1"><span>提出</span></a>
    </div>
        `,
    setup(props) {
        const count = Vue.ref(0)
        const countCorrect = Vue.ref(0)
        const showButtons = Vue.ref(false)
        const question = Vue.ref(props.questionSet[count.value]["question_en"])
        const answer = Vue.ref(props.questionSet[count.value]["answer_jp"])
        const op1 = Vue.ref(props.questionSet[count.value]["option_1"])
        const op2 = Vue.ref(props.questionSet[count.value]["option_2"])
        const op3 = Vue.ref(props.questionSet[count.value]["option_3"])
        const op4 = Vue.ref(props.questionSet[count.value]["option_4"])
        const radio = Vue.ref("")
        const isCorrect = Vue.ref(false)
        const isDisabled = Vue.ref(false)
        const isOp1 = Vue.ref(false)
        const isOp2 = Vue.ref(false)
        const isOp3 = Vue.ref(false)
        const isOp4 = Vue.ref(false)
        const isAttempt = Vue.ref(false)

        const nextItem = () => {
            if (count.value < props.numQuestion-1) {
                count.value ++
                question.value = props.questionSet[count.value]["question_en"]
                answer.value = props.questionSet[count.value]["answer_jp"]
                op1.value = props.questionSet[count.value]["option_1"]
                op2.value = props.questionSet[count.value]["option_2"]
                op3.value = props.questionSet[count.value]["option_3"]
                op4.value = props.questionSet[count.value]["option_4"]
                moveItemUpdates()
            }
        };

        const prevItem = () => {
            if (count.value > 0) {
                count.value --
                question.value = props.questionSet[count.value]["question_en"]
                answer.value = props.questionSet[count.value]["answer_jp"]
                op1.value = props.questionSet[count.value]["option_1"]
                op2.value = props.questionSet[count.value]["option_2"]
                op3.value = props.questionSet[count.value]["option_3"]
                op4.value = props.questionSet[count.value]["option_4"]
                moveItemUpdates()
            }
        };

        const moveItemUpdates = () => {
            showButtons.value = false
            radio.value = ""
            isDisabled.value = false
            isCorrect.value = false
            isOp1.value = false
            isOp2.value = false
            isOp3.value = false
            isOp4.value = false
            isAttempt.value = false
            console.log(count.value)
            console.log(countCorrect.value)
            console.log(question.value)
            console.log(isCorrect.value)
            console.log(isOp1.value)
            console.log(isOp2.value)
            console.log(isOp3.value)
            console.log(isOp4.value)
        }

        const userAttempt = () => {
            isAttempt.value = true
            if (radio.value == answer.value) {
                isCorrect.value = true
                countCorrect.value ++
            }
            else {
                isCorrect.value = false
            }
            showButtons.value = true
            isDisabled.value = true
            isOp1.value = radio.value == op1.value
            isOp2.value = radio.value == op2.value
            isOp3.value = radio.value == op3.value
            isOp4.value = radio.value == op4.value
        }

        const Submit = () => {
            window.sessionStorage.setItem(['count'], [count.value+1]);
            window.sessionStorage.setItem(['countCorrect'], [countCorrect.value]);
            console.log(window.sessionStorage.getItem('count'));
            console.log(window.sessionStorage.getItem('countCorrect'));
        }

        return {
            count,
            countCorrect,
            showButtons,
            question,
            answer,
            op1,
            op2,
            op3,
            op4,
            radio,
            isCorrect,
            isDisabled,
            isOp1,
            isOp2,
            isOp3,
            isOp4,
            isAttempt,
            nextItem,
            prevItem,
            moveItemUpdates,
            userAttempt,
            Submit
        };
    },
    delimiters: ['[[', ']]']
};

app = Vue.createApp({
    components: {
        QuestionComponent
    },
})
app.mount('#app')