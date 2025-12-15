#!/usr/bin/env python3
"""
build.py - Deterministic slide builder
Converts Markdown to reveal.js HTML using Pandoc.
Governed by Python for reproducibility and diagnostics.
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from typing import Optional

# --- Configuration ---
CONSOLE = Console()

# Define the paths for the source, vendor, and output directories
SOURCE_MD = Path("slides") / "deck.md"
OUTPUT_HTML = Path("dist") / "index.html"
REVEAL_VENDOR = Path("revealjs")

# Build metadata
BUILD_TIME = datetime.now().isoformat(timespec='seconds')

# --- Helper Functions ---
def get_git_hash() -> str:
    """Get current commit hash if in git repo."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            cwd=Path.cwd()
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.SubprocessError, FileNotFoundError):
        pass
    return "unknown"

def print_build_summary(source_size: int, output_size: int):
    """Display a nice summary table of the build."""
    table = Table(title="Build Summary", show_header=False, box=None)
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="white")
    
    table.add_row("Source", f"{SOURCE_MD} ({source_size:,} bytes)")
    table.add_row("Output", f"{OUTPUT_HTML} ({output_size:,} bytes)")
    table.add_row("Build Time", BUILD_TIME)
    table.add_row("Commit", get_git_hash())
    table.add_row("reveal.js", str(REVEAL_VENDOR.resolve()))
    
    CONSOLE.print()
    CONSOLE.print(table)
    CONSOLE.print()

# --- Checks ---
def check_paths():
    """Ensure all required files and directories exist before running Pandoc."""
    CONSOLE.print("[bold blue]🔍 Validating environment...[/bold blue]")
    
    checks_passed = True
    
    # Check source file
    if not SOURCE_MD.exists():
        CONSOLE.print(f"  [red]❌[/red] Source file not found: {SOURCE_MD}")
        CONSOLE.print("  Please create the file and add the slide content.")
        checks_passed = False
    else:
        CONSOLE.print(f"  [green]✓[/green] Source file: {SOURCE_MD}")
        # Show source file size
        source_size = SOURCE_MD.stat().st_size
        CONSOLE.print(f"       Size: {source_size:,} bytes")
        
        # Count slides (approximate by counting '---' separators)
        try:
            content = SOURCE_MD.read_text(encoding='utf-8')
            slide_count = content.count('\n---\n') + 1
            CONSOLE.print(f"       Slides: ~{slide_count}")
        except:
            pass

    # Check reveal.js
    reveal_index = REVEAL_VENDOR / "dist" / "reveal.js"
    if not reveal_index.exists():
        CONSOLE.print(f"  [red]❌[/red] reveal.js not found at {REVEAL_VENDOR}")
        CONSOLE.print("  Run: [yellow]git clone https://github.com/hakimel/reveal.js revealjs[/yellow]")
        CONSOLE.print("  Or as submodule: [yellow]git submodule add https://github.com/hakimel/reveal.js[/yellow]")
        checks_passed = False
    else:
        CONSOLE.print(f"  [green]✓[/green] reveal.js: {REVEAL_VENDOR}")
        
    # Check pandoc
    try:
        result = subprocess.run(["pandoc", "--version"], 
                              capture_output=True, text=True)
        version_line = result.stdout.split('\n')[0]
        CONSOLE.print(f"  [green]✓[/green] Pandoc: {version_line}")
    except (subprocess.SubprocessError, FileNotFoundError):
        CONSOLE.print(f"  [red]❌[/red] Pandoc not found in PATH")
        CONSOLE.print("  Install from: [yellow]https://pandoc.org/installing.html[/yellow]")
        checks_passed = False
    
    # Ensure output directory exists
    OUTPUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    CONSOLE.print(f"  [green]✓[/green] Output directory: {OUTPUT_HTML.parent}")
    
    if not checks_passed:
        CONSOLE.print("\n[bold red]Validation failed. Please fix the issues above.[/bold red]")
        exit(1)
    
    CONSOLE.print("\n[green]✅ All checks passed![/green]\n")
    return True

# --- Build Execution ---
def run_pandoc():
    """Constructs and executes the Pandoc command with reproducibility."""
    CONSOLE.print(f"[bold cyan]⚙️  Building slides...[/bold cyan]")
    CONSOLE.print(f"  Source: [yellow]{SOURCE_MD}[/yellow]")
    CONSOLE.print(f"  Target: [yellow]{OUTPUT_HTML}[/yellow]")
    
    # Get commit hash for metadata
    commit_hash = get_git_hash()
    
    # 1. Define the core Pandoc arguments
    pandoc_args = [
        # Call Pandoc
        "pandoc",
        
        # Input file
        str(SOURCE_MD),
        
        # Output format
        "-t", "revealjs",
        
        # Output file path
        "-o", str(OUTPUT_HTML),

        # Standalone HTML with embedded resources
        "--standalone", 
        "--embed-resources",
        
        # Slide configuration
        "--slide-level=1",  # Only H1 starts new slides
        
        # reveal.js configuration
        "-V", f"revealjs-url={REVEAL_VENDOR}",
        "-V", "theme=black",  # black, white, league, beige, sky, night, serif, simple, solarized
        
        # Presentation controls
        "-V", "slide-number=true",
        "-V", "transition=slide",  # none, fade, slide, convex, concave, zoom
        "-V", "controls=true",
        "-V", "progress=true",
        "-V", "center=true",
        "-V", "mouseWheel=true",
        "-V", "showSlideProgress=true",
        
        # Build metadata
        "-V", f"build-time={BUILD_TIME}",
        "-V", f"commit-hash={commit_hash}",
        
        # Clean output
        "--strip-comments",
        
        # Resource path for images
        "--resource-path=.:slides:.",
    ]
    
    # Show the exact command for reproducibility
    cmd_text = " ".join(pandoc_args)
    if len(cmd_text) > 100:
        cmd_display = cmd_text[:100] + "..."
    else:
        cmd_display = cmd_text
    
    CONSOLE.print(f"  [dim]Command: {cmd_display}[/dim]")
    
    # Show full command in a panel if requested or in verbose mode
    if "--verbose" in sys.argv or "-v" in sys.argv:
        syntax = Syntax(cmd_text, "bash", theme="monokai", line_numbers=False)
        CONSOLE.print(Panel(syntax, title="Full Pandoc Command", border_style="blue"))
    
    try:
        # Show progress indicator
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            task = progress.add_task("Running Pandoc...", total=None)
            
            # Execute the command
            result = subprocess.run(
                pandoc_args, 
                check=True, 
                capture_output=True, 
                text=True,
                encoding='utf-8'
            )
            
            progress.update(task, completed=100)
        
        # Success message
        CONSOLE.print("[bold green]✅ Build complete![/bold green]")
        
        # Display file sizes
        if OUTPUT_HTML.exists():
            output_size = OUTPUT_HTML.stat().st_size
            source_size = SOURCE_MD.stat().st_size if SOURCE_MD.exists() else 0
            CONSOLE.print(f"  Output size: [yellow]{output_size:,}[/yellow] bytes")
            CONSOLE.print(f"  Compression: [yellow]{output_size/source_size:.1%}[/yellow]" if source_size > 0 else "")
        
        # Show any warnings from Pandoc
        if result.stderr:
            CONSOLE.print(f"[yellow]📝 Pandoc Messages:[/yellow]")
            for line in result.stderr.strip().split('\n'):
                if line.strip():
                    CONSOLE.print(f"  [dim]{line}[/dim]")
        
        # Show summary table
        if OUTPUT_HTML.exists() and SOURCE_MD.exists():
            print_build_summary(
                source_size=SOURCE_MD.stat().st_size,
                output_size=OUTPUT_HTML.stat().st_size
            )
            
        # Next steps
        CONSOLE.print("[bold]Next steps:[/bold]")
        CONSOLE.print(f"  1. Open in browser: [yellow]open {OUTPUT_HTML}[/yellow]")
        CONSOLE.print(f"  2. Start local server: [yellow]python -m http.server --directory dist/[/yellow]")
        CONSOLE.print(f"  3. View at: [yellow]http://localhost:8000[/yellow]")
            
    except subprocess.CalledProcessError as e:
        CONSOLE.print(f"[bold red]❌ Build Failed! (exit code: {e.returncode})[/bold red]")
        
        if e.stdout:
            CONSOLE.print("[yellow]Standard Output:[/yellow]")
            CONSOLE.print(f"[dim]{e.stdout}[/dim]")
        
        if e.stderr:
            CONSOLE.print("[red]Error Output:[/red]")
            # Try to extract meaningful error
            error_lines = e.stderr.strip().split('\n')
            for line in error_lines[-5:]:  # Show last 5 lines of error
                if line.strip():
                    CONSOLE.print(f"  [red]{line}[/red]")
        
        exit(1)
        
    except FileNotFoundError:
        CONSOLE.print("[bold red]❌ Error: Pandoc not found.[/bold red]")
        CONSOLE.print("  Please install Pandoc from: [yellow]https://pandoc.org/installing.html[/yellow]")
        CONSOLE.print("  Or check it's in your PATH.")
        exit(1)
        
    except KeyboardInterrupt:
        CONSOLE.print("\n[yellow]⚠️  Build interrupted by user[/yellow]")
        exit(130)

def show_help():
    """Display help information."""
    CONSOLE.print(Panel(
        "[bold]Slides Builder[/bold]\n\n"
        "Builds reveal.js slides from Markdown using Pandoc.\n\n"
        "[bold]Usage:[/bold]\n"
        "  [cyan]python build.py[/cyan]          # Build slides\n"
        "  [cyan]python build.py --verbose[/cyan] # Show full Pandoc command\n"
        "  [cyan]python build.py --help[/cyan]    # Show this help\n\n"
        "[bold]Requirements:[/bold]\n"
        "  • Python 3.12+ with rich package\n"
        "  • Pandoc 2.14+ installed and in PATH\n"
        "  • reveal.js vendored in 'revealjs/' directory\n\n"
        "[bold]Project Layout:[/bold]\n"
        "  slides/deck.md    → Source Markdown\n"
        "  dist/index.html   → Output HTML\n"
        "  revealjs/         → reveal.js library",
        title="Help",
        border_style="green"
    ))

def main():
    """Main entry point."""
    # Parse command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] in ["--help", "-h", "help"]:
            show_help()
            return
        elif sys.argv[1] in ["--version", "-V"]:
            CONSOLE.print("[bold]Slides Builder[/bold] v0.1.0")
            return
    
    # Show header
    CONSOLE.print("[bold blue]" + "=" * 60 + "[/bold blue]")
    CONSOLE.print("[bold blue]🎯 Slides Builder[/bold blue]")
    CONSOLE.print("[bold blue]" + "=" * 60 + "[/bold blue]\n")
    
    # Run build pipeline
    try:
        check_paths()
        run_pandoc()
        
        # Final success message
        CONSOLE.print("[bold green]" + "=" * 60 + "[/bold green]")
        CONSOLE.print("[bold green]✨ Build successful! Open dist/index.html to view. ✨[/bold green]")
        CONSOLE.print("[bold green]" + "=" * 60 + "[/bold green]")
        
    except Exception as e:
        CONSOLE.print(f"\n[bold red]💥 Unexpected error:[/bold red] {e}")
        CONSOLE.print_exception()
        exit(1)

if __name__ == "__main__":
    main()