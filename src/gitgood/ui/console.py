"""Rich console wrapper with app-specific styling."""

from rich.console import Console
from rich.theme import Theme
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown


# Custom theme for the application (Claude Code inspired: orange/terracotta)
GITGOOD_THEME = Theme({
    "info": "orange1",
    "success": "green bold",
    "warning": "yellow",
    "error": "red bold",
    "command": "bright_white on grey23",
    "branch": "orange1 bold",
    "commit": "yellow",
    "instruction": "orange1",
    "hint": "dim orange1 italic",
    "prompt": "green bold",
    "header": "bold orange1",
})


WELCOME_ART = """
   _____ _ _    _____                 _
  / ____(_) |  / ____|               | |
 | |  __ _| |_| |  __  ___   ___   __| |
 | | |_ | | __| | |_ |/ _ \\ / _ \\ / _` |
 | |__| | | |_| |__| | (_) | (_) | (_| |
  \\_____|_|\\__|\\_____|\\___/ \\___/ \\__,_|
"""


class GitGoodConsole:
    """Wrapper around Rich console with app-specific methods."""

    def __init__(self):
        self.console = Console(theme=GITGOOD_THEME)

    def print_welcome(self) -> None:
        """Display welcome message and ASCII art."""
        self.console.print()
        art = Text(WELCOME_ART)
        art.stylize("#c15f3c")
        self.console.print(art)
        self.console.print()
        self.console.print(
            "[white]⏺ Learn GitHub Flow interactively by typing real git commands![/white]",
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
            title="[bold #c15f3c]Instruction[/bold #c15f3c]",
            border_style="#c15f3c",
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
        self.console.print(f"[white]⏺ {text}[/white]")

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
