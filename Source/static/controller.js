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
    question : exampleQuestions[0],
    selectedAnswers: []
  },
  computed: {
    isAnswered: function(){
      return this.selectedAnswers.length != 0;
    }
  },
  methods: {
    getNextQuestion: function(){

      var self = this;

      if(self.isAnswered){

      var result = $.ajax({
        type: 'GET',
        url: '/get_next_question',
        success: function(data){
          console.log("data")

            self.question = data
            alert('Wow!')
            self.selectedAnswers = [];

            if(self.question.type === "end"){
              self.mode = 'end';
            }
          }
      })
      } else {
        app.noAnswersError();
      }
    },
    //Change to "previous" question
    getLastQuestion: function(){
      var self = this;
      var result = $.ajax({
        type: 'GET',
        url: '/get_prev_question',
        success: function(data){
          //implement for what gets returned when there is no previous question
          if(data.type != "error"){
            console.log(data)
            self.question = data
            self.selectedAnswers = [];
            if(self.question.type === "end"){
              self.mode = 'end';
            }
          }
        }
      })
    },
    noAnswersError: function(){
      $("#test").css("border", "10px solid red");
    },

    data: function() {
    var data = $.ajax({
        url : '/get_next_question',
        type: 'GET'
    });
    this.question = data
    }
  }
})
