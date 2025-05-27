from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import uvicorn

app = FastAPI(title="Word Checker API", description="Workshop API for checking submitted words")

# Sample word list - replace with your actual words
CORRECT_WORDS = [
    "Python", "coding", "programming", "variables", "functions", "loops",
    "conditionals", "syntax", "debugging", "interpreter", "script", "module",
    "package", "pip", "virtualenv", "IDE", "editor", "terminal", "print", "input",
    "list", "dictionary", "tuple", "set", "string", "integer", "float", "boolean",
    "if", "for", "while", "import", "def", "class", "object", "exception", "try",
    "except", "data", "automation", "file", "open", "read", "write", "append",
    "comment", "indentation", "error", "traceback", "args", "kwargs", "loop",
    "range", "len", "type", "index", "slice", "pop", "append", "extend", "remove",
    "sort", "reverse", "lambda", "map", "filter", "reduce", "comprehension",
    "scope", "global", "local", "return", "None", "True", "False", "is", "in",
    "not", "and", "or", "elif", "assert", "with", "as", "pass", "continue",
    "break", "help", "dir", "zip", "enumerate", "built-in", "standard library"
]


# Pydantic models for request/response
class WordSubmission(BaseModel):
    word: str
    participant_name: str = None

class WordResponse(BaseModel):
    word: str
    is_correct: bool
    message: str
    participant_name: str = None

# Store submissions (in production, use a proper database)
submissions: List[Dict] = []

@app.get("/")
async def root():
    """Welcome endpoint"""
    return {"message": "Welcome to the Word Checker Workshop API!"}

@app.post("/check-word", response_model=WordResponse)
async def check_word(submission: WordSubmission):
    """
    Check if the submitted word is correct
    """
    word = submission.word.lower().strip()

    if not word:
        raise HTTPException(status_code=400, detail="Word cannot be empty")

    is_correct = word in CORRECT_WORDS

    # Store the submission
    submission_record = {
        "word": word,
        "participant_name": submission.participant_name,
        "is_correct": is_correct
    }
    submissions.append(submission_record)

    message = "Correct! Well done!" if is_correct else "Sorry, that's not quite right. Try again!"

    return WordResponse(
        word=word,
        is_correct=is_correct,
        message=message,
        participant_name=submission.participant_name
    )

@app.get("/words")
async def get_word_list():
    """
    Get the list of correct words (for workshop organizers)
    """
    return {"correct_words": sorted(list(CORRECT_WORDS))}

@app.get("/submissions")
async def get_submissions():
    """
    Get all submissions (for workshop organizers)
    """
    return {"submissions": submissions, "total_count": len(submissions)}

@app.get("/stats")
async def get_stats():
    """
    Get workshop statistics
    """
    total_submissions = len(submissions)
    correct_submissions = sum(1 for s in submissions if s["is_correct"])

    return {
        "total_submissions": total_submissions,
        "correct_submissions": correct_submissions,
        "incorrect_submissions": total_submissions - correct_submissions,
        "success_rate": round(correct_submissions / total_submissions * 100, 2) if total_submissions > 0 else 0
    }

@app.post("/add-word")
async def add_word(word: str):
    """
    Add a new word to the correct words list (for workshop organizers)
    """
    word = word.lower().strip()
    if word in CORRECT_WORDS:
        return {"message": f"Word '{word}' already exists in the list"}

    CORRECT_WORDS.add(word)
    return {"message": f"Word '{word}' added successfully", "total_words": len(CORRECT_WORDS)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)