import reflex as rx
from app.states.auth_state import AuthState


def auth_form_field(
    label: str, placeholder: str, field_id: str, field_type: str = "text"
) -> rx.Component:
    """A reusable form field component for authentication forms."""
    return rx.el.div(
        rx.el.label(label, class_name="text-sm font-medium text-gray-700"),
        rx.el.input(
            id=field_id,
            type=field_type,
            placeholder=placeholder,
            required=True,
            class_name="mt-1 w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-purple-500 focus:border-purple-500",
        ),
        class_name="w-full",
    )


def login_form() -> rx.Component:
    """The login form component."""
    return rx.el.div(
        rx.el.h2("Log In", class_name="text-2xl font-bold text-center text-gray-800"),
        rx.el.form(
            rx.el.div(
                auth_form_field("Email", "your@email.com", "email", "email"),
                auth_form_field("Password", "********", "password", "password"),
                class_name="space-y-4",
            ),
            rx.el.button(
                "Log In",
                type="submit",
                class_name="mt-6 w-full bg-purple-600 text-white py-2 rounded-lg font-semibold hover:bg-purple-700",
            ),
            on_submit=AuthState.login,
            reset_on_submit=True,
            class_name="w-full mt-6",
        ),
        rx.el.p(
            "Don't have an account? ",
            rx.el.a(
                "Sign Up",
                href="/register",
                class_name="text-purple-600 hover:underline",
            ),
            class_name="mt-4 text-center text-sm text-gray-600",
        ),
        class_name="max-w-md w-full bg-white p-8 rounded-xl shadow-lg",
    )


def registration_form() -> rx.Component:
    """The registration form component."""
    return rx.el.div(
        rx.el.h2(
            "Create Account", class_name="text-2xl font-bold text-center text-gray-800"
        ),
        rx.el.form(
            rx.el.div(
                auth_form_field("Email", "your@email.com", "email", "email"),
                auth_form_field("Password", "********", "password", "password"),
                class_name="space-y-4",
            ),
            rx.el.button(
                "Sign Up",
                type="submit",
                class_name="mt-6 w-full bg-purple-600 text-white py-2 rounded-lg font-semibold hover:bg-purple-700",
            ),
            on_submit=AuthState.register,
            reset_on_submit=True,
            class_name="w-full mt-6",
        ),
        rx.el.p(
            "Already have an account? ",
            rx.el.a(
                "Log In", href="/login", class_name="text-purple-600 hover:underline"
            ),
            class_name="mt-4 text-center text-sm text-gray-600",
        ),
        class_name="max-w-md w-full bg-white p-8 rounded-xl shadow-lg",
    )