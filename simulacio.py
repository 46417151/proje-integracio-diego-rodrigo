import random
import os
import os.path
import sys
import shutil


def generate_big_random_letters(filename, size):
    """
    generate big random letters/alphabets to a file
    :param filename: the filename
    :param size: the size in bytes
    :return: void
    """
    import random
    import string

    chars = ''.join([random.choice(string.ascii_letters) for i in range(size)])  # 1

    with open(filename, 'w') as f:
        f.write(chars)
    pass


if (not len(sys.argv) == 2):
    print('Necesito tus iniciales')
    sys.exit()

iniciales = sys.argv[1]
users = []
for i in range(1, 4):
    user = iniciales + str(i)
    users.append(user)
print(users)
for user in users:
    cmd = f'useradd {user}'
    os.system(cmd)
    print('excuted:', cmd)

dir = iniciales + '_init'
if os.path.exists(dir):
    print('dir', dir, 'ja existeix')
else:
    os.mkdir(dir)
    print('created:', dir)

for i in range(1, 20):
    fname = 'foo_' + str(i)
    size = random.randint(1, 20) * 1024 * 1024
    extension = random.choice(['bin', 'exe', 'pdf'])
    dir_final = dir
    for i in range(random.randint(1, 4)):
        dir_final = os.path.join(dir_final, random.choice(['d1', 'd2', 'd3']))
    path = os.path.join(dir_final, f'{fname}.{extension}')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    generate_big_random_letters(path, size)
    user = random.choice(users)
    shutil.chown(path, user, user)
    print(f'Created {path} amb {size} bytes propietary {user}')
    if (random.random() > 0.9):
        extension = random.choice(['pdf', 'bin', 'exe'])
        shutil.move(path, path + '.' + extension)




