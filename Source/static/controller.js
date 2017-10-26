var exampleQuestions = [
  {
    "text": "What types of weather do you like?",
    "type": "multi-choice-response",
    "answers": ["hot weather","warm weather","rainy weather","cool weather","windy weather"]
  },
  {
    "text": "What is your favorite color?",
    "type": "single-response",
    "answers": ["red","blue","green"]
  },
  {
    "text": "What do you like most about animals?",
    "type": "free-response"
  },
  {
    "type" : "end"
  }
]

var app = new Vue({
  el: "#app-4",
  data: {
    mode : "start",
    question : getNextQuestion()
    selectedAnswers: []
  },
  computed: {
    isAnswered: function(){
      return this.selectedAnswers.length != 0;
    }
  },
  methods: {
    getNextQuestion: function(){
      var result = $.ajax({
        type: 'GET',
        url: '/get_next_question',
        success: callback
      })

      var callback = function(data){
        if(this.isAnswered){
          this.question = data
          alert('Wow!')
          this.selectedAnswers = [];

          if(this.question.type === "end"){
            this.mode = 'end';
          }
        } else {
          this.noAnswersError();
        }
      }
    },
    //Change to "previous" question
    getLastQuestion: function(){
      var result = $.ajax({
        type: 'GET',
        url: '/get_prev_question',
        success: callback
      })

      var callback = function(data){
        if(this.isAnswered){
          this.question = data

          this.selectedAnswers = [];

          if(this.question.type === "end"){
            this.mode = 'end';
          }
        } else {
          this.noAnswersError();
        }
       }
    },
    noAnswersError: function(){
      $("#test").css("border", "10px solid red");
    }

    function data() {
    var data = $.ajax({
        url : '/get_next_question',
        type: 'GET'
    });
    this.question = data
    }

  }
})
