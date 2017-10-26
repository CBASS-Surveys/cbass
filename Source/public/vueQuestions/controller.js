var exampleQuestions = [
  {
    "text": "What types of weather do you like?",
    "type": "multi",
    "answers": ["hot weather","warm weather","rainy weather","cool weather","windy weather"]
  },
  {
    "text": "What is your favorite color?",
    "type": "single",
    "answers": ["red","blue","green"]
  },
  {
    "text": "What do you like most about animals?",
    "type": "text"
  },
  {
    "type" : "end"
  }
]

var app = new Vue({
  el: "#app-4",
  data: {
    mode : "start",
    question : exampleQuestions[0],
    tempCounter : 0,
    selectedAnswers: []
  },
  computed: {
    isAnswered: function(){
      return this.selectedAnswers.length != 0;
    }
  },
  methods: {
    getNextQuestion: function(){
      if(this.isAnswered){
        if(this.tempCounter < exampleQuestions.length-1){
          this.tempCounter++
          this.question = exampleQuestions[this.tempCounter]
        }
        console.log(this.selectedAnswers)
        this.selectedAnswers = [];
        if(this.question.type === "end"){
          this.mode = 'end';
        }
      } else {
        this.noAnswersError();
      }
    },
    getLastQuestion: function(){
      if(this.tempCounter > 0){
        this.tempCounter--
        this.question = exampleQuestions[this.tempCounter]
      }
    },
    noAnswersError: function(){
      $("#test").css("border", "10px solid red");
    }
  }
})
