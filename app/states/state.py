import reflex as rx
import json
import logging
from typing import Any
from app.models import (
    Form,
    FormField,
    FieldType,
    TextField,
    EmailField,
    TelField,
    TextareaField,
    SelectField,
    CheckboxField,
    RadioField,
    Option,
)

AVAILABLE_FIELDS = {
    "text": {"icon": "text", "name": "Text"},
    "email": {"icon": "mail", "name": "Email"},
    "tel": {"icon": "phone", "name": "Phone"},
    "textarea": {"icon": "file-text", "name": "Text Area"},
    "select": {"icon": "list", "name": "Dropdown"},
    "checkbox": {"icon": "check-square", "name": "Checkbox"},
    "radio": {"icon": "circle", "name": "Radio Group"},
}


def create_field_from_type(field_type: FieldType) -> FormField:
    field_map = {
        "text": TextField,
        "email": EmailField,
        "tel": TelField,
        "textarea": TextareaField,
        "select": SelectField,
        "checkbox": CheckboxField,
        "radio": RadioField,
    }
    field_class = field_map.get(field_type)
    if field_class:
        return field_class()
    raise ValueError(f"Unknown field type: {field_type}")


class AppState(rx.State):
    """Manages a collection of forms."""

    forms_json: str = rx.LocalStorage("[]", name="forms-data")

    @rx.var
    def forms(self) -> list[Form]:
        try:
            forms_data = json.loads(self.forms_json)
            return [Form.model_validate(form_dict) for form_dict in forms_data]
        except (json.JSONDecodeError, TypeError):
            logging.exception("Error decoding forms JSON")
            return []

    def _save_forms(self):
        self.forms_json = json.dumps([form.model_dump() for form in self.forms])

    @rx.event
    def create_new_form(self):
        new_form = Form(title="Untitled Form")
        self.forms.append(new_form)
        self._save_forms()
        return rx.redirect(f"/editor/{new_form.id}")

    @rx.event
    def delete_form(self, form_id: str):
        self.forms = [form for form in self.forms if form.id != form_id]
        self._save_forms()

    @rx.event
    def get_form(self, form_id: str) -> Form | None:
        for form in self.forms:
            if form.id == form_id:
                return form
        return None

    @rx.event
    def update_form(self, updated_form: Form):
        for i, form in enumerate(self.forms):
            if form.id == updated_form.id:
                self.forms[i] = updated_form
                self._save_forms()
                return


class FormEditorState(rx.State):
    """Manages the state of the form editor for a single form."""

    form: Form | None = None
    selected_field_id: str | None = None

    @rx.var
    def url_form_id(self) -> str:
        return self.router.page.params.get("form_id", "")

    @rx.event
    async def on_load(self):
        """Load the form to be edited based on the URL."""
        app_state = await self.get_state(AppState)
        self.form = app_state.get_form(self.url_form_id)
        if self.form is None:
            return rx.redirect("/")

    async def _save_form_changes(self):
        """Save the current state of the form back to the main AppState."""
        if self.form:
            app_state = await self.get_state(AppState)
            app_state.update_form(self.form)

    @rx.var
    def selected_field(self) -> FormField | None:
        if self.form and self.selected_field_id:
            for field in self.form.fields:
                if field.id == self.selected_field_id:
                    return field
        return None

    @rx.var
    def selected_field_display_name(self) -> str:
        """Get the display name for the selected field type."""
        if self.selected_field:
            field_type = self.selected_field.type
            return AVAILABLE_FIELDS.get(field_type, {"name": field_type})["name"]
        return ""

    @rx.var
    def available_fields(self) -> list[dict[str, str]]:
        return [
            {"type": key, "icon": value["icon"], "name": value["name"]}
            for key, value in AVAILABLE_FIELDS.items()
        ]

    @rx.event
    async def add_field(self, field_type: str):
        if self.form:
            new_field = create_field_from_type(field_type)
            self.form.fields.append(new_field)
            self.selected_field_id = new_field.id
            await self._save_form_changes()

    @rx.event
    def select_field(self, field_id: str):
        self.selected_field_id = (
            None if self.selected_field_id == field_id else field_id
        )

    @rx.event
    async def delete_selected_field(self):
        if self.form and self.selected_field_id:
            self.form.fields = [
                f for f in self.form.fields if f.id != self.selected_field_id
            ]
            self.selected_field_id = None
            await self._save_form_changes()

    @rx.event
    async def update_field_property(self, key: str, value: Any):
        if self.form and self.selected_field_id:
            for i, field in enumerate(self.form.fields):
                if field.id == self.selected_field_id:
                    if isinstance(getattr(field, key), bool):
                        value = (
                            value.lower() == "true"
                            if isinstance(value, str)
                            else bool(value)
                        )
                    setattr(self.form.fields[i], key, value)
                    break
            await self._save_form_changes()

    @rx.event
    async def add_option(self):
        if (
            self.form
            and self.selected_field
            and hasattr(self.selected_field, "options")
        ):
            num_options = len(self.selected_field.options)
            new_option = Option(
                value=f"option{num_options + 1}", label=f"Option {num_options + 1}"
            )
            self.selected_field.options.append(new_option)
            await self.update_field_property("options", self.selected_field.options)

    @rx.event
    async def remove_option(self, index: int):
        if (
            self.form
            and self.selected_field
            and hasattr(self.selected_field, "options")
        ):
            if 0 <= index < len(self.selected_field.options):
                self.selected_field.options.pop(index)
                await self.update_field_property("options", self.selected_field.options)

    @rx.event
    async def update_option_property(self, index: int, key: str, value: str):
        if (
            self.form
            and self.selected_field
            and hasattr(self.selected_field, "options")
        ):
            if 0 <= index < len(self.selected_field.options):
                setattr(self.selected_field.options[index], key, value)
                if key == "label":
                    self.selected_field.options[index].value = value.lower().replace(
                        " ", "_"
                    )
                await self.update_field_property("options", self.selected_field.options)

    @rx.event
    async def update_form_property(self, key: str, value: str):
        if self.form:
            setattr(self.form, key, value)
            await self._save_form_changes()


class FormViewState(rx.State):
    """Manages the public view of a form for submission."""

    form: Form | None = None
    submission_data: dict = {}
    is_submitted: bool = False

    @rx.var
    def url_form_id(self) -> str:
        return self.router.page.params.get("form_id", "")

    @rx.event
    async def on_load(self):
        """Load the form to be viewed."""
        app_state = await self.get_state(AppState)
        self.form = app_state.get_form(self.url_form_id)
        if self.form is None:
            return rx.redirect("/404")

    @rx.event
    def handle_submit(self, form_data: dict):
        self.submission_data = form_data
        self.is_submitted = True
        print("Form Submitted:", form_data)
        yield rx.toast.success("Form submitted successfully!")