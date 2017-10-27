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
    testCounter : 0,
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

      $.post('/get_next_question',
        self.selectedAnswers,
        function(data){
          console.log("data")
          self.question = data
          self.selectedAnswers = [];
          if(self.question.type === "end"){
            self.mode = 'end';
          }
      })
      } else {
        app.noAnswersError();
      }
    },
    getNextTestQuestion: function(){
      var self = this;

      if(self.isAnswered){
        self.testCounter++
        self.question = exampleQuestions[self.testCounter]
        self.selectedAnswers = [];
        if(self.question.type === "end"){
          self.mode = 'end';
        }
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
    getLastTestQuestion: function(){
      var self = this;

      if(self.testCounter > 0){
        self.testCounter--
        self.question = exampleQuestions[self.testCounter]
        self.selectedAnswers = [];
      }
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
