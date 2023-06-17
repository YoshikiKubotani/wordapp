const ResultComponent = {
    template: `
    <h3> [[ countCorrect ]]/[[ count ]] </h3>
    `,
    setup() {
        const count = Vue.ref(window.sessionStorage.getItem(['count']))
        const countCorrect = Vue.ref(window.sessionStorage.getItem(['countCorrect']))

        return {
            count,
            countCorrect,
        };
    },
    delimiters: ['[[', ']]'],
};

app = Vue.createApp({
    components: {
        ResultComponent
    },
});
app.mount('#vue');