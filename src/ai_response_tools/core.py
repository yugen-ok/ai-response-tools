

import json
from json import JSONDecodeError
from typing import Any, Iterator, Optional
import os

from urllib.parse import urlparse
import base64
from chompjs import parse_js_object
from jsonschema.validators import Draft7Validator
from lbgpt.types import ChatCompletionAddition
from openai.types.chat import ChatCompletion
import openai
import diskcache

import lbgpt

cache = diskcache.Cache('lbgpt_cache')


ChatCompletionTypes = ChatCompletionAddition | ChatCompletion



# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def image_path_or_url_to_url(image_path_or_url):
    if not is_url(image_path_or_url):
        base64_image = encode_image(image_path_or_url)
        return f"data:image/jpeg;base64,{base64_image}"
    else:
        return image_path_or_url


def is_url(path):
    try:
        result = urlparse(path)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


import os
import lbgpt
import openai
import logging


def query_lbgpt(
        system_prompt: str,
        user_prompts: list[str] = None,
        image_urls: list[str] = None,
        model: str = 'gpt-4o',
        temperature: float = 0.7,
        max_tokens: int = 4000,
        use_azure: bool = True,
        cache=None
) -> list[str]:
    """
    Query a language model (Azure or OpenAI) via lbgpt with optional image support.
    Handles exceptions gracefully so that a failure in one request doesn't break the whole process.

    Parameters:
        system_prompt (str): The system-level instruction to guide the model.
        user_prompts (list[str]): A list of user prompts (one prompt per request).
        image_urls (list[str], optional): A list of image URLs corresponding to each user prompt.
                                          If provided, must be the same length as user_prompts.
        model (str): The model name, defaults to 'gpt-4o'.
        temperature (float): The temperature for response variability.
        max_tokens (int): Max tokens in the response.
        use_azure (bool): Whether to use Azure GPT endpoint or OpenAI endpoint.
        cache: Optional cache object for lbgpt.

    Returns:
        list[str]: A list of generated responses from the model, one per prompt.
    """

    if user_prompts is None:
        user_prompts = [""]

    logging.basicConfig(level=logging.ERROR)

    # Setup client
    try:
        if use_azure:
            lbgpt_client = lbgpt.AzureGPT(
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                azure_api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
                azure_model_map={model: model},
                max_parallel_calls=100,
                cache=cache
            )
        else:
            lbgpt_client = lbgpt.ChatGPT(
                api_key=openai.api_key,
                max_parallel_calls=100,
                cache=cache
            )
    except Exception as e:
        logging.error(f"Failed to initialize lbgpt client: {e}")
        return ["Error initializing GPT client"] * len(user_prompts)

    # Validate image and prompt alignment
    if image_urls:
        assert len(user_prompts) == len(image_urls), "Number of prompts and image URLs must match"

    responses = []

    for i, prompt in enumerate(user_prompts):
        try:
            request_data = {
                "model": model,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": [{"type": "text", "text": prompt}]}
                ],
            }

            if image_urls:
                request_data["messages"][1]["content"].append({
                    "type": "image_url",
                    "image_url": {"url": image_path_or_url_to_url(image_urls[i])}
                })

            response = lbgpt_client.chat_completion_list([request_data], show_progress=False)
            responses.append(response[0].choices[0].message.content)

        except Exception as e:
            logging.error(f"Error processing prompt {i}: {e}")
            responses.append(f"Error processing prompt {i}")

    return responses


