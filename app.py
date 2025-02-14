import requests
import socket
from rich.console import Console
from rich.table import Table
from rich.progress import track
from rich.prompt import Prompt
from rich.panel import Panel
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.align import Align

console = Console()

def display_banners():
    console.clear()
    banner_text = "[bold green]SSLABLK Checker Tool[/bold green]"
    ascii_art = """
       (`.  : \\               __..----..__
        `.`.| |:          _,-':::''' '  `:`-._
          `.:\||       _,':::::'         `::::`-.
            \\`|    _,':::::::'     `:.     `':::`.
             ;` `-''  `::::::.                  `::\\
          ,-'      .::'  `:::::.         `::..    `:\\
        ,' /_) -.            `::.           `:.     |
      ,'.:     `    `:.        `:.     .::.          \\
 __,-'   ___,..-''-.  `:.        `.   /::::.         |
|):'_,--'           `.    `::..       |::::::.      ::\\
 `-'                 |`--.:_::::|_____\\::::::::.__  ::|
                     |   _/|::::|      \\::::::|::/\\  :|
                     /:./  |:::/        \\__:::):/  \\  :\\
                   ,'::'  /:::|        ,'::::/_/    `. ``-.__
     KUDDA VPN    ''''   (//|/\\      ,';':,-'         `-.__  `'--..__
                                                           `''---::::'
    """
    centered_banner = Align.center(banner_text)
    centered_ascii = Align.center(ascii_art)
    console.print(centered_banner)
    console.print(centered_ascii)

def get_domain_ip(domain):
    try:
        domain = domain.replace('http://', '').replace('https://', '').split('/')[0]
        ip = socket.gethostbyname(domain)
        return ip
    except socket.error as e:
        return f"Could not resolve IP: {e}"

def detect_cdn(headers, ip):
    cdn_providers = {
        "Cloudflare": ["cf-ray", "cf-cache-status", "cf-connecting-ip"],
        "Akamai": ["akamai", "x-akamai-transformed", "x-akamai-request-id"],
        "Fastly": ["fastly", "x-fastly-request-id", "x-fastly-cache-status"],
        "Google CDN": ["x-goog-meta", "x-google-backend", "x-goog-origin"],
        "BunnyCDN": ["bunnycdn", "server: bunnycdn", "x-bunnycdn-cache-status"],
        "KeyCDN": ["x-keycdn-request-id", "x-keycdn-cache-status"],
        "Cloudfront": ["via", "x-cache", "x-amz-cf-id", "x-amz-cf-pop"],
        "CDN77": ["cdn77", "x-cdn77-request-id", "x-cdn77-cache-status"],
        "StackPath": ["x-stackpath", "stackpath", "x-stackpath-cdn"],
        "Incapsula": ["x-incapsula", "incapsula", "x-incapsula-sid"],
        "CacheFly": ["cachefly", "cf-cache-status", "x-cache"],
        "Microsoft Azure CDN": ["x-ms-cdn", "x-azure-request-id", "x-ms-origin"],
        "Cloudflare Stream": ["cf-stream", "cf-ray", "cf-cache-status"],
        "ChinaCache": ["chinacache", "x-cdn-origin", "x-chinacache-request-id"],
        "Rackspace CDN": ["rackcdn", "x-rackcdn-cache-status"],
        "MaxCDN": ["maxcdn", "x-maxcdn-request-id", "x-maxcdn-cache-status"],
        "CDN Planet": ["cdnplanet", "x-cdn-planet-id"],
        "Imperva": ["x-imperva", "imperva", "x-imperva-cookie"],
        "Level3": ["level3", "x-level3-cache-status"],
        "Tencent Cloud CDN": ["tencentcloud", "x-tencent-cdn"],
        "Varnish": ["via", "x-varnish", "x-varnish-request-id"],
        "CDNify": ["cdnify", "x-cdnify-request-id"],
        "ArvanCloud": ["x-arv-cdn-request-id", "arvancloud", "x-arvancloud-cache-status"],
        "Sucuri": ["sucuri", "x-sucuri-cache"],
        "Limelight Networks": ["limelight", "x-limelight-cache-status"],
        "EdgeCast": ["edgecast", "x-edgecast-cache-status"],
        "NetDNA": ["netdna", "x-netdna-cache-status"],
        "F5": ["f5", "x-f5-cache-status"],
        "QCDN": ["qcdn", "x-qcdn-cache-status"],
        "Cloudflare Workers": ["cf-worker", "cf-ray", "cf-cache-status"],
        "Alibaba Cloud CDN": ["aliyuncdn", "x-aliyun-cdn-cache-status"],
        "Tata Communications CDN": ["tatacommunications", "x-tatacommunications-cache-status"],
        "Fastly": ["fastly", "x-fastly-request-id", "x-fastly-cache-status"],
        "Akamai CDN": ["akamai", "x-akamai-cache-status"],
        "ChinaNetCenter": ["chinacache", "x-cdn-origin", "x-chinacache-request-id"],
        "Edgecast CDN": ["edgecast", "x-edgecast-cache-status"],
        "QCDN": ["qcdn", "x-qcdn-cache-status"],
        "Jetpack CDN": ["jetpack", "x-jetpack-cache-status"],
        "Webscale CDN": ["webscale", "x-webscale-cache-status"],
        "CDNify": ["cdnify", "x-cdnify-cache-status"],
        "Tata CDN": ["tatacdn", "x-tatacdn-cache-status"],
        "MaxCDN": ["maxcdn", "x-maxcdn-request-id", "x-maxcdn-cache-status"],
        "Edgecast": ["edgecast", "x-edgecast-cache-status"],
        "QCDN": ["qcdn", "x-qcdn-cache-status"],
        "Cloudflare": ["cf-ray", "cf-cache-status", "cf-connecting-ip"],
        "F5": ["f5", "x-f5-cache-status"],
        "ArvanCloud CDN": ["arvancloud", "x-arvancloud-cache-status"],
        "Fastly": ["fastly", "x-fastly-cache-status"],
        "ChinaCache": ["chinacache", "x-cdn-origin", "x-chinacache-request-id"],
        "Level3 CDN": ["level3", "x-level3-cache-status"],
        "CDN77": ["cdn77", "x-cdn77-cache-status"],
        "Cloudfront": ["via", "x-cache", "x-amz-cf-id", "x-amz-cf-pop"],
        "StackPath CDN": ["x-stackpath-cdn", "stackpath-cdn"],
        "ArvanCloud CDN": ["x-arvancloud-cdn", "arvancloud-cdn"]
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
    output_file = "response.txt"
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
                
                console.print(output)
                outfile.write(output)
                outfile.flush()  # Ensures that the result is written immediately

def check_ip_from_file(file_path):
    output_file = "ip_response.txt"
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
            outfile.flush()  # Ensures that the result is written immediately

def display_banner():
    banner_text = "[bold green]SSLABLK Checker Tool[/bold green]"
    centered_banner = Align.center(banner_text)
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
    display_banners()
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
