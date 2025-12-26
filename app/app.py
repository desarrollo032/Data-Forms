import reflex as rx
from app.states.state import AppState, FormEditorState, FormViewState
from app.states.auth_state import AuthState
from app.components.sidebar import editor_sidebar
from app.models import Form as FormModel
from app.components.auth import login_form, registration_form


def landing_page() -> rx.Component:
    """The landing page of the app."""
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Custom Form Builder",
                class_name="text-5xl font-extrabold text-gray-900",
            ),
            rx.el.p(
                "Create, manage, and share powerful forms with ease.",
                class_name="mt-4 text-xl text-gray-600",
            ),
            rx.el.div(
                rx.el.a(
                    "Log In",
                    href="/login",
                    class_name="px-8 py-3 bg-purple-600 text-white font-semibold rounded-lg shadow-md hover:bg-purple-700",
                ),
                rx.el.a(
                    "Sign Up",
                    href="/register",
                    class_name="px-8 py-3 bg-gray-200 text-gray-800 font-semibold rounded-lg shadow-md hover:bg-gray-300",
                ),
                class_name="mt-8 flex gap-4",
            ),
            class_name="text-center",
        ),
        class_name="flex items-center justify-center h-screen bg-gray-50 font-['Inter']",
    )


def login_page() -> rx.Component:
    """The login page."""
    return rx.el.div(
        login_form(),
        class_name="flex items-center justify-center h-screen bg-gray-100 font-['Inter']",
    )


def registration_page() -> rx.Component:
    """The registration page."""
    return rx.el.div(
        registration_form(),
        class_name="flex items-center justify-center h-screen bg-gray-100 font-['Inter']",
    )


def form_card(form: FormModel) -> rx.Component:
    """A card to display a summary of a form on the dashboard."""
    return rx.el.div(
        rx.el.div(
            rx.el.h3(form.title, class_name="font-bold text-lg text-gray-800"),
            rx.el.p(
                f"{form.fields.length()} fields",
                class_name="text-sm text-gray-500 mt-1",
            ),
            class_name="flex-grow",
        ),
        rx.el.div(
            rx.el.a(
                rx.icon("copy", size=18, class_name="text-gray-500"),
                href=f"/editor/{form.id}",
                class_name="p-2 rounded-md hover:bg-gray-200",
            ),
            rx.el.a(
                rx.icon("eye", size=18, class_name="text-gray-500"),
                href=f"/view/{form.id}",
                target="_blank",
                class_name="p-2 rounded-md hover:bg-gray-200",
            ),
            rx.el.button(
                rx.icon("trash-2", size=18, class_name="text-red-500"),
                on_click=lambda: AppState.delete_form(form.id),
                class_name="p-2 rounded-md hover:bg-red-100",
            ),
            class_name="flex items-center space-x-2",
        ),
        class_name="flex items-center p-4 bg-white border border-gray-200 rounded-xl shadow-sm hover:shadow-lg transition-shadow",
    )


def dashboard_page() -> rx.Component:
    """The main dashboard page listing all created forms."""
    return rx.el.div(
        rx.el.header(
            rx.el.div(
                rx.el.h1("My Forms", class_name="text-3xl font-bold text-gray-900"),
                rx.el.div(
                    rx.el.button(
                        "Create New Form",
                        on_click=AppState.create_new_form,
                        class_name="px-4 py-2 bg-purple-600 text-white font-semibold rounded-lg shadow-md hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-opacity-75",
                    ),
                    rx.el.button(
                        "Sign Out",
                        on_click=AuthState.logout,
                        class_name="px-4 py-2 bg-red-500 text-white font-semibold rounded-lg shadow-md hover:bg-red-600",
                    ),
                    class_name="flex items-center gap-4",
                ),
                class_name="container mx-auto flex justify-between items-center",
            ),
            class_name="bg-white border-b border-gray-200 p-4",
        ),
        rx.el.main(
            rx.el.div(
                rx.cond(
                    AppState.forms.length() > 0,
                    rx.el.div(
                        rx.foreach(AppState.forms, form_card),
                        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
                    ),
                    rx.el.div(
                        rx.el.h2(
                            "No forms yet!",
                            class_name="text-xl font-semibold text-gray-700",
                        ),
                        rx.el.p(
                            "Click 'Create New Form' to get started.",
                            class_name="text-gray-500 mt-2",
                        ),
                        class_name="text-center p-16 bg-gray-50 rounded-xl border-2 border-dashed border-gray-300",
                    ),
                ),
                class_name="container mx-auto py-8 px-4",
            ),
            class_name="flex-grow bg-gray-50",
        ),
        class_name="flex flex-col h-screen w-screen bg-gray-50 font-['Inter']",
    )


from app.components.editor import form_canvas, properties_editor


def editor_page() -> rx.Component:
    """The page for editing a specific form."""
    return rx.el.div(
        rx.cond(
            FormEditorState.form,
            rx.el.div(
                editor_sidebar(),
                form_canvas(),
                properties_editor(),
                class_name="flex flex-1",
            ),
            rx.el.div(
                rx.spinner(class_name="text-purple-500"),
                class_name="flex items-center justify-center flex-1",
            ),
        ),
        class_name="flex h-screen w-screen bg-gray-50 font-['Inter']",
    )


def view_form_page() -> rx.Component:
    """The public page for filling out a form."""
    return rx.el.div(
        rx.cond(
            FormViewState.form,
            rx.el.div(
                rx.el.h1(
                    FormViewState.form.title, class_name="text-3xl font-bold mb-2"
                ),
                rx.el.p(
                    FormViewState.form.description, class_name="text-gray-600 mb-8"
                ),
                rx.el.form(
                    rx.el.div("Form fields here", class_name="space-y-4"),
                    rx.el.button(
                        "Submit",
                        type="submit",
                        class_name="mt-6 w-full bg-purple-600 text-white py-3 rounded-lg font-semibold hover:bg-purple-700",
                    ),
                    on_submit=FormViewState.handle_submit,
                    reset_on_submit=True,
                    class_name="w-full",
                ),
                class_name="max-w-2xl w-full bg-white p-8 rounded-xl shadow-lg",
            ),
            rx.el.div(rx.spinner(class_name="text-purple-500")),
        ),
        class_name="min-h-screen w-screen bg-gray-100 flex items-center justify-center p-4 font-['Inter']",
    )


app = rx.App(
    theme=rx.theme(appearance="light", accent_color="purple", radius="medium"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(landing_page, route="/")
app.add_page(login_page, route="/login")
app.add_page(registration_page, route="/register")
app.add_page(dashboard_page, route="/dashboard", on_load=AuthState.check_auth)
app.add_page(
    editor_page,
    route="/editor/[form_id]",
    on_load=[FormEditorState.on_load, AuthState.check_auth],
)
app.add_page(view_form_page, route="/view/[form_id]", on_load=FormViewState.on_load)