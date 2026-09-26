import tkinter as tk
from tkinter import ttk, messagebox
import threading
import whois

def perform_whois():
    domain = entry_domain.get().strip()
    
    # Clean up input in case user pastes a URL
    domain = domain.replace("https://", "").replace("http://", "").split("/")[0]
    
    if not domain:
        messagebox.showerror("Input Error", "Please enter a valid domain name.")
        return
        
    btn_scan.config(state=tk.DISABLED)
    lbl_status.config(text="Querying WHOIS databases...", fg="#e67e22")
    text_output.config(state=tk.NORMAL)
    text_output.delete(1.0, tk.END)
    text_output.insert(tk.END, f"[*] Fetching OSINT data for: {domain}\n")
    text_output.insert(tk.END, "-" * 55 + "\n")
    
    # Run in background thread
    threading.Thread(target=fetch_data, args=(domain,), daemon=True).start()

def fetch_data(domain):
    try:
        # Perform the WHOIS query using the 'whois' library
        domain_info = whois.whois(domain)
        
        # Format dates nicely if they exist
        creation_date = format_date(domain_info.creation_date)
        expiration_date = format_date(domain_info.expiration_date)
        updated_date = format_date(domain_info.updated_date)
        
        # Format the output
        insert_text("Registrar", domain_info.registrar)
        insert_text("WHOIS Server", domain_info.whois_server)
        insert_text("Creation Date", creation_date)
        insert_text("Updated Date", updated_date)
        insert_text("Expiration Date", expiration_date)
        insert_text("Registrant Name", domain_info.name)
        insert_text("Registrant Org", domain_info.org)
        insert_text("Registrant Country", domain_info.country)
        insert_text("Registrant Email", domain_info.emails)
        
        # Handle multiple name servers
        ns = domain_info.name_servers
        if isinstance(ns, list):
            ns = ", ".join(ns)
        insert_text("Name Servers", ns)

        text_output.insert(tk.END, "-" * 55 + "\n[*] Intelligence gathering complete.\n")
        lbl_status.config(text="Query Successful", fg="#27ae60")
        
    except whois.parser.PywhoisError:
        text_output.insert(tk.END, f"[!] No WHOIS records found for '{domain}'. It may be unregistered or invalid.\n")
        lbl_status.config(text="No Records Found", fg="#c0392b")
    except Exception as e:
        text_output.insert(tk.END, f"[!] An error occurred during the query: {str(e)}\n")
        lbl_status.config(text="Query Failed", fg="#c0392b")
        
    text_output.config(state=tk.DISABLED)
    btn_scan.config(state=tk.NORMAL)

def format_date(date_obj):
    if not date_obj:
        return "N/A"
    if isinstance(date_obj, list):
        return date_obj[0].strftime("%Y-%m-%d %H:%M:%S")
    return date_obj.strftime("%Y-%m-%d %H:%M:%S")

def insert_text(label, value):
    if not value:
        value = "REDACTED / PRIVACY PROTECTED"
    if isinstance(value, list):
        value = ", ".join(value)
    text_output.insert(tk.END, f"{label+':':<20} {value}\n")

# --- Tkinter GUI Layout ---
root = tk.Tk()
root.title("SOC Toolkit - WHOIS OSINT Tool")
root.geometry("600x500")
root.resizable(False, False)

frame = ttk.Frame(root, padding="15")
frame.pack(fill=tk.BOTH, expand=True)

lbl_title = tk.Label(frame, text="Domain Intelligence (WHOIS) Lookup", font=("Helvetica", 13, "bold"))
lbl_title.pack(anchor="w", pady=(0, 10))

# Input Frame
input_frame = tk.Frame(frame)
input_frame.pack(fill=tk.X, pady=(0, 10))

lbl_domain = tk.Label(input_frame, text="Target Domain:", font=("Helvetica", 10))
lbl_domain.pack(side=tk.LEFT, padx=(0, 5))

entry_domain = ttk.Entry(input_frame, width=30, font=("Helvetica", 10))
entry_domain.pack(side=tk.LEFT, padx=(0, 10))
entry_domain.insert(0, "cisco.com")

btn_scan = tk.Button(input_frame, text="Gather Intelligence", command=perform_whois, bg="#2980b9", fg="white", font=("Helvetica", 9, "bold"))
btn_scan.pack(side=tk.LEFT)

lbl_status = tk.Label(frame, text="Ready", font=("Helvetica", 9, "italic"), fg="#555")
lbl_status.pack(anchor="w", pady=(0, 5))

# Output Console Display
text_frame = tk.Frame(frame)
text_frame.pack(fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(text_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_output = tk.Text(text_frame, font=("Consolas", 10), bg="#1e1e1e", fg="#ecf0f1", yscrollcommand=scrollbar.set)
text_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
text_output.config(state=tk.DISABLED)
scrollbar.config(command=text_output.yview)

root.mainloop()