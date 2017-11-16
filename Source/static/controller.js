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

var startingProperties = {
  "name": "Survey Name Not Currently Available",
  "properties": {
    "before_text":"none",
    "after_text":"none"
  }
}

var app = new Vue({
  el: "#app-4",
  data: {
    mode : "start",
    question : {},
    testCounter : 0,
    selectedAnswers: [],
    surveyProperies: {
      "name": "Survey Name Not Currently Available",
      "properties": {
        "before_text":"none",
        "after_text":"none"
      }
    }
  },
  created: function() {
    var result = $.ajax({
      type: 'GET',
      url: '/get_properties',
      success: function(data){
        if(data.type != "error"){
          console.log(data)
          startingProperties = data
          app.surveyProperies = data
        }
      }
    })
  },
  computed: {
    isAnswered: function(){
      return this.selectedAnswers.length != 0;
    },
    formatedAnswers: function(){
      return JSON.stringify(this.selectedAnswers)
      /*var temp = [];
      for(var i = 0; i < this.selectedAnswers.length; i++){
        temp.push(this.selectedAnswers[i]);
        return temp;
      }*/
    }
  },
  methods: {
    getNextQuestion: function(){

      var self = this;

      if(self.isAnswered){

      $.ajax({
        url:'/get_next_question',
        type: "POST",
        data: JSON.stringify(this.selectedAnswers),
        dataType: "JSON",
        contentType: "application/json; charset=utf-8",
        success: function(data){
          console.log(data)
          self.question = data;
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
      /*

      TODO: Implement previous question functionality

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
      }*/
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
    startSurvey: function(){
      var self = this;

      self.mode = 'survey'

      $.get('/get_next_question',
        function(data){
          console.log(data)
          self.question = data;
          self.selectedAnswers = [];
          if(self.question.type === "end"){
            self.mode = 'end';
          }
      })
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
