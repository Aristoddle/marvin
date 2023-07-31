# Marvin Platform - Action Based Specifications

This document provides an overview of the main components of the Marvin platform, their implementation, top-level use, and developer utility.

## AIModel

`AIModel` is a base class for AI models. It is used to extract structured data from text or generate structured data from text.

### Implementation

`AIModel` is implemented as a Pydantic `BaseModel` with additional methods for extracting and generating data.

### Top-Level Use

```python
from src.marvin.components.ai_model import AIModel

class Location(AIModel):
    city: str
    state: str
    latitude: float
    longitude: float

# Extract structured data from text
location = Location.extract("I live in San Francisco, California.")
print(location.city)  # "San Francisco"
print(location.state)  # "California"

# Generate structured data from text
location = Location.generate("I need a location in California.")
print(location.city)  # Some city in California
print(location.state)  # "California"
```

### Developer Utility

`AIModel` provides a way to leverage AI to parse natural language text into structured data or generate structured data from natural language text.

## ai_classifier

`ai_classifier` is a decorator that is used to transform a regular Enum class into an AIEnum class.

### Implementation

`ai_classifier` is implemented as a Python decorator that adds additional attributes and methods to an Enum class.

### Top-Level Use

```python
from src.marvin.components.ai_classifier import ai_classifier

@ai_classifier
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

# Classify text
color = Color("I like the color of the sky.")
print(color)  # Color.BLUE
```

### Developer Utility

`ai_classifier` provides a way to leverage AI to classify natural language text into predefined categories.

## AIApplication

`AIApplication` is a class that represents a stateful, autonomous, natural language interface to an application.

### Implementation

`AIApplication` is implemented as a Pydantic `BaseModel` with additional attributes and methods for maintaining state and interacting with the application.

### Top-Level Use

```python
from src.marvin.components.ai_application import AIApplication

class TodoApp(AIApplication):
    name = "Todo App"
    description = "A simple todo app."

# Create an instance of the app
app = TodoApp()

# Interact with the app
app("I need to go to the store.")
print(app.state)  # State of the app
print(app.plan)  # Plan of the app
```

### Developer Utility

`AIApplication` provides a way to create a natural language interface to an application that can maintain state and interact with the application autonomously.

## AIFunction

`AIFunction` is a class that represents a Python function with a signature and docstring as a prompt for an AI to predict the function's output.

### Implementation

`AIFunction` is implemented as a Pydantic `BaseModel` with additional methods for predicting function output.

### Top-Level Use

```python
from src.marvin.components.ai_function import ai_fn

@ai_fn
def add(a: int, b: int) -> int:
    """Adds two integers."""

# Predict function output
result = add(1, 2)
print(result)  # 3
```

### Developer Utility

`AIFunction` provides a way to leverage AI to predict the output of a Python function based on its signature and docstring.