def chatgpt_raw_response_parsing(
    response: ChatCompletionTypes,
    raise_exception_on_irregular_finish: bool = False,
) -> Optional[str]:
    """
    Parses the raw response from a ChatGPT API call and extracts the message content.
    Handles unexpected finish reasons by either raising an exception or logging a
    warning based on the given parameters.

    Parameters:
    response: ChatCompletionTypes
        The raw response object from the ChatGPT API call containing choices and
        finish reasons.
    raise_exception_on_irregular_finish: bool, optional
        A flag to determine if an exception should be raised when the finish
        reason is not 'stop'. Defaults to False.

    Returns:
    Optional[str]
        The content of the message if the finish reason is 'stop'; otherwise, None.
    """
    if response.choices[0].finish_reason != "stop":
        if raise_exception_on_irregular_finish:
            raise ValueError(
                "Unexpected finish reason: {}".format(response.choices[0].finish_reason)
            )
        else:
            print("Unexpected finish reason: {}. Returning `None`".format(
                    response.choices[0].finish_reason
                ))
        return

    return response.choices[0].message.content


def _iter_over_all_items(d: list | dict) -> Iterator[list | dict]:
    """Iterate over all items in a list or dictionary, returning the items."""
    # yield the self item if it is a valid item type, otherwise return
    if isinstance(d, (list, dict)):
        yield d
    else:
        return

    # yield the children
    if isinstance(d, list):
        for item in d:
            yield from _iter_over_all_items(item)
    elif isinstance(d, dict):
        for value in d.values():
            yield from _iter_over_all_items(value)


def fuzzy_parse_json(json_string: str) -> dict[str, Any]:
    try:
        return json.loads(json_string)
    except JSONDecodeError:
        # this is just returning the first JS object it encounters in the string.
        # may want to extend it eventually if it is an issue to return the `largest` object.
        return parse_js_object(json_string)


def response_parsing(
    response: ChatCompletionTypes | str,
    response_schema: Optional[dict[str, Any]] = None,
    element_schema: Optional[dict[str, Any]] = None,
    raise_exception_on_irregular_finish: bool = False,
) -> list[dict] | dict | None:
    """
    Parses a response into a structured format based on optional schemas. The function
    handles responses that are either strings or of type ChatCompletion. It can perform
    parsing based on provided JSON schemas, either for the entire response or individual
    elements within the response. The function also supports handling irregular completion
    flags in responses and raises exceptions for unexpected input types or conflicting
    schema specifications.

    Parameters:
        response: The input to be parsed, which can be a ChatCompletion object or a raw
            response string.
        response_schema: An optional dictionary defining a JSON schema for validating the
            entire parsed response.
        element_schema: An optional dictionary defining a JSON schema for validating
            individual elements within the parsed response.
        raise_exception_on_irregular_finish: A boolean flag indicating whether an
            exception should be raised for responses with irregular completion.

    Returns:
        A list of dictionaries, a single dictionary, or None depending on the schema
        provided and the contents of the response.

    Raises:
        NotImplementedError: If the response is neither a ChatCompletion object nor a
            string.
        ValueError: If both response_schema and element_schema are specified.
    """
    if isinstance(response, ChatCompletion):
        txt = chatgpt_raw_response_parsing(
            response, raise_exception_on_irregular_finish
        )
        if txt is None:
            return
    elif isinstance(response, str):
        txt = response
    else:
        raise NotImplementedError(
            "Cannot parse response of type {}".format(type(response))
        )

    fuzzy_parsed_object = fuzzy_parse_json(txt)

    if response_schema is not None and element_schema is not None:
        raise ValueError(
            "Cannot specify both response_schema and element_schema. Please specify at most one."
        )

    elif response_schema is not None:
        # setting up the json schema properly
        validator = Draft7Validator(response_schema)

        # returning the first element that matches the schema
        for ppjo in _iter_over_all_items(fuzzy_parsed_object):
            if validator.is_valid(ppjo):
                return ppjo

    elif element_schema is not None:
        # setting up the json schema properly
        validator = Draft7Validator(element_schema)

        # returning all elements that match the schema
        res = list()
        for ppjo in _iter_over_all_items(fuzzy_parsed_object):
            if validator.is_valid(ppjo):
                res.append(ppjo)

        return res

    else:
        return fuzzy_parsed_object
