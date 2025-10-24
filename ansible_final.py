import subprocess

def showrun(ip_address):
    playbook_showrun_file = 'showrun_playbook.yaml' 
    expected_filename = f"show_run_66070158_{ip_address}.txt"

    # run playbook
    command = [
        'ansible-playbook',
        playbook_showrun_file,
        '-e', f"target_host={ip_address}",
        '-e', f"output_filename={expected_filename}"
    ]
    
    print(f"Running Ansible: {' '.join(command)}")
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        playbook_summary = result.stdout
        print("Ansible Output:\n", playbook_summary) # for debug

        if 'failed=0' in playbook_summary and 'unreachable=0' in playbook_summary:
            print(f"SUCCESS: Ansible playbook completed. File saved as {expected_filename}")
            # --- Return the filename so the main script can attach it ---
            return expected_filename
        else:
            print("ERROR: Ansible playbook reported failures.")
            return "error"

    except subprocess.CalledProcessError as e:
        # This catches errors if ansible-playbook itself fails to run or returns a non-zero exit code
        print(f"ERROR: Ansible command failed with exit code {e.returncode}")
        print("Standard Error:\n", e.stderr)
        return "error"
    except FileNotFoundError:
        print("ERROR: 'ansible-playbook' command not found. Is Ansible installed and in your PATH?")
        return "error"
    except Exception as e:
        # Catch any other unexpected errors
        print(f"ERROR: An unexpected error occurred: {e}")
        return "error"