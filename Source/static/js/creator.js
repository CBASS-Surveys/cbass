var test1 = {
  "survey_title": "Test Survey",
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
  "survey_properties": {
    "before_text": "Hello, please take the survey",
    "after_text": "Goodbye"
  }
};

var app = new Vue({
  el:"#vueApp",
  data:{
    survey:{
      "survey_title":"",
      "questions":[],
      "survey_properies":{
        "before_text":"",
        "after_text":""
      }
    },
    questionTypes:[
      {
        "value":"multi-choice-response",
        "text": "Multiple Select"
      },
      {
        "value": "single-response",
        "text": "Single Select"
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
        "type":
          {
            "value": "single-response",
            "text": "Single Select"
          },
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
    getSavedJSON: function(json){
      //A check to implement for correctness
      var isCorrect = true;

      if(isCorrect){
        this.survey = json;
      }
    },
    postJSON: function(){

    }
  },
  mounted: function(){
    //this.getSavedJSON(test1);
  }
})
