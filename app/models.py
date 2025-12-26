import reflex as rx
from typing import Literal, Union, Optional
import uuid
from pydantic import BaseModel, Field as PydanticField


def generate_uuid_str() -> str:
    """Generate a UUID and return it as a string."""
    return str(uuid.uuid4())


FieldType = Literal["text", "email", "tel", "textarea", "select", "checkbox", "radio"]


class BaseField(BaseModel):
    id: str = PydanticField(default_factory=generate_uuid_str)
    type: FieldType
    label: str = "New Field"
    required: bool = False


class TextField(BaseField):
    type: Literal["text"] = "text"
    placeholder: str = "Enter text..."


class EmailField(BaseField):
    type: Literal["email"] = "email"
    placeholder: str = "Enter email..."


class TelField(BaseField):
    type: Literal["tel"] = "tel"
    placeholder: str = "Enter phone number..."


class TextareaField(BaseField):
    type: Literal["textarea"] = "textarea"
    placeholder: str = "Enter a longer message..."


class Option(BaseModel):
    value: str
    label: str


class SelectField(BaseField):
    type: Literal["select"] = "select"
    options: list[Option] = [
        Option(value="option1", label="Option 1"),
        Option(value="option2", label="Option 2"),
    ]


class CheckboxField(BaseField):
    type: Literal["checkbox"] = "checkbox"
    checked: bool = False


class RadioField(BaseField):
    type: Literal["radio"] = "radio"
    options: list[Option] = [
        Option(value="option1", label="Option 1"),
        Option(value="option2", label="Option 2"),
    ]


FormField = Union[
    TextField,
    EmailField,
    TelField,
    TextareaField,
    SelectField,
    CheckboxField,
    RadioField,
]


class Form(BaseModel):
    id: str = PydanticField(default_factory=generate_uuid_str)
    title: str = "My Custom Form"
    description: str = "This is a form that can be customized."
    fields: list[FormField] = []