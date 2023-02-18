const QuestionComponent = {
    props: {
        "questionSet": Object,
        "numQuestion": Number,
    },
    template: `
    <h1>👋 問題👋</h1>
    <div class="question"> [[ question ]] </div>
    <fieldset>
        <input id="option-1" class="radio-inline__input" type="radio" name="solve-choice[[ count ]]" value="[[ op1 ]]" checked="checked"/>
        <label class="radio-inline__label" for="option-1">
            [[ op1 ]]
        </label>
        <input id="option-2" class="radio-inline__input" type="radio" name="solve-choice[[ count ]]" value="[[ op2 ]]"/>
        <label class="radio-inline__label" for="option-2">
            [[ op2 ]]
        </label>
        <input id="option-3" class="radio-inline__input" type="radio" name="solve-choice[[ count ]]" value="[[ op3 ]]"/>
        <label class="radio-inline__label" for="option-3">
            [[ op3 ]]
        </label>
        <input id="option-4" class="radio-inline__input" type="radio" name="solve-choice[[ count ]]" value="[[ op4 ]]"/>
        <label class="radio-inline__label" for="option-4">
            [[ op4 ]]
        </label>
    </fieldset>
    <div id="switch">
        <a href="#" class="btn btn-flat" @click=prevItem><span>前の問題</span></a>
        <a href="#" class="btn btn-flat" @click=nextItem><span>次の問題</span></a>
    </div>
        `,
    setup(props) {
        const count = Vue.ref(0)
        const question = Vue.ref(props.questionSet[count.value]["question_en"])
        const answer = Vue.ref(props.questionSet[count.value]["answer_jp"])
        const op1 = Vue.ref(props.questionSet[count.value]["option_1"])
        const op2 = Vue.ref(props.questionSet[count.value]["option_2"])
        const op3 = Vue.ref(props.questionSet[count.value]["option_3"])
        const op4 = Vue.ref(props.questionSet[count.value]["option_4"])
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
                console.log(count.value)
                console.log(question.value)
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
                console.log(count.value)
                console.log(question.value)
            }
        };

        return {
            question,
            answer,
            op1,
            op2,
            op3,
            op4,
            nextItem,
            prevItem
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