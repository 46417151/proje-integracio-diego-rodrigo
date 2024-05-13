import os
import random
from faker import Faker

# Create a main directory
main_dir = "P1_rbg"
os.makedirs(main_dir, exist_ok=True)

# Create a directory for files
files_dir = os.path.join(main_dir, "files")
os.makedirs(files_dir, exist_ok=True)

# Create users
users = ["rbg1", "rbg2", "rbg3"]

# Create files
fake = Faker()
for i in range(10):  # Change this number to create more or less files
    file_size = random.randint(1, 20)  # File size in KB
    file_name = fake.file_name(category=None, extension=None)
    file_path = os.path.join(files_dir, file_name)
    
    # Assign random user to file
    file_owner = random.choice(users)
    
    # Create file with random size
    with open(file_path, "wb") as f:
        f.write(os.urandom(file_size * 1024))  # Convert KB to bytes

    # Change file owner
    os.system(f"chown {file_owner} {file_path}")

    # Randomly assign suspicious extensions
    if random.choice([True, False]):
        suspicious_extension = ".exe"  # Change this to the extension you want
        os.rename(file_path, file_path + suspicious_extension)
