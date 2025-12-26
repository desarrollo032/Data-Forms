import reflex as rx


class AuthState(rx.State):
    """Manages user authentication and session."""

    is_authenticated: bool = False

    @rx.event
    def register(self, form_data: dict):
        """Register a new user (dummy implementation)."""
        email = form_data.get("email")
        password = form_data.get("password")
        if not email or not password:
            return rx.toast.error("Email and password are required.")
        self.is_authenticated = True
        return rx.redirect("/dashboard")

    @rx.event
    def login(self, form_data: dict):
        """Log in a user (dummy implementation)."""
        email = form_data.get("email")
        password = form_data.get("password")
        if not email or not password:
            return rx.toast.error("Email and password are required.")
        self.is_authenticated = True
        return rx.redirect("/dashboard")

    @rx.event
    def logout(self):
        """Log out the user."""
        self.is_authenticated = False
        return rx.redirect("/")

    @rx.event
    def check_auth(self):
        """Check if the user is authenticated, redirect to login if not."""
        if not self.is_authenticated:
            return rx.redirect("/login")