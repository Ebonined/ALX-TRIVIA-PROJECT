# API Development and Documentation Final Project

## Trivia API Documentation

The API is developed to work with the **Trivia app.** Several endpoints where created as follows;

1. GET `'/categories'`
2. GET `'/questions?page=${integer}'`
3. DELETE ` '/questions/${id}'`
4. POST `'/questions'`
5. POST `'/search_questions'`
6. GET `'/categories/${`id `}/questions'`
7. POST `'/quizzes'`

### 1. GET `'/categories'`

* Fetches: a dictionary of questions categories in which the key corresponds to the ids of a particular category and the values corresponds to the category name in the trivia database
* Resquest Arguments: **None**
* Returns: An Object with single key, `Categories`, containing a values of dictionaries with the format `id: category_string: key: Value_pair`

```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

### 2. GET `'`/questions?page=$`{integer}'`

* Fetches: the pagination of questions,  total Questions, categories and currentcategory
* Request Arguments: `page - integer`
* Returns: An object of keys questions, totalQuestions, categories and currentCategory.

```
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 2
    }
  ],
  "totalQuestions": 100,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": "History"
}

```

### 3. DELETE ` '/questions/${id}'`

* Deletes a particular question by the id of the question
* Request Arguments: id
* Returns: The proper HTTP status code on successful delete or failed delete.

### 4. POST `'/questions'`

* Sends a post request that adds new question to database
* Request Body

```
{
  "question": "Heres a new question string",
  "answer": "Heres a new answer string",
  "difficulty": 1,
  "category": 3
}
```

* Returns: this doesn't return anything

### 5. POST `'/search_questions'`

* Searches for a questions based on the search query provided in the request
* Request Body

```
{
"searchTerm": "Search query goes here"
}
```

* Returns: An object of keys questions, totalQuestions and currentCategory as follows

```
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 5
    }
  ],
  "totalQuestions": 100,
  "currentCategory": "Entertainment"
}
```

### 6. GET `'/categories/${`id `}/questions'`

* Fetches the questions based on a particular category id's
* Request Argument: `id - integer`
* Returns: An object of keys questions, totalQuestions and currentCategory as follows

```
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 5
    }
  ],
  "totalQuestions": 100,
  "currentCategory": "Entertainment"
}
```

### 7. POST `'/quizzes'`

* Select a random question based on category and previous questionsa asked in order to avoid repetition
* Request Body

```
{
    'previous_questions': [1, 4, 20, 15]
    quiz_category': 'current category'
 }
```

* Returns: An object of question as per a partivular category

```
{
    'previous_questions': [1, 4, 20, 15]
    quiz_category': 'current category'
}
```
