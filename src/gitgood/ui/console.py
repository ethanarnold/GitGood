"""Rich console wrapper with app-specific styling."""

from rich.console import Console
from rich.theme import Theme
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown

from .regions import RegionManager, LayoutConfig


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

# Fixed height for instruction panel (ensures output area never shifts)
INSTRUCTION_PANEL_HEIGHT = 10


class GitGoodConsole:
    """Wrapper around Rich console with app-specific methods."""

    def __init__(self):
        self.console = Console(theme=GITGOOD_THEME)
        self._output_buffer: list = []  # Accumulated output history
        self._current_instruction: str | None = None  # Current instruction text
        self._region_manager = RegionManager(self.console)

    def _is_buffered_mode(self) -> bool:
        """Check if we're in buffered mode (instruction is active)."""
        return self._current_instruction is not None

    def _render_title(self) -> None:
        """Render title region at top of screen."""
        self._region_manager.move_home()
        art = Text(WELCOME_ART)
        art.stylize("#c15f3c")
        self.console.print(art)
        self.console.print("[white]Learn GitHub Flow interactively![/white]")
        self.console.rule(style="grey50")
        self._region_manager._title_rendered = True

    def _redraw(self) -> None:
        """Clear content area and redraw: instruction + output history + bottom separator."""
        # Ensure title is rendered first
        if not self._region_manager._title_rendered:
            self.console.clear()
            self._render_title()

        # Clear only below title (preserves title region)
        self._region_manager.clear_from_row(self._region_manager.config.title_height)
        self._region_manager.move_to_row(self._region_manager.config.title_height)

        # 1. Print instruction panel with FIXED HEIGHT (if any)
        if self._current_instruction:
            panel = Panel(
                Markdown(self._current_instruction),
                title="[bold #c15f3c]Instruction[/bold #c15f3c]",
                border_style="#c15f3c",
                padding=(1, 2),
                height=INSTRUCTION_PANEL_HEIGHT,
            )
            self.console.print(panel)
            self.console.rule(style="grey50")

        # 2. Print accumulated output (always starts at same row due to fixed panel height)
        for line in self._output_buffer:
            self.console.print(line)

    def redraw(self) -> None:
        """Public method to trigger a redraw (e.g., on terminal resize)."""
        # On resize, re-render everything with new terminal dimensions
        self.console.clear()
        self._region_manager._title_rendered = False
        self._render_title()
        if self._is_buffered_mode():
            self._redraw()

    def print_welcome(self) -> None:
        """Display welcome message and ASCII art."""
        self.console.clear()
        self._render_title()
        self.console.print(
            "Type [command]help[/command] to see available commands, "
            "or [command]lessons[/command] to start learning.",
            style="dim",
        )
        self.console.print()

    def print_instruction(self, text: str) -> None:
        """Set current instruction and redraw."""
        self._current_instruction = text
        self._redraw()

    def clear_instruction(self) -> None:
        """Clear the current instruction."""
        self._current_instruction = None

    def add_input_line(self, line: str) -> None:
        """Add a user input line to the output buffer."""
        if self._is_buffered_mode():
            self._output_buffer.append(f"[bright_white]{line}[/bright_white]")
            # Don't redraw here - will redraw after command output

    def print_success(self, text: str) -> None:
        """Print a success message."""
        if self._is_buffered_mode():
            self._output_buffer.append("")  # Blank line
            self._output_buffer.append(f"[success]✓ {text}[/success]")
            self._redraw()
        else:
            self.console.print()
            self.console.print(f"[success]✓ {text}[/success]")

    def print_error(self, text: str) -> None:
        """Print an error message."""
        if self._is_buffered_mode():
            self._output_buffer.append(f"[error]✗ {text}[/error]")
            self._redraw()
        else:
            self.console.print(f"[error]✗ {text}[/error]")

    def print_warning(self, text: str) -> None:
        """Print a warning message."""
        if self._is_buffered_mode():
            self._output_buffer.append(f"[warning]⚠ {text}[/warning]")
            self._redraw()
        else:
            self.console.print(f"[warning]⚠ {text}[/warning]")

    def print_hint(self, hints: list[str]) -> None:
        """Print helpful hints."""
        if not hints:
            return
        if self._is_buffered_mode():
            self._output_buffer.append("")  # Blank line
            for hint in hints:
                self._output_buffer.append(f"[hint]  → {hint}[/hint]")
            self._redraw()
        else:
            self.console.print()
            for hint in hints:
                self.console.print(f"[hint]  → {hint}[/hint]")

    def print_command_output(self, output: str) -> None:
        """Print simulated git command output."""
        if not output:
            return
        if self._is_buffered_mode():
            self._output_buffer.append("")  # Blank line
            self._output_buffer.append(output)
            self._redraw()
        else:
            self.console.print()
            self.console.print(output)

    def print_info(self, text: str) -> None:
        """Print informational text."""
        if self._is_buffered_mode():
            self._output_buffer.append(f"[white]⏺ {text}[/white]")
            self._redraw()
        else:
            self.console.print(f"[white]⏺ {text}[/white]")

    def print_divider(self) -> None:
        """Print a visual divider in the output."""
        if self._is_buffered_mode():
            self._output_buffer.append("")
            self._output_buffer.append("[dim]" + "─" * 40 + "[/dim]")
            self._output_buffer.append("")
            self._redraw()
        else:
            self.console.print()
            self.console.rule(style="dim")
            self.console.print()

    def print_panel(self, panel) -> None:
        """Print a panel to output buffer."""
        if self._is_buffered_mode():
            self._output_buffer.append(panel)
            self._redraw()
        else:
            self.console.print(panel)

    def print_lesson_complete(self, title: str) -> None:
        """Print lesson completion message."""
        panel = Panel(
            f"[success]🎉 Congratulations![/success]\n\n"
            f"You've completed: [bold]{title}[/bold]\n\n"
            f"Type [command]lessons[/command] to continue to the next lesson.",
            border_style="green",
            padding=(1, 2),
        )
        if self._is_buffered_mode():
            self._output_buffer.append("")
            self._output_buffer.append(panel)
            self._redraw()
        else:
            self.console.print()
            self.console.print(panel)

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
        if self._is_buffered_mode():
            self._output_buffer.append("")
            self._output_buffer.append(panel)
            self._redraw()
        else:
            self.console.print()
            self.console.print(panel)

    def clear_output_buffer(self) -> None:
        """Clear the output buffer (e.g., when starting a new lesson)."""
        self._output_buffer.clear()
