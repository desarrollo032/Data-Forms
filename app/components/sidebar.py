import reflex as rx
from app.states.state import FormEditorState


def field_palette_item(field: dict) -> rx.Component:
    """A component for an individual item in the field palette."""
    return rx.el.div(
        rx.el.button(
            rx.icon(field["icon"], size=20, class_name="mr-3"),
            rx.el.span(field["name"], class_name="font-medium"),
            on_click=lambda: FormEditorState.add_field(field["type"]),
            class_name="w-full flex items-center text-left px-4 py-2.5 rounded-lg text-sm text-gray-700 bg-white hover:bg-gray-100 transition-colors duration-150 ease-in-out border border-gray-200 shadow-sm hover:shadow-md hover:-translate-y-px",
        ),
        class_name="w-full",
    )


def editor_sidebar() -> rx.Component:
    """The left sidebar component for the form editor."""
    return rx.el.aside(
        rx.el.div(
            rx.el.a(
                rx.icon("arrow-left", size=16, class_name="mr-2"),
                "Back to Dashboard",
                href="/",
                class_name="flex items-center p-4 border-b border-gray-200 text-sm font-medium text-gray-600 hover:bg-gray-100",
            ),
            rx.el.div(
                rx.el.h2(
                    "Form Elements",
                    class_name="px-4 pt-4 pb-2 text-sm font-semibold text-gray-500 uppercase tracking-wider",
                ),
                rx.el.div(
                    rx.foreach(FormEditorState.available_fields, field_palette_item),
                    class_name="space-y-2 p-4",
                ),
                class_name="flex-grow overflow-y-auto",
            ),
            rx.el.div(
                rx.el.a(
                    rx.icon("github", size=18, class_name="mr-2"),
                    "Built with Reflex",
                    href="https://github.com/reflex-dev/reflex",
                    target="_blank",
                    class_name="flex items-center justify-center text-xs text-gray-500 hover:text-purple-600 transition-colors",
                ),
                class_name="p-4 border-t border-gray-200",
            ),
            class_name="flex flex-col h-full",
        ),
        class_name="w-64 bg-gray-50 border-r border-gray-200 flex-shrink-0 hidden md:flex flex-col",
    )