"""Rich console wrapper with app-specific styling."""

from rich.console import Console
from rich.theme import Theme
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown


# Custom theme for the application
GHFLOW_THEME = Theme({
    "info": "cyan",
    "success": "green bold",
    "warning": "yellow",
    "error": "red bold",
    "command": "bright_white on grey23",
    "branch": "magenta bold",
    "commit": "yellow",
    "instruction": "cyan",
    "hint": "dim cyan italic",
    "prompt": "green bold",
    "header": "bold blue",
})


WELCOME_ART = """
   _____ _ _   _    _       _       ______ _
  / ____(_) | | |  | |     | |     |  ____| |
 | |  __ _| |_| |__| |_   _| |__   | |__  | | _____      __
 | | |_ | | __|  __  | | | | '_ \\  |  __| | |/ _ \\ \\ /\\ / /
 | |__| | | |_| |  | | |_| | |_) | | |    | | (_) \\ V  V /
  \\_____|_|\\__|_|  |_|\\__,_|_.__/  |_|    |_|\\___/ \\_/\\_/
"""


class GHFlowConsole:
    """Wrapper around Rich console with app-specific methods."""

    def __init__(self):
        self.console = Console(theme=GHFLOW_THEME)

    def print_welcome(self) -> None:
        """Display welcome message and ASCII art."""
        self.console.print()
        self.console.print(WELCOME_ART, style="bold blue")
        self.console.print()
        self.console.print(
            "Learn GitHub Flow interactively by typing real git commands!",
            style="info",
        )
        self.console.print()
        self.console.print(
            "Type [command]help[/command] to see available commands, "
            "or [command]lessons[/command] to start learning.",
            style="dim",
        )
        self.console.print()

    def print_instruction(self, text: str) -> None:
        """Print a lesson instruction."""
        # Parse as markdown for rich formatting
        self.console.print()
        self.console.print(Panel(
            Markdown(text),
            title="[header]Instruction[/header]",
            border_style="cyan",
            padding=(1, 2),
        ))

    def print_success(self, text: str) -> None:
        """Print a success message."""
        self.console.print()
        self.console.print(f"[success]✓ {text}[/success]")

    def print_error(self, text: str) -> None:
        """Print an error message."""
        self.console.print(f"[error]✗ {text}[/error]")

    def print_warning(self, text: str) -> None:
        """Print a warning message."""
        self.console.print(f"[warning]⚠ {text}[/warning]")

    def print_hint(self, hints: list[str]) -> None:
        """Print helpful hints."""
        if not hints:
            return
        self.console.print()
        for hint in hints:
            self.console.print(f"[hint]  → {hint}[/hint]")

    def print_command_output(self, output: str) -> None:
        """Print simulated git command output."""
        if output:
            self.console.print()
            self.console.print(output)

    def print_info(self, text: str) -> None:
        """Print informational text."""
        self.console.print(f"[info]{text}[/info]")

    def print_divider(self) -> None:
        """Print a visual divider."""
        self.console.print()
        self.console.rule(style="dim")
        self.console.print()

    def print_lesson_complete(self, title: str) -> None:
        """Print lesson completion message."""
        self.console.print()
        self.console.print(Panel(
            f"[success]🎉 Congratulations![/success]\n\n"
            f"You've completed: [bold]{title}[/bold]\n\n"
            f"Type [command]lessons[/command] to continue to the next lesson.",
            border_style="green",
            padding=(1, 2),
        ))

    def print_all_complete(self) -> None:
        """Print message when all lessons are complete."""
        self.console.print()
        self.console.print(Panel(
            "[success]🎉 Amazing work![/success]\n\n"
            "You've completed all GitHub Flow lessons!\n\n"
            "You now know how to:\n"
            "• Create feature branches\n"
            "• Make commits with good messages\n"
            "• Push branches to remote\n"
            "• Create and manage pull requests\n"
            "• Handle code reviews\n"
            "• Merge and clean up branches\n\n"
            "Go forth and collaborate!",
            title="[bold]Course Complete[/bold]",
            border_style="green",
            padding=(1, 2),
        ))
