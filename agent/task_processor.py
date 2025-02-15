# agent/task_processor.py
import os
import subprocess
import json
import sqlite3
import glob
from datetime import datetime
import re

from agent.llm_client import call_llm

def process_task(task: str) -> dict:
    task_lower = task.lower()
    if "install uv" in task_lower and "datagen.py" in task:
        return task_a1(task)
    elif "format" in task_lower and "/data/format.md" in task_lower:
        return task_a2(task)
    elif "/data/dates.txt" in task_lower and "wednesday" in task_lower:
        return task_a3(task, day="wednesday")
    elif "/data/contacts.json" in task_lower and "sort" in task_lower:
        return task_a4(task)
    elif "/data/logs" in task_lower and ".log" in task_lower:
        return task_a5(task)
    elif "/data/docs/" in task_lower and "index" in task_lower:
        return task_a6(task)
    elif "/data/email.txt" in task_lower:
        return task_a7(task)
    elif "/data/credit-card.png" in task_lower:
        return task_a8(task)
    elif "/data/comments.txt" in task_lower:
        return task_a9(task)
    elif "/data/ticket-sales.db" in task_lower:
        return task_a10(task)
    else:
        # For business tasks B3 to B10 (and bonus tasks), you can add more branches.
        return {"status": "error", "message": "Task not recognized or not implemented."}

