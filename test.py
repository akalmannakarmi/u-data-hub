import subprocess

# Run a shell command and capture its output
result = subprocess.run(['echo', 'hello word'], capture_output=True, text=True)

# Check if the command was successful
if result.returncode == 0:
    print("Command executed successfully!")
    # Print the output
    print("Output:", result.stdout)
else:
    print("Command failed!")
    # Print the error message
    print("Error:", result.stderr)
