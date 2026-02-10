"""Rich console wrapper with app-specific styling."""

import sys
from io import StringIO

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
        self._last_panel_height = 0
        self._lines_since_instruction = 0  # Track all lines since last instruction

    def _measure_renderable(self, renderable) -> int:
        """Measure how many lines a renderable will take."""
        # Create a temporary console to measure output
        temp_console = Console(
            theme=GITGOOD_THEME,
            file=StringIO(),
            width=self.console.width,
            force_terminal=True,
        )
        temp_console.print(renderable)
        output = temp_console.file.getvalue()
        return output.count('\n')

    def _clear_lines(self, count: int) -> None:
        """Clear the last N lines from the terminal."""
        if count <= 0:
            return
        # Move cursor up and clear each line
        for _ in range(count):
            sys.stdout.write('\033[A')  # Move up
            sys.stdout.write('\033[2K')  # Clear line
        sys.stdout.flush()

    def clear_last_panel(self) -> None:
        """Clear the last panel that was printed."""
        self._clear_lines(self._last_panel_height)
        self._last_panel_height = 0

    def print_panel(self, panel, replace_previous: bool = True) -> None:
        """Print a panel, optionally replacing the previous one."""
        if replace_previous and self._last_panel_height > 0:
            self.clear_last_panel()
        self._last_panel_height = self._measure_renderable(panel)
        self.console.print(panel)

    def reset_panel_tracking(self) -> None:
        """Reset panel tracking (call after non-panel output)."""
        self._last_panel_height = 0

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

    def note_input_line(self) -> None:
        """Track that a user input line was displayed (call after prompt)."""
        self._lines_since_instruction += 1

    def print_instruction(self, text: str, replace_previous: bool = True) -> None:
        """Print a lesson instruction, replacing the previous one."""
        panel = Panel(
            Markdown(text),
            title="[bold #c15f3c]Instruction[/bold #c15f3c]",
            border_style="#c15f3c",
            padding=(1, 2),
        )

        # Clear everything since last instruction (old instruction + user input + outputs)
        if replace_previous and self._lines_since_instruction > 0:
            self._clear_lines(self._lines_since_instruction)

        # Print new instruction with blank line before
        self.console.print()
        self.console.print(panel)

        # Track this instruction's height for next replacement
        self._lines_since_instruction = self._measure_renderable(panel) + 1  # +1 for blank line

    def print_success(self, text: str) -> None:
        """Print a success message."""
        self.console.print()
        self.console.print(f"[success]✓ {text}[/success]")
        # Count lines: blank line + text (which may wrap)
        self._lines_since_instruction += text.count('\n') + 2

    def print_error(self, text: str) -> None:
        """Print an error message."""
        self.console.print(f"[error]✗ {text}[/error]")
        self._lines_since_instruction += text.count('\n') + 1

    def print_warning(self, text: str) -> None:
        """Print a warning message."""
        self.console.print(f"[warning]⚠ {text}[/warning]")
        self._lines_since_instruction += text.count('\n') + 1

    def print_hint(self, hints: list[str]) -> None:
        """Print helpful hints."""
        if not hints:
            return
        self.console.print()
        for hint in hints:
            self.console.print(f"[hint]  → {hint}[/hint]")
        self._lines_since_instruction += len(hints) + 1  # +1 for blank line

    def print_command_output(self, output: str) -> None:
        """Print simulated git command output."""
        if output:
            self.console.print()
            self.console.print(output)
            self._lines_since_instruction += output.count('\n') + 2  # +2 for blank line + final line

    def print_info(self, text: str) -> None:
        """Print informational text."""
        self.console.print(f"[white]⏺ {text}[/white]")
        self._lines_since_instruction += text.count('\n') + 1

    def print_divider(self) -> None:
        """Print a visual divider. Resets instruction tracking (signals new section)."""
        self._lines_since_instruction = 0
        self._last_panel_height = 0
        self.console.print()
        self.console.rule(style="dim")
        self.console.print()

    def print_lesson_complete(self, title: str) -> None:
        """Print lesson completion message."""
        panel = Panel(
            f"[success]🎉 Congratulations![/success]\n\n"
            f"You've completed: [bold]{title}[/bold]\n\n"
            f"Type [command]lessons[/command] to continue to the next lesson.",
            border_style="green",
            padding=(1, 2),
        )
        self.console.print()
        self.print_panel(panel, replace_previous=True)

    def print_all_complete(self) -> None:
        """Print message when all lessons are complete."""
        panel = Panel(
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
        )
        self.console.print()
        self.print_panel(panel, replace_previous=True)