def task_a1(task: str) -> dict:
    """
    A1. Install uv (if required) and run datagen.py from:
         https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py
         with ${user.email} as the only argument.
    """
    try:
        # Check if 'uv' is installed (simulate by checking the command version)
        try:
            subprocess.run(["uv", "--version"], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            # Simulate installing uv (for a real system, you might run: pip install uv)
            subprocess.run(["pip", "install", "uv"], check=True)
        # Get the user email from an environment variable (set USER_EMAIL before running)
        user_email = os.environ.get("USER_EMAIL", "user@example.com")
        # Download datagen.py from the given URL
        datagen_url = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
        datagen_path = "/tmp/datagen.py"
        import requests
        r = requests.get(datagen_url)
        if r.status_code != 200:
            return {"status": "error", "message": "Failed to download datagen.py"}
        with open(datagen_path, "w", encoding="utf-8") as f:
            f.write(r.text)
        # Run datagen.py with the user email as argument
        subprocess.run(["python3", datagen_path, user_email], check=True)
        return {"status": "success", "details": "A1 executed"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def task_a2(task: str) -> dict:
    """
    A2. Format the contents of /data/format.md using prettier@3.4.2 (in-place).
    """
    try:
        # Check if prettier is installed (assume it is available)
        cmd = ["prettier", "--version"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if "3.4.2" not in result.stdout:
            # (Optionally install or warn; for now, we assume the correct version is used.)
            pass
        file_path = "/data/format.md"
        cmd = ["prettier", "--write", file_path]
        subprocess.run(cmd, check=True)
        return {"status": "success", "details": "A2 executed"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def task_a3(task: str, day="wednesday") -> dict:
    """
    A3. Count the number of Wednesdays in /data/dates.txt and write the number
         to /data/dates-wednesdays.txt.
    """
    try:
        file_path = "/data/dates.txt"
        output_path = "/data/dates-wednesdays.txt"
        if not os.path.exists(file_path):
            return {"status": "error", "message": f"{file_path} does not exist"}
        count = 0
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    dt = datetime.strptime(line, "%Y-%m-%d")
                    # Wednesday is weekday()==2 (Monday=0)
                    if day.lower() == "wednesday" and dt.weekday() == 2:
                        count += 1
                except:
                    continue
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(str(count))
        return {"status": "success", "details": f"A3 executed, count={count}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def task_a4(task: str) -> dict:
    """
    A4. Sort the contacts in /data/contacts.json by last_name then first_name,
         and write the sorted array to /data/contacts-sorted.json.
    """
    try:
        input_path = "/data/contacts.json"
        output_path = "/data/contacts-sorted.json"
        if not os.path.exists(input_path):
            return {"status": "error", "message": f"{input_path} does not exist"}
        with open(input_path, "r", encoding="utf-8") as f:
            contacts = json.load(f)
        sorted_contacts = sorted(contacts, key=lambda x: (x.get("last_name", ""), x.get("first_name", "")))
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(sorted_contacts, f, indent=2)
        return {"status": "success", "details": "A4 executed"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def task_a5(task: str) -> dict:
    """
    A5. From /data/logs/ take the 10 most recent .log files and write the first
         line of each (most recent first) to /data/logs-recent.txt.
    """
    try:
        logs_dir = "/data/logs/"
        output_path = "/data/logs-recent.txt"
        log_files = glob.glob(os.path.join(logs_dir, "*.log"))
        if not log_files:
            return {"status": "error", "message": "No log files found"}
        # Sort files by modification time (descending)
        log_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        recent_logs = log_files[:10]
        lines = []
        for log_file in recent_logs:
            with open(log_file, "r", encoding="utf-8") as f:
                first_line = f.readline().strip()
                lines.append(first_line)
        with open(output_path, "w", encoding="utf-8") as f:
            for line in lines:
                f.write(line + "\n")
        return {"status": "success", "details": "A5 executed"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def task_a6(task: str) -> dict:
    """
    A6. In /data/docs/, for every Markdown (.md) file, extract the first H1 (a line starting with "#")
         and create an index JSON mapping filename (relative to /data/docs/) to the title.
         Write the JSON to /data/docs/index.json.
    """
    try:
        docs_dir = "/data/docs/"
        output_path = "/data/docs/index.json"
        if not os.path.exists(docs_dir):
            return {"status": "error", "message": f"{docs_dir} does not exist"}
        index = {}
        for root, dirs, files in os.walk(docs_dir):
            for file in files:
                if file.endswith(".md"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8") as f:
                        for line in f:
                            if line.startswith("#"):
                                title = line.lstrip("#").strip()
                                # Get the filename relative to docs_dir
                                rel_path = os.path.relpath(file_path, docs_dir)
                                index[rel_path] = title
                                break
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=2)
        return {"status": "success", "details": "A6 executed"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def task_a7(task: str) -> dict:
    """
    A7. Read /data/email.txt, pass its contents to an LLM (via our llm_client)
         to extract the sender’s email address, and write the address to /data/email-sender.txt.
    """
    try:
        input_path = "/data/email.txt"
        output_path = "/data/email-sender.txt"
        if not os.path.exists(input_path):
            return {"status": "error", "message": f"{input_path} does not exist"}
        with open(input_path, "r", encoding="utf-8") as f:
            content = f.read()
        prompt = f"Extract the sender's email address from the following email message:\n\n{content}\n\nSender email:"
        sender_email = call_llm(prompt)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(sender_email.strip())
        return {"status": "success", "details": "A7 executed"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def task_a8(task: str) -> dict:
    """
    A8. Read the image /data/credit-card.png, send it to the LLM (encoded in base64)
         to extract the credit card number, remove any spaces, and write it to /data/credit-card.txt.
    """
    try:
        input_path = "/data/credit-card.png"
        output_path = "/data/credit-card.txt"
        if not os.path.exists(input_path):
            return {"status": "error", "message": f"{input_path} does not exist"}
        import base64
        with open(input_path, "rb") as f:
            img_data = f.read()
        img_b64 = base64.b64encode(img_data).decode("utf-8")
        prompt = f"Extract the credit card number from the following image data (base64 encoded):\n\n{img_b64}\n\nCredit card number (no spaces):"
        card_number = call_llm(prompt)
        card_number = card_number.replace(" ", "").strip()
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(card_number)
        return {"status": "success", "details": "A8 executed"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def task_a9(task: str) -> dict:
    """
    A9. Read /data/comments.txt (a list of comments, one per line), find the most similar pair
         (using a simple similarity metric), and write them (one per line) to /data/comments-similar.txt.
    """
    try:
        input_path = "/data/comments.txt"
        output_path = "/data/comments-similar.txt"
        if not os.path.exists(input_path):
            return {"status": "error", "message": f"{input_path} does not exist"}
        with open(input_path, "r", encoding="utf-8") as f:
            comments = [line.strip() for line in f if line.strip()]
        if len(comments) < 2:
            return {"status": "error", "message": "Not enough comments to compare"}
        # Use a naive similarity: count common words
        def similarity(c1, c2):
            set1 = set(c1.split())
            set2 = set(c2.split())
            return len(set1.intersection(set2))
        max_sim = -1
        pair = ("", "")
        for i in range(len(comments)):
            for j in range(i+1, len(comments)):
                sim = similarity(comments[i], comments[j])
                if sim > max_sim:
                    max_sim = sim
                    pair = (comments[i], comments[j])
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(pair[0] + "\n" + pair[1])
        return {"status": "success", "details": "A9 executed"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def task_a10(task: str) -> dict:
    """
    A10. In the SQLite database /data/ticket-sales.db (table "tickets" with columns type, units, price),
         calculate the total sales for rows where type is "Gold" (i.e. SUM(units*price))
         and write the result to /data/ticket-sales-gold.txt.
    """
    try:
        db_path = "/data/ticket-sales.db"
        output_path = "/data/ticket-sales-gold.txt"
        if not os.path.exists(db_path):
            return {"status": "error", "message": f"{db_path} does not exist"}
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        query = "SELECT SUM(units * price) FROM tickets WHERE type = 'Gold';"
        cursor.execute(query)
        result = cursor.fetchone()
        total_sales = result[0] if result[0] is not None else 0
        conn.close()
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(str(total_sales))
        return {"status": "success", "details": "A10 executed"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

