import json
from typing import List, Optional, Callable, Any


def keyword_callback(word: str, field: str) -> Any:
    pass


def parse_json(json_str: str, keyword_callback: Callable, required_fields: Optional[List[str]] = None,
               keywords: Optional[List[str]] = None) -> None:
    if (required_fields is None) or (keywords is None):
        return

    if not isinstance(json_str, str):
        raise TypeError

    if (not isinstance(required_fields, List)) or (not isinstance(keywords, List)):
        raise TypeError
    else:
        if (not all(isinstance(elem, str) for elem in keywords)) or \
           (not all(isinstance(elem, str) for elem in required_fields)):
            raise TypeError

    if not callable(keyword_callback):
        raise TypeError

    json_doc = json.loads(json_str)

    if not all(isinstance(elem, str) for elem in json_doc.values()):
        raise ValueError("This is non primitive json string")

    for field in json_doc.keys():
        if field not in required_fields:
            continue

        field_value = json_doc[field].split(' ')

        for word in keywords:
            if word in field_value:
                keyword_callback(word, field)
