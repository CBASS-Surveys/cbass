var test1 = {
  "title": "Test Survey",
  "questions": [
    {
      "text": "Question One",
      "type": "single-response",
      "answers": [
        {
          "value": "Red",
          "description": "Q1R3"
        },
        {
          "value": "Blue",
          "description": "Q1R2"
        },
        {
          "value": "Green",
          "description": "Q1R3"
        }
      ],
      "constraints": [
        {
          "question_from": 0,
          "response_from": 0,
          "type": "modify",
          "question_to": 2,
          "responses_discluded": [
            0,
            1,
            2
          ]
        },
        {
          "question_from": 0,
          "response_from": 1,
          "type": "modify",
          "question_to": 2,
          "responses_discluded": [
            3
          ]
        },
        {
          "question_from": 0,
          "response_from": 2,
          "type": "forbids",
          "question_to": 1,
          "responses_discluded": []
        }
      ]
    },
    {
      "text": "Question Two",
      "type": "free-response",
      "answers": [],
      "constraints": []
    },
    {
      "text": "Question Three",
      "type": "multi-choice-response",
      "answers": [
        {
          "value": "Snakes",
          "description": "Q3R1"
        },
        {
          "value": "Spiders",
          "description": "Q3R2"
        },
        {
          "value": "Frogs",
          "description": "Q3R3"
        },
        {
          "value": "Lizard",
          "description": "Q3R4"
        }
      ],
      "constraints": []
    }
  ],
  "properties": {
    "before_text": "Hello, please take the survey",
    "after_text": "Goodbye"
  }
};

var trimConstraints = function(json){
  var constraints = [];
  for(var i = 0; i < json.questions.length; i++){
    constraints.concat(json.questions.constraints);
  }
  var result = JSON.parse(JSON.stringify(json));
  result.constraints = constraints;
  return result;
}

var app = new Vue({
  el:"#vueApp",
  data:{
    survey:{
      "title":"",
      "questions":[],
      "properties":{
        "before_text":"",
        "after_text":""
      }
    },
    questionTypes:[
      {
        "value": "single-response",
        "text": "Single Select"
      },
      {
        "value":"multi-choice-response",
        "text": "Multiple Select"
      },
      {
        "value": "free-response",
        "text": "Free Response"
      }
    ],
    constraintTypes: [
      {
        "value":"forbids",
        "text": "Forbids"
      },
      /*{
        "value": "single-response",
        "text": "Single Select"
      },*/
      {
        "value": "modify",
        "text": "Modify"
      }
    ]
  },
  computed:{
    surveyLength : function(){
      return this.survey.questions.length;
    }
  },
  methods:{
    addQuestion: function(){
      this.survey.questions.push({
        "text":"",
        "type": this.questionTypes[0],
        "answers":[],
        "constraints":[]
      })
    },
    addAnswer: function(index){
      this.survey.questions[index].answers.push({
        "value":"",
        "description":""
      })
    },
    addConstraint: function(index){
      this.survey.questions[index].constraints.push({
        "question_from":index,
        "response_from":-1,
        "type":"require",
        "question_to":-1,
        "responses_discluded":[]
      })
    },
    //Caution: Deletion of data can cause problems with constraint referencing.
    //Look into solutions to this problem
    deleteQuestion: function(qIndex){
        this.survey.questions.splice(qIndex, 1);
    },
    deleteAnswer: function(qIndex, aIndex){
      this.survey.questions[qIndex].answers.splice(aIndex, 1);
    },
    deleteConstraint: function(qIndex, cIndex){
      this.survey.questions[qIndex].constraints.splice(cIndex, 1);
    },
    getSavedJSON: function(json){
      //A check to implement for correctness
      var isCorrect = true;

      if(isCorrect){
        this.survey = json;
      }
    },
    saveSurvey: function(){
      $.ajax({
        url:'/save_survey',
        type: "POST",
        data: JSON.stringify(this.survey),
        dataType: "JSON",
        contentType: "application/json; charset=utf-8",
        success: function(data){
          console.log(data)
        }
      })
    },
    publishSurvey: function(){
      $.ajax({
        url:'/save_survey',
        type: "POST",
        data: JSON.stringify(trimConstraints(this.survey)),
        dataType: "JSON",
        contentType: "application/json; charset=utf-8",
        success: function(data){
          console.log(data)
        }
      })
    }
  },
  mounted: function(){
    /*$.ajax({
      url:'/load_survey=2',
      type: "GET",
      contentType: "application/json; charset=utf-8",
      success: function(data){
        app.getSavedJSON(data);
      }
    })*/
    this.getSavedJSON(test1);
  }
})
