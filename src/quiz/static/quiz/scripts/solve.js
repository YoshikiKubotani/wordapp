const QuestionComponent = {
    props: {
        "questionSet": Object,
        "numQuestion": Number,
    },
    template: `
    <h1>👋 問題👋</h1>
    <div class="question"> [[ question ]] </div>
    <fieldset>
        <input id="option-1" class="radio-inline__input" type="radio" name="solve-choice[[ count ]]" v-model="radio" v-bind:value="op1" checked="checked"/>
        <label class="radio-inline__label" for="option-1">
            [[ op1 ]]
        </label>
        <input id="option-2" class="radio-inline__input" type="radio" name="solve-choice[[ count ]]" v-model="radio" v-bind:value="op2"/>
        <label class="radio-inline__label" for="option-2">
            [[ op2 ]]
        </label>
        <input id="option-3" class="radio-inline__input" type="radio" name="solve-choice[[ count ]]" v-model="radio" v-bind:value="op3"/>
        <label class="radio-inline__label" for="option-3">
            [[ op3 ]]
        </label>
        <input id="option-4" class="radio-inline__input" type="radio" name="solve-choice[[ count ]]" v-model="radio" v-bind:value="op4"/>
        <label class="radio-inline__label" for="option-4">
            [[ op4 ]]
        </label>
    </fieldset>
    <div id="answer" v-if="!showButtons">
        <a href="#" class="btn btn-3d-circle" @click="showSwitch">
            <span class="btn-3d-circle-content">
                <span class="btn-3d-circle-front">解答</span>
            </span>
            <span class="btn-3d-circle-back"><i class="fas fa-mouse-pointer"></i></span>
        </a>
    </div>
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
        <a href="#" class="btn btn-flat" @click=nextItem><span>次の問題</span></a>
    </div>
        `,
    setup(props) {
        const count = Vue.ref(0)
        const showButtons = Vue.ref(false)
        const question = Vue.ref(props.questionSet[count.value]["question_en"])
        const answer = Vue.ref(props.questionSet[count.value]["answer_jp"])
        const op1 = Vue.ref(props.questionSet[count.value]["option_1"])
        const op2 = Vue.ref(props.questionSet[count.value]["option_2"])
        const op3 = Vue.ref(props.questionSet[count.value]["option_3"])
        const op4 = Vue.ref(props.questionSet[count.value]["option_4"])
        const radio = Vue.ref(op1.value)
        const isCorrect = Vue.ref(false)
        console.log(count.value)

        const nextItem = () => {
            if (count.value < props.numQuestion-1) {
                count.value ++
                question.value = props.questionSet[count.value]["question_en"]
                answer.value = props.questionSet[count.value]["answer_jp"]
                op1.value = props.questionSet[count.value]["option_1"]
                op2.value = props.questionSet[count.value]["option_2"]
                op3.value = props.questionSet[count.value]["option_3"]
                op4.value = props.questionSet[count.value]["option_4"]
                showButtons.value = false
                console.log(count.value)
                console.log(question.value)
                radio.value = op1.value
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
                showButtons.value = false
                console.log(count.value)
                console.log(question.value)
                radio.value = op1.value
            }
        };

        const showSwitch = () => {
            console.log(radio.value)
            console.log(answer.value)
            if (radio.value == answer.value) {
                isCorrect.value = true
            }
            else {
                isCorrect.value = false
            }
            showButtons.value = true
        }

        return {
            showButtons,
            question,
            answer,
            op1,
            op2,
            op3,
            op4,
            radio,
            isCorrect,
            nextItem,
            prevItem,
            showSwitch
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