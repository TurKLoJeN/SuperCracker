import pyzipper
import rarfile
import os
import time

GREEN = '\033[92m'
RED = '\033[91m'
BOLD_RED = '\033[1;91m'
PINK = '\033[95m'
BOLD = '\033[1m'
RESET = '\033[0m'

MESSAGES = {
    'EN': {
        'char_sets': 'Enter character sets (a: lowercase, A: uppercase, 1: digits, ?: special characters): ',
        'min_length': 'Enter minimum password length: ',
        'max_length': 'Enter maximum password length: ',
        'file_path': 'Enter the path of the ZIP or RAR file to crack: ',
        'file_path_entered': 'File path entered: ',
        'passwords_saved': 'Passwords saved to passlist.txt',
        'invalid_file_path': 'Invalid file path. Please check the path and try again.',
        'password_list_not_found': 'Password list file not found. Please check for \'passlist.txt\'.',
        'unsupported_file_format': 'Unsupported file format',
        'zip_password_found': 'ZIP Password found: ',
        'rar_password_found': 'RAR Password found: ',
        'not_found': 'Password not found',
        'progress': 'Progress: ',
        'estimated_time_left': 'Estimated Time Left: ',
        'password': 'Password ',
        'of': ' of ',
        'percentage': '{:.2f}%'
    },
    'TR': {
        'char_sets': 'Karakter setlerini girin (a: küçük harfler, A: büyük harfler, 1: sayılar, ?: özel işaretler): ',
        'min_length': 'Minimum şifre uzunluğunu girin: ',
        'max_length': 'Maksimum şifre uzunluğunu girin: ',
        'file_path': 'Kırılacak ZIP veya RAR dosyasının yolunu girin: ',
        'file_path_entered': 'Girilen dosya yolu: ',
        'passwords_saved': 'Şifreler passlist.txt dosyasına kaydedildi',
        'invalid_file_path': 'Geçersiz dosya yolu. Lütfen yolu kontrol edin ve tekrar deneyin.',
        'password_list_not_found': 'Şifre listesi dosyası bulunamadı. Lütfen \'passlist.txt\' dosyasını kontrol edin.',
        'unsupported_file_format': 'Desteklenmeyen dosya formatı',
        'zip_password_found': 'ZIP Şifresi bulundu: ',
        'rar_password_found': 'RAR Şifresi bulundu: ',
        'not_found': 'Şifre bulunamadı',
        'progress': 'İlerleme: ',
        'estimated_time_left': 'Tahmini Kalan Süre: ',
        'password': 'Şifre ',
        'of': ' / ',
        'percentage': '{:.2f}%'
    }
}

def display_banner():
    banner = """
:'######::'##::::'##:'########::'########:'########::'######::'########:::::'###:::::'######::'##:::'##:'########:'########:::::::::::::::::'##::::'##::::'##::::::::::'#####:::
'##... ##: ##:::: ##: ##.... ##: ##.....:: ##.... ##:'##... ##: ##.... ##:::'## ##:::'##... ##: ##::'##:: ##.....:: ##.... ##:::::::::::::::: ##:::: ##::'####:::::::::'##.. ##::
 ##:::..:: ##:::: ##: ##:::: ##: ##::::::: ##:::: ##: ##:::..:: ##:::: ##::'##:. ##:: ##:::..:: ##:'##::: ##::::::: ##:::: ##:::::::::::::::: ##:::: ##::.. ##::::::::'##:::: ##:
. ######:: ##:::: ##: ########:: ######::: ########:: ##::::::: ########::'##:::. ##: ##::::::: #####:::: ######::: ########:::::'#######:::: ##:::: ##:::: ##:::::::: ##:::: ##:
:..... ##: ##:::: ##: ##.....::: ##...:::: ##.. ##::: ##::::::: ##.. ##::: #########: ##::::::: ##. ##::: ##...:::: ##.. ##::::::........::::. ##:: ##::::: ##:::::::: ##:::: ##:
'##::: ##: ##:::: ##: ##:::::::: ##::::::: ##::. ##:: ##::: ##: ##::. ##:: ##.... ##: ##::: ##: ##:. ##:: ##::::::: ##::. ##::::::::::::::::::. ## ##:::::: ##:::'###:. ##:: ##::
. ######::. #######:: ##:::::::: ########: ##:::. ##:. ######:: ##:::. ##: ##:::: ##:. ######:: ##::. ##: ########: ##:::. ##::::::::::::::::::. ###:::::'######: ###::. #####:::
:......::::.......:::..:::::::::........::..:::::..:::......:::..:::::..::..:::::..:::......:::..::::..::........::..:::::..::::::::::::::::::::...::::::......::...::::.....::::

  _                    _       ___                              
 /   _   _|  _   _|   |_)       |     ._ |/ |   _    |  _  |\ | 
 \_ (_) (_| (/_ (_|   |_) \/    | |_| |  |\ |_ (_) \_| (/_ | \| 
    """
    print(f"{BOLD_RED}{banner}{RESET}")

def get_language():
    while True:
        choice = input(f"{GREEN}Select language (1 - EN, 2 - TR): {RESET}").strip()
        if choice == '1':
            return 'EN'
        elif choice == '2':
            return 'TR'
        else:
            print(f"{RED}Invalid choice. Please enter 1 for English or 2 for Turkish.{RESET}")

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def format_number(number):
    return "{:,}".format(number).replace(',', '.')

