import inspect
import langchain_core.output_parsers as output_parsers

# Get all classes defined in output_parsers module
parser_classes = inspect.getmembers(output_parsers, inspect.isclass)

# Filter classes that are defined in the output_parsers module itself
parsers_from_module = [
    cls for name, cls in parser_classes 
]

# Print parser class names
for parser in parsers_from_module:
    print(parser.__name__,"-> ", parser.__doc__)


'''

BaseCumulativeTransformOutputParser ->  Base class for an output parser that can handle streaming input.
BaseGenerationOutputParser ->  Base class to parse the output of an LLM call.
BaseLLMOutputParser ->  Abstract base class for parsing the outputs of a model.
BaseOutputParser ->  Base class to parse the output of an LLM call.

    Output parsers help structure language model responses.

    Example:
        .. code-block:: python

            class BooleanOutputParser(BaseOutputParser[bool]):
                true_val: str = "YES"
                false_val: str = "NO"

                def parse(self, text: str) -> bool:
                    cleaned_text = text.strip().upper()
                    if cleaned_text not in (self.true_val.upper(), self.false_val.upper()):
                        raise OutputParserException(
                            f"BooleanOutputParser expected output value to either be "
                            f"{self.true_val} or {self.false_val} (case-insensitive). "
                            f"Received {cleaned_text}."
                        )
                    return cleaned_text == self.true_val.upper()

                @property
                def _type(self) -> str:
                    return "boolean_output_parser"
    
BaseTransformOutputParser ->  Base class for an output parser that can handle streaming input.
CommaSeparatedListOutputParser ->  Parse the output of an LLM call to a comma-separated list.
JsonOutputKeyToolsParser ->  Parse tools from OpenAI response.
JsonOutputParser ->  Parse the output of an LLM call to a JSON object.

    When used in streaming mode, it will yield partial JSON objects containing
    all the keys that have been returned so far.

    In streaming, if `diff` is set to `True`, yields JSONPatch operations
    describing the difference between the previous and the current object.
    
JsonOutputToolsParser ->  Parse tools from OpenAI response.
ListOutputParser ->  Parse the output of an LLM call to a list.
MarkdownListOutputParser ->  Parse a Markdown list.
NumberedListOutputParser ->  Parse a numbered list.
PydanticOutputParser ->  Parse an output using a pydantic model.
PydanticToolsParser ->  Parse tools from OpenAI response.
JsonOutputParser ->  Parse the output of an LLM call to a JSON object.

    When used in streaming mode, it will yield partial JSON objects containing
    all the keys that have been returned so far.

    In streaming, if `diff` is set to `True`, yields JSONPatch operations
    describing the difference between the previous and the current object.

StrOutputParser ->  OutputParser that parses LLMResult into the top likely string.
XMLOutputParser ->  Parse an output using xml format.

'''