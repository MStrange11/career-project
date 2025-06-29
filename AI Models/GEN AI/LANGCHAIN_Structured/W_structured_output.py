from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from typing import Literal, Optional, TypedDict, Annotated
from pydantic import BaseModel, Field
import json

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# schema for structured output
class Review1(TypedDict):
    summary: str
    sentiment: str


# Schema for structured output using Pydantic
class Review2(BaseModel):
    summary: str
    sentiment: str
    

# Schema for structured output using Pydantic
class Review3(BaseModel):
    summary: Annotated[str, "A brief summary of the review"]
    sentiment: Annotated[str, "Return sentiment of the review either neutral, positive or negative"]


class Review4(BaseModel):
    key_themes: Annotated[list[str], "Write down all the key themes discussed in the review"]
    summary: Annotated[str, "A brief summary of the review"]
    sentiment: Annotated[Literal[ "pos", "neg"], "Return sentiment of the review either neutral, positive or negative"]
    pros: Annotated[Optional[list[str]], "Write down all the pros inside a list"]
    cons: Annotated[Optional[list[str]], "Write down all the cons inside a list"]
    name : Annotated[Optional[str], "Name of the reviewer, only if available"]
    date: Annotated[Optional[str], "Date of the review, only if available"]


class Review5(BaseModel):
    key_themes: list[str] = Field(description="Write down all the key themes discussed in the review")
    summary: str = Field( description="A brief summary of the review")
    sentiment: Literal["pos", "neg"] = Field(description="Return sentiment of the review either neutral, positive or negative")
    pros: Optional[list[str]] = Field(None, description="Write down all the pros inside a list")
    cons: Optional[list[str]] = Field(None, description="Write down all the cons inside a list")
    name: Optional[str] = Field(None, description="Name of the reviewer, only if available")
    date: Optional[str] = Field(None, description="Date of the review, only if available")
    rating: Optional[int] = Field(None, description="Rating out of 5, only if available")




# we can use the schema to define the structured output
structured_output = model.with_structured_output(Review5)


res = structured_output.invoke("""I recently upgraded to the Samsung Galaxy S24 Ultra, and I must say, it's an absolute powerhouse! The Snapdragon 8 Gen 3
processor makes everything lightning fast-whether I'm gaming, multitasking, or editing photos. The 5000mAh battery easily lasts a full day even with heavy use, and the 45W fast charging is a lifesaver.

The S-Pen integration is a great touch for note-taking and quick sketches, though I don't use it often. What really blew me away is the 200MP camera-the night mode is stunning, capturing crisp, vibrant images even in low light. Zooming up to 100x actually works well for distant objects, but anything beyond 30x loses quality.

However, the weight and size make it a bit uncomfortable for one-handed use. Also, Samsung's One UI still comes with bloatware-why do I need five different Samsung apps for things Google already provides? The $1,300 price tag is also a hard pill to swallow.

Pros:
Insanely powerful processor (great for gaming and productivity)
Stunning 200MP camera with incredible zoom capabilities
Long battery life with fast charging
S-Pen support is unique and useful

Cons :
Bulky and heavy-not great for one-handed use
Bloatware still exists in One UI
Expensive compared to competitors
                               
reviewed by MStrange  
""")

# we get a class instance with the attributes defined in the schema
# print(res, type(res))

# summary="The hardware is great, but the software feels bloated. There are too many pre-installed apps that I can't remove. Also, the UI looks outdated compared to other brands. Hoping for a software update to fix this." sentiment='negative'

for key in res.model_dump().keys():
    print(f"{key}: {res.model_dump().get(key)}")
