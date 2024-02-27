import psutil
import time
import pandas as pd
import os
import matplotlib.pyplot as plt
import colorama
from colorama import Fore, Style
colorama.init(autoreset=True)

# Clears screen.
def clear_screen():
    '''
        input:
            None.

        output:
            None, but clears the prompt.
    '''
    if os.name == 'nt':
        os.system('cls')    # For Windows.
    else:
        os.system('clear')  # For Linux and Mac.

# Chooses which color to use for display percentage.
def choose_color(device_usage):
    '''
        input:
            device_usage: a float between (inclusive) 0 and 100 

        output:
            None, but clears the prompt.
    '''
    if device_usage <= 34:
        color = Fore.LIGHTCYAN_EX
    elif device_usage <= 64:
        color = Fore.YELLOW + Style.BRIGHT
    else:
        color = Fore.LIGHTRED_EX
    return color

# Displayer of current usage of CPU and RAM.
def display_usage(cpu_usage, ram_usage, bars=50):
    ''' 
        input:
            cpu_usage, ram_usage: float between (inclusive) 0 and a 100.
            bars: int >= 1. 

        output:
            None, but the function prints out the percent usage of RAM and CPU.
    '''
    
    cpu_percent = (cpu_usage / 100)
    ram_percent = (ram_usage / 100)

    cpu_bar = '█' * int(cpu_percent*bars) + '-'*int(bars - cpu_percent*bars)
    ram_bar = '█' * int(ram_percent*bars) + '-'*int(bars - ram_percent*bars)

    cpu_color = choose_color(cpu_usage)
    ram_color = choose_color(ram_usage)

    print(f'\rCPU Usage:{cpu_color} |{cpu_bar}| {cpu_usage:.2f}%  ', end='')
    print(f'RAM Usage:{ram_color} |{ram_bar}| {ram_usage:.2f}%  ', end="\r")


# Creation of DataFrame with its respective empty columns.
columns = ['timestamp', 'CPU', 'RAM']
df = pd.DataFrame(columns=columns)


# Timer before start.
clear_screen()
for i in range(5, 0, -1):
    
    print(f'Hardware Monitor starts in: {i}', end='\r')
    time.sleep(1)


# Default interface.
clear_screen()
print('HARDWARE MONITOR\n')


start = time.time()
max_ram = 0
max_cpu = 0
i = 0
while True:
    
    try:

        # Storages current usage of CPU and RAM.
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent

        # Verifies if current usage of CPU or RAM is the maximum used until the iteration.
        if (max_cpu < cpu_usage):
            max_cpu = cpu_usage
        if (max_ram < ram_usage):
            max_ram = ram_usage

        # Displays usage of CPU and RAM.
        display_usage(cpu_usage, ram_usage, 40)
        
        # Saves the current usage of CPU and RAM into pandas DataFrame.
        df.loc[i] = [time.time() - start, ram_usage, cpu_usage]
        time.sleep(0.5)

        i += 1

    except KeyboardInterrupt:

        print(f"\n\nCPU peak usage: {max_cpu}%")
        ram_total = psutil.virtual_memory().total
        print(f"RAM peak usage: {(ram_total*max_ram/100)/10**9:.1f}GB ({max_ram}%)")
        
        # Salvation of usage of CPU and RAM into a .xlsx file when user interrupts the execution (Ctrl + C).
        df.to_excel('cpu_ram_data.xlsx', index=False)

        # Plots a graph using the data in 'df'.
        plt.plot(df['timestamp'], df['CPU'], marker='o', color='b', linestyle='-', label='CPU')
        plt.plot(df['timestamp'], df['RAM'], marker='o', color='g', linestyle='-', label='RAM')

        plt.ylim(0, 100)

        plt.xlabel('Timestamp')
        plt.ylabel('Usage (%)')
        plt.title('CPU and RAM Usage Over Time')

        plt.legend()

        plt.savefig('cpu_ram_plot.png')

        plt.show()

        break