import reflex as rx
from app.models import (
    FormField,
    TextField,
    EmailField,
    TelField,
    TextareaField,
    SelectField,
    CheckboxField,
    RadioField,
    Option,
)
from app.states.state import FormEditorState


def render_field(field: FormField) -> rx.Component:
    """Renders a form field based on its type for the canvas preview."""
    base_class = "w-full p-3 border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
    label_class = "block text-sm font-medium text-gray-700 mb-1"
    common_props = {
        "is_disabled": True,
        "placeholder": rx.cond(hasattr(field, "placeholder"), field.placeholder, ""),
    }
    field_component = rx.match(
        field.type,
        ("text", rx.el.input(type="text", class_name=base_class, **common_props)),
        ("email", rx.el.input(type="email", class_name=base_class, **common_props)),
        ("tel", rx.el.input(type="tel", class_name=base_class, **common_props)),
        ("textarea", rx.el.textarea(class_name=base_class, **common_props)),
        (
            "select",
            rx.el.select(
                rx.foreach(
                    field.options, lambda opt: rx.el.option(opt.label, value=opt.value)
                ),
                class_name=base_class,
                is_disabled=True,
            ),
        ),
        (
            "checkbox",
            rx.el.div(
                rx.el.input(
                    type="checkbox",
                    is_disabled=True,
                    class_name="h-4 w-4 text-purple-600 border-gray-300 rounded focus:ring-purple-500",
                ),
                class_name="flex items-center h-12",
            ),
        ),
        (
            "radio",
            rx.el.div(
                rx.foreach(
                    field.options,
                    lambda opt: rx.el.label(
                        rx.el.input(
                            type="radio",
                            name=field.id,
                            is_disabled=True,
                            class_name="h-4 w-4 text-purple-600 border-gray-300 focus:ring-purple-500",
                        ),
                        rx.el.span(opt.label, class_name="ml-2 text-gray-700"),
                        class_name="flex items-center mr-4",
                    ),
                ),
                class_name="flex items-center h-12",
            ),
        ),
        rx.el.p(f"Unknown field type: {field.type}"),
    )
    return rx.el.div(
        rx.el.label(
            field.label,
            rx.cond(field.required, rx.el.span(" *", class_name="text-red-500"), ""),
            class_name=label_class,
        ),
        field_component,
        class_name="w-full",
    )


def canvas_field_wrapper(field: FormField) -> rx.Component:
    """A wrapper for a field on the canvas, making it selectable."""
    is_selected = FormEditorState.selected_field_id == field.id
    return rx.el.div(
        render_field(field),
        on_click=lambda: FormEditorState.select_field(field.id),
        class_name=rx.cond(
            is_selected,
            "relative p-4 rounded-lg cursor-pointer border-2 border-purple-500 bg-purple-50",
            "relative p-4 rounded-lg cursor-pointer border-2 border-transparent hover:border-gray-300",
        ),
    )


def form_canvas() -> rx.Component:
    """The central area where the form is built by dropping fields."""
    return rx.el.main(
        rx.el.div(
            rx.el.div(
                rx.el.input(
                    on_change=lambda val: FormEditorState.update_form_property(
                        "title", val
                    ),
                    placeholder="Form Title",
                    class_name="text-3xl font-bold w-full p-2 rounded-lg hover:bg-gray-100 focus:bg-gray-100 outline-none",
                    default_value=FormEditorState.form.title,
                ),
                rx.el.input(
                    on_change=lambda val: FormEditorState.update_form_property(
                        "description", val
                    ),
                    placeholder="Form Description...",
                    class_name="text-gray-600 w-full mt-2 p-2 rounded-lg hover:bg-gray-100 focus:bg-gray-100 outline-none",
                    default_value=FormEditorState.form.description,
                ),
                class_name="p-6 border-b border-gray-200 bg-white",
            ),
            rx.el.div(
                rx.cond(
                    FormEditorState.form.fields.length() > 0,
                    rx.el.div(
                        rx.foreach(FormEditorState.form.fields, canvas_field_wrapper),
                        class_name="space-y-4",
                    ),
                    rx.el.div(
                        rx.icon(
                            "square_dashed_mouse_pointer",
                            size=48,
                            class_name="text-gray-400",
                        ),
                        rx.el.p(
                            "Drag & Drop fields here", class_name="mt-4 text-gray-500"
                        ),
                        class_name="flex flex-col items-center justify-center h-64 border-2 border-dashed border-gray-300 rounded-xl",
                    ),
                ),
                class_name="p-8",
            ),
            class_name="max-w-4xl mx-auto w-full",
        ),
        class_name="flex-grow flex flex-col items-center bg-gray-100 overflow-y-auto",
    )


