import requests
import socket
from rich.console import Console
from rich.table import Table
from rich.progress import track
from rich.prompt import Prompt
from rich.panel import Panel
from rich.align import Align

console = Console()

def get_domain_ip(domain):
    try:
        # Clean the domain string and resolve the IP.
        domain = domain.replace('http://', '').replace('https://', '').split('/')[0]
        ip = socket.gethostbyname(domain)
        return ip
    except socket.error as e:
        return f"Could not resolve IP: {e}"

def detect_cdn(headers, ip):
    cdn_providers = {
        "Cloudflare": ["cf-ray", "cf-cache-status"],
        "Akamai": ["akamai", "x-akamai-transformed"],
        "Fastly": ["fastly", "x-fastly-request-id"],
        "Google CDN": ["x-goog-meta"],
        "BunnyCDN": ["bunnycdn", "server: bunnycdn"]
    }
    
    for cdn, identifiers in cdn_providers.items():
        for key in identifiers:
            if key.lower() in [h.lower() for h in headers.keys()]:
                return cdn
    return "Unknown"

def check_http_response(url):
    results = {}
    protocols = ["http://", "https://"]
    
    for protocol in protocols:
        full_url = protocol + url if not url.startswith(('http://', 'https://')) else url
        try:
            response = requests.get(full_url, timeout=5)
            ip = get_domain_ip(full_url)
            cdn = detect_cdn(response.headers, ip)
            
            results[protocol] = {
                "status_code": response.status_code,
                "url": full_url,
                "headers": dict(response.headers),
                "cdn": cdn,
                "ip": ip
            }
        except requests.exceptions.RequestException as e:
            results[protocol] = {
                "url": full_url,
                "error": str(e),
                "cdn": "Unknown",
                "ip": get_domain_ip(full_url)
            }
    
    return results

def check_response_from_file(file_path):
    output_file = "response.txt"  # File where results will be saved in the same directory
    try:
        with open(file_path, 'r') as file:
            hosts = file.read().splitlines()
    except FileNotFoundError:
        error_message = f"Error: File '{file_path}' not found.\n"
        console.print(f"[red]{error_message}[/red]")
        with open(output_file, "w") as outfile:
            outfile.write(error_message)
        return
    
    # Open the output file in write mode so previous results are overwritten.
    with open(output_file, "w") as outfile:
        for host in track(hosts, description="Processing hosts", total=len(hosts)):
            if not host.strip():
                continue
            
            response = check_http_response(host)
            
            for protocol, data in response.items():
                output = f"Results for {data['url']}\n"
                output += f"IP: {data['ip']}\n"
                if "error" in data:
                    output += f"Status: Error\n"
                    output += f"Error: {data['error']}\n"
                else:
                    output += f"Status Code: {data['status_code']}\n"
                    output += f"Status: OK\n"
                output += f"CDN: {data['cdn']}\n"
                output += "-" * 40 + "\n"
                
                # Print the result to the console.
                console.print(output)
                # Write the result to the file.
                outfile.write(output)

def check_ip_from_file(file_path):
    output_file = "ip_response.txt"  # Separate file for IP results
    try:
        with open(file_path, 'r') as file:
            hosts = file.read().splitlines()
    except FileNotFoundError:
        error_message = f"Error: File '{file_path}' not found.\n"
        console.print(f"[red]{error_message}[/red]")
        with open(output_file, "w") as outfile:
            outfile.write(error_message)
        return
    
    with open(output_file, "w") as outfile:
        for host in track(hosts, description="Resolving IPs", total=len(hosts)):
            if not host.strip():
                continue
            
            ip = get_domain_ip(host)
            output = f"IP for {host}: {ip}\n" + "-" * 40 + "\n"
            
            console.print(output)
            outfile.write(output)

def display_banner():
    # Clear the terminal.
    console.clear()
    # Prepare and center the banner text.
    banner_text = "[bold green]SSLABLK Checker Tool[/bold green]"
    centered_banner = Align.center(banner_text)
    # Create a panel with the centered banner.
    panel = Panel(centered_banner, border_style="bright_blue")
    console.print(panel)

def display_menu():
    panel = Panel.fit(
        "[bold blue]Options:[/bold blue]\n1. Check HTTP/HTTPS Response for a list of hosts\n2. Check IP Address for a list of hosts", 
        title="Menu", 
        border_style="green"
    )
    console.print(panel)

def main():
    display_banner()
    display_menu()
    choice = Prompt.ask("Enter your choice", choices=["1", "2"], default="1")
    file_path = Prompt.ask("Enter the path to the text file (e.g., hosts.txt)")
    
    if choice == '1':
        check_response_from_file(file_path)
    elif choice == '2':
        check_ip_from_file(file_path)
    else:
        console.print("[red]Invalid choice. Please enter 1 or 2.[/red]")

if __name__ == "__main__":
    main()
