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
          startingProperties = data
          app.surveyProperies = data
          document.title = data.name;
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
    getLastQuestion: function(){},
    noAnswersError: function(){
      $("#test").css("border", "10px solid red");
    },
    startSurvey: function(){
      var self = this;

      self.mode = 'survey'

      $.get('/get_next_question',
        function(data){
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