def property_input(label: str, prop_name: str, **kwargs) -> rx.Component:
    """A generic input for editing a field property."""
    return rx.el.div(
        rx.el.label(
            label, class_name="block text-xs font-medium text-gray-500 uppercase"
        ),
        rx.el.input(
            on_change=lambda val: FormEditorState.update_field_property(prop_name, val),
            class_name="mt-1 w-full p-2 border border-gray-300 rounded-md shadow-sm text-sm focus:ring-purple-500 focus:border-purple-500",
            **kwargs,
            default_value=getattr(FormEditorState.selected_field, prop_name),
        ),
        class_name="w-full",
    )


def property_toggle(label: str, prop_name: str) -> rx.Component:
    """A toggle switch for a boolean field property."""
    return rx.el.div(
        rx.el.label(
            rx.el.input(
                type="checkbox",
                checked=getattr(FormEditorState.selected_field, prop_name),
                on_change=lambda val: FormEditorState.update_field_property(
                    prop_name, val
                ),
                class_name="h-4 w-4 text-purple-600 border-gray-300 rounded focus:ring-purple-500",
            ),
            rx.el.span(label, class_name="ml-2 text-sm font-medium text-gray-700"),
            class_name="flex items-center",
        )
    )


def option_editor() -> rx.Component:
    """Editor for fields with options (select, radio)."""
    return rx.el.div(
        rx.el.label(
            "Options",
            class_name="block text-xs font-medium text-gray-500 uppercase mb-2",
        ),
        rx.foreach(
            FormEditorState.selected_field.options,
            lambda option, index: rx.el.div(
                rx.el.input(
                    on_change=lambda val: FormEditorState.update_option_property(
                        index, "label", val
                    ),
                    class_name="w-full p-1.5 border border-gray-300 rounded-md text-sm",
                    default_value=option.label,
                ),
                rx.el.button(
                    rx.icon("x", size=14),
                    on_click=lambda: FormEditorState.remove_option(index),
                    class_name="p-1 hover:bg-gray-200 rounded-md",
                ),
                class_name="flex items-center space-x-2",
            ),
        ),
        rx.el.button(
            rx.icon("plus", size=14, class_name="mr-2"),
            "Add Option",
            on_click=FormEditorState.add_option,
            class_name="mt-2 text-sm text-purple-600 font-semibold hover:text-purple-800 flex items-center",
        ),
    )


def selected_field_properties() -> rx.Component:
    """Displays the properties editor for the currently selected field."""
    field_type = FormEditorState.selected_field.type
    return rx.el.div(
        rx.el.h3(
            f"{FormEditorState.selected_field_display_name} Field",
            class_name="text-lg font-bold text-gray-800",
        ),
        rx.el.div(
            property_input("Label", "label"),
            rx.cond(
                (field_type == "text")
                | (field_type == "email")
                | (field_type == "tel")
                | (field_type == "textarea"),
                property_input("Placeholder", "placeholder"),
                rx.el.div(),
            ),
            rx.cond(
                (field_type == "select") | (field_type == "radio"),
                option_editor(),
                rx.el.div(),
            ),
            property_toggle("Required", "required"),
            rx.el.button(
                rx.icon("trash-2", size=16, class_name="mr-2"),
                "Delete Field",
                on_click=FormEditorState.delete_selected_field,
                class_name="w-full flex items-center justify-center mt-6 px-4 py-2 bg-red-50 text-red-600 font-semibold rounded-lg shadow-sm hover:bg-red-100 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-opacity-75",
            ),
            class_name="mt-6 space-y-4",
        ),
        class_name="p-6",
    )


def properties_editor() -> rx.Component:
    """The right sidebar for editing component properties."""
    return rx.el.aside(
        rx.el.div(
            rx.cond(
                FormEditorState.selected_field,
                selected_field_properties(),
                rx.el.div(
                    rx.icon("disc_3", size=32, class_name="text-gray-400"),
                    rx.el.p(
                        "Select a field to edit its properties.",
                        class_name="mt-4 text-sm text-gray-500 text-center",
                    ),
                    class_name="flex flex-col items-center justify-center h-full text-center p-4",
                ),
            ),
            class_name="flex-grow overflow-y-auto",
        ),
        class_name="w-80 bg-white border-l border-gray-200 hidden lg:flex flex-col flex-shrink-0",
    )