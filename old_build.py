# build.py

import subprocess
from pathlib import Path
from rich.console import Console

# --- Configuration ---
CONSOLE = Console()

# Define the paths for the source, vendor, and output directories
SOURCE_MD = Path("slides") / "deck.md"
OUTPUT_HTML = Path("dist") / "index.html"
REVEAL_VENDOR = Path("revealjs")

# --- Checks ---
def check_paths():
    """Ensure all required files and directories exist before running Pandoc."""
    if not SOURCE_MD.exists():
        CONSOLE.print(f"[bold red]Error:[/bold red] Source file not found: {SOURCE_MD}")
        CONSOLE.print("Please create the file and add the slide content.")
        exit(1)

    if not REVEAL_VENDOR.is_dir():
        CONSOLE.print(f"[bold red]Error:[/bold red] reveal.js vendor directory not found: {REVEAL_VENDOR}")
        CONSOLE.print("Run 'git clone https://github.com/hakimel/reveal.js revealjs' first.")
        exit(1)
        
    # Ensure the output directory exists
    if not OUTPUT_HTML.parent.exists():
        CONSOLE.print(f"[yellow]Note:[/yellow] Creating output directory: [yellow]{OUTPUT_HTML.parent}[/yellow]")
        OUTPUT_HTML.parent.mkdir(parents=True, exist_ok=True)


# --- Build Execution ---
def run_pandoc():
    """Constructs and executes the Pandoc command."""
    CONSOLE.print(f"[bold blue]Starting build...[/bold blue] ({SOURCE_MD} -> {OUTPUT_HTML})")

    # 1. Define the core Pandoc arguments
    pandoc_args = [
        # Call Pandoc
        "pandoc",
        
        # Input file
        str(SOURCE_MD),
        
        # Output format: Using the dedicated revealjs writer (no problematic extensions)
        "-t", "revealjs",
        
        # Output file path
        "-o", str(OUTPUT_HTML),

        # This copies the necessary reveal.js files into the 'dist/' folder
        "--standalone", 
        
        # Embed all external resources (CSS, JS, local images) into the HTML
        "--embed-resources",
        
        # Fixes vertical stacking: Ensures ONLY H1 headers start a new top-level horizontal slide.
        "--slide-level=1",
        
        # Enable slide numbering
        "-V", "slide-number=true",
        
        # CRITICAL: Use the path to the vendored reveal.js files for asset resolution
        "-V", f"revealjs-url={REVEAL_VENDOR}",
        
        # Use the Pandoc theme variable to select the theme. 
        "-V", "theme=black", 

        # Use --strip-comments to clean up HTML output (optional)
        "--strip-comments",
    ]

    try:
        # Execute the command
        CONSOLE.print(f"[dim]Running command: {' '.join(str(a) for a in pandoc_args)}[/dim]")
        
        result = subprocess.run(pandoc_args, check=True, capture_output=True, text=True)
        
        # Success message
        CONSOLE.print("[bold green]Build complete![/bold green]")
        CONSOLE.print(f"Output written to: [yellow]{OUTPUT_HTML}[/yellow]")
        
        # Display any warnings/errors from Pandoc
        if result.stderr:
            CONSOLE.print(f"[yellow]Pandoc Messages:[/yellow]\n{result.stderr}")
            
    except subprocess.CalledProcessError as e:
        CONSOLE.print(f"[bold red]Build Failed![/bold red]")
        CONSOLE.print(f"Command: {' '.join(str(a) for a in pandoc_args)}")
        CONSOLE.print(f"Error output:\n{e.stderr}")
        exit(1)
    except FileNotFoundError:
        CONSOLE.print("[bold red]Error:[/bold red] Pandoc command not found. Is Pandoc installed and in your PATH?")
        exit(1)


if __name__ == "__main__":
    check_paths()
    run_pandoc()