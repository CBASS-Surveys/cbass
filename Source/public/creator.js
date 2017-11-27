var app = new Vue({
  el:"#vueApp",
  data:{
    survey:{
      "surveyTitle":"",
      "questions":[],
      "surveyProperies":{
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
    }
  }
})