def load_passwords(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def generate_passwords(characters, min_length, max_length, start_time):
    from itertools import product
    
    all_chars = {
        'a': 'abcdefghijklmnopqrstuvwxyz',
        'A': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
        '1': '0123456789',
        '?': '!@#$%^&*()_+-=[]{}|;:,.<>?/~`'
    }

    char_set = ''.join(all_chars[char] for char in characters if char in all_chars)
    
    if not char_set:
        print(GREEN + "No valid character sets provided. Exiting..." + RESET)
        return
    
    total_combinations = sum(len(char_set) ** length for length in range(min_length, max_length + 1))
    print(f"{GREEN}Generating {BOLD_RED}{format_number(total_combinations)}{RESET} passwords...{RESET}")

    with open('passlist.txt', 'w') as file:
        count = 0
        for length in range(min_length, max_length + 1):
            for password in product(char_set, repeat=length):
                file.write(''.join(password) + '\n')
                count += 1
                
                elapsed_time = time.time() - start_time
                progress = count / total_combinations * 100
                if count == 0:
                    estimated_time = 0
                else:
                    estimated_time = (elapsed_time / count) * (total_combinations - count)
                
                print(f"\r{GREEN}{MESSAGES[language]['progress']}{BOLD_RED}{format_number(count)}{RESET}/{BOLD_RED}{format_number(total_combinations)}{RESET} - {GREEN}{MESSAGES[language]['estimated_time_left']}{BOLD_RED}{format_time(estimated_time)}{RESET}", end='')
        print()

def crack_zip(zip_file_path, passwords):
    try:
        with pyzipper.AESZipFile(zip_file_path, 'r') as zip_file:
            total_passwords = len(passwords)
            start_time = time.time()

            print(f"\n{GREEN}Total passwords to try: {BOLD_RED}{format_number(total_passwords)}{RESET}")

            for index, password in enumerate(passwords):
                try:
                    zip_file.extractall(pwd=password.encode())
                    elapsed_time = time.time() - start_time
                    print(f"\n{GREEN}{MESSAGES[language]['zip_password_found']}{BOLD_RED}{password}{RESET}")
                    print(f"{PINK}Found in {BOLD}{int(elapsed_time // 60)}{RESET} minutes and {BOLD}{int(elapsed_time % 60)}{RESET} seconds")
                    print(f"{PINK}Password was at position {BOLD}{index + 1}{RESET} in the list{RESET}")
                    return
                except (RuntimeError, pyzipper.BadZipFile, pyzipper.LargeZipFile):
                    pass
                
                progress = (index + 1) / total_passwords * 100
                elapsed_time = time.time() - start_time
                estimated_time = (elapsed_time / (index + 1)) * (total_passwords - (index + 1))
                
                print(f"\r{GREEN}{MESSAGES[language]['progress']}{BOLD_RED}{progress:.2f}%{RESET} - {GREEN}{MESSAGES[language]['estimated_time_left']}{BOLD_RED}{format_time(estimated_time)}{RESET}", end='')
    except FileNotFoundError:
        print(RED + MESSAGES[language]['invalid_file_path'] + RESET)

def crack_rar(rar_file_path, passwords):
    try:
        with rarfile.RarFile(rar_file_path) as rar_file:
            total_passwords = len(passwords)
            start_time = time.time()

            print(f"\n{GREEN}Total passwords to try: {BOLD_RED}{format_number(total_passwords)}{RESET}")

            for index, password in enumerate(passwords):
                try:
                    rar_file.extractall(pwd=password)
                    elapsed_time = time.time() - start_time
                    print(f"\n{GREEN}{MESSAGES[language]['rar_password_found']}{BOLD_RED}{password}{RESET}")
                    print(f"{PINK}Found in {BOLD}{int(elapsed_time // 60)}{RESET} minutes and {BOLD}{int(elapsed_time % 60)}{RESET} seconds")
                    print(f"{PINK}Password was at position {BOLD}{index + 1}{RESET} in the list{RESET}")
                    return
                except rarfile.BadRarFile:
                    pass
                except rarfile.Error:
                    pass
                
                progress = (index + 1) / total_passwords * 100
                elapsed_time = time.time() - start_time
                estimated_time = (elapsed_time / (index + 1)) * (total_passwords - (index + 1))
                
                print(f"\r{GREEN}{MESSAGES[language]['progress']}{BOLD_RED}{progress:.2f}%{RESET} - {GREEN}{MESSAGES[language]['estimated_time_left']}{BOLD_RED}{format_time(estimated_time)}{RESET}", end='')
    except FileNotFoundError:
        print(RED + MESSAGES[language]['invalid_file_path'] + RESET)

display_banner()
language = get_language()

char_sets = input(GREEN + MESSAGES[language]['char_sets'] + RESET).strip()
min_length = int(input(GREEN + MESSAGES[language]['min_length'] + RESET).strip())
max_length = int(input(GREEN + MESSAGES[language]['max_length'] + RESET).strip())

start_time = time.time()
generate_passwords(char_sets, min_length, max_length, start_time)
print(GREEN + MESSAGES[language]['passwords_saved'] + RESET)

file_path = input(GREEN + MESSAGES[language]['file_path'] + RESET).strip()
print(GREEN + MESSAGES[language]['file_path_entered'] + file_path + RESET)

if os.path.exists('passlist.txt'):
    passwords = load_passwords('passlist.txt')
    if file_path.endswith('.zip'):
        crack_zip(file_path, passwords)
    elif file_path.endswith('.rar'):
        crack_rar(file_path, passwords)
    else:
        print(RED + MESSAGES[language]['unsupported_file_format'] + RESET)
else:
    print(RED + MESSAGES[language]['password_list_not_found'] + RESET)
