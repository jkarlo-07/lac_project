import subprocess

# Run the first job (update_peak_seasons)
subprocess.run(['python', 'manage.py', 'update_peak_seasons'])

# Run the second job (update_room_prices)
subprocess.run(['python', 'manage.py', 'update_room_prices'])
