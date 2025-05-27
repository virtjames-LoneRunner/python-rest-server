# Api Documentation

## Routes

### '/'

- return

```python
{
    "message": "Welcome to the Word Checker Workshop API!"
}
```

### '/check-word'

- payload

```python
{
    "word": word,
    "participant_name": name
}
```

- return

```python
{
    word: str,
    is_correct: bool,
    message: str,
    participant_name: str = None
}
```

### '/stats`

- return

````python
{
        "total_submissions": total_submissions,
        "correct_submissions": correct_submissions,
        "incorrect_submissions": total_submissions - correct_submissions,
        "success_rate": round(correct_submissions / total_submissions * 100, 2) if total_submissions > 0 else 0
}```
````

### '/submissions'

- return

```python
{
    "submissions": submissions,
    "total_count": len(submissions)
}
```
