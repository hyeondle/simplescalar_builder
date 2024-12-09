import os
import requests
import sys
import datetime

# Clear terminal
def clear_terminal() :
	cmd = "cls" if os.name == "nt" else "clear"
	os.system(cmd)

# Print menu
def print_sim_menu() :
	clear_terminal()
	print('''
Select Simulation
1. Sim-Fast
2. Sim-Safe
3. Sim-Profile
4. Sim-Cache
5. Sim-BPred
6. Sim-Outorder
''')

def default_cache() :
	return ["-cache:dl1 none", "-cache:dl2 none", "-cache:il1 none", "-cache:il2 none", "-tlb:dtlb none", "-tlb:itlb none"]

def ret_sim_order(selection) :
	if selection == 1 :
		return "sim-fast"
	elif selection == 2 :
		return "sim-safe"
	elif selection == 3 :
		return "sim-profile"
	elif selection == 4 :
		return "sim-cache"
	elif selection == 5 :
		return "sim-bpred"
	elif selection == 6 :
		return "sim-outorder"
	else :
		return ""

def print_ben_menu() :
	clear_terminal()
	print('''
Select Benchmark
1. APPLU
2. EQUAKE
3. GCC
4. GZIP
5. MCF
6. WUPWISE
''')

def ret_ben_order(benchmarks) :
	if benchmarks == 1 :
		return "applu"
	elif benchmarks == 2 :
		return "equake"
	elif benchmarks == 3 :
		return "gcc"
	elif benchmarks == 4 :
		return "gzip"
	elif benchmarks == 5 :
		return "mcf"
	elif benchmarks == 6 :
		return "wupwise"
	else :
		return ""

def rco(cache) :
	if cache == 1 :
		return "dl1"
	elif cache == 2 :
		return "dl2"
	elif cache == 3 :
		return "il1"
	elif cache == 4 :
		return "il2"
	elif cache == 5 :
		return "dtlb"
	elif cache == 6 :
		return "itlb"
	else :
		return ""

def print_cache_menu() :
	cache = default_cache()
	while True :
		clear_terminal()
		print(f'''
Select Cache
1. dl1 (level 1 data cache)
2. dl2 (level 2 data cache)
3. il1 (level 1 instruction cache)
4. il2 (level 2 instruction cache)
5. tlb-d (data TLB)
6. tlb-i (instruction TLB)
9. reset inputs
0. setting done

Cache selected: \n{"\n".join(cache)}
''')
		ins = input('Order: ')
		try:
			ins = int(ins)
			if ins == 0:
				break
			elif ins == 9:
				cache = default_cache()
				continue
		except ValueError:
			print("Invalid input. Please enter a number.")
			input("Press Enter to continue...")
			continue
		clear_terminal()
		print(f'''
Selected Cache #: {ins}

Configurations
<nsets> <bsize> <assoc> <repl>

be sure that inputs must be separated by space

nsets: number of sets in the cache
bsize: block size of the cache
assoc: associativity of the cache (# of 'way')
repl: block replacement policy (l=LRU, f=FIFO, r=Random)
''')

		data = list(map(str, input('Inputs : ').split(' ')))
		if len(data) != 4 and len(data) != 1:
			print('Invalid input')
			input('press enter to continue...')
			continue

		tp = "cache" if ins < 5 else "tlb"
		if len(data) == 1 :
			lorder = f"-{tp}:{rco(ins)} none"
		else :
			lorder = f"-{tp}:{rco(ins)} {rco(ins)}:{data[0]}:{data[1]}:{data[2]}:{data[3]}"

		clear_terminal()
		print(f'''
		Your input will be
		{lorder}
		Right? (y/n)
		''')
		confirm = input()
		if confirm == 'n' :
			continue
		cache[ins-1] = lorder
	return cache

def get_order(selection, benchmarks, max_inst, cache) :
	sim = ""
	ben = ""
	rdir = ""
	order = ""

	sim = "./simplescalar/simplesim-3.0/" + ret_sim_order(selection)

	if benchmarks == 1 :
		ben = "./simplescalar/benchmark/applu/applu00.peak.ev6 < ./simplescalar/benchmark/applu/applu.in > applu.out 2> applu.err"
	elif benchmarks == 2 :
		ben = "./simplescalar/benchmark/equake/equake00.peak.ev6 < ./simplescalar/benchmark/equake/inp.in > equake.out 2> equake.err"
	elif benchmarks == 3 :
		ben = "./simplescalar/benchmark/gcc/gcc00.peak.ev6 ./simplescalar/benchmark/gcc/cp-decl.i -o cp.decl.s > gcc.out 2> gcc.err"
	elif benchmarks == 4 :
		ben = "./simplescalar/benchmark/gzip/gzip00.peak.ev6 ./simplescalar/benchmark/gzip/input.combined 60> gzip.out 2> gzip.err"
	elif benchmarks == 5 :
		ben = "./simplescalar/benchmark/mcf/mcf00.peak.ev6 ./simplescalar/benchmark/mcf/inp.in > mcf.out 2> mcf.err"
	elif benchmarks == 6 :
		ben = "./simplescalar/benchmark/wupwise/wupwise.peak.ev6 > wupwise.out 2> wupwise.err"
	else :
		ben = ""

	now = datetime.datetime.now()
	date_str = now.strftime("%Y%m%d")
	time_str = now.strftime("%H%M")
	file_name = f"./data/test_{date_str}_{time_str}.txt"
	rdir = f"-redir:sim {file_name}"

	caches = " \\\n".join(cache) + " \\\n"

	order = f"{sim} \\\n {rdir} \\\n -max:inst {max_inst} \\\n {caches} {ben}"
	return (order, file_name)

# Docker check
def server_check() :
	try :
		response = requests.get('http://localhost:5000')
		if response.status_code == 200:
			print('Server is running')
			return True
		else:
			print(f'Server is not running: {response.status_code}')
			return False
	except requests.exceptions.RequestsException as e :
		print(f"Server is not running: {e}")
		return False

def send_to_server(command):
	clear_terminal()

	try:
		url = "http://localhost:5000/exec"
		headers = {'Content-Type': 'application/json'}
		payload = {"command": command}

		print('''
******************************
***** Server is Running ******
******************************\n
''')
		print(f"Command sent to server: {command}")

		response = requests.post(url, json=payload, headers=headers)

		if response.status_code == 200:
			result = response.json()
			print("\nExecution Result:")
			if result.get('return_code') == 1 :
				print("Execution error. please check your inputs")
			else :
				print("Execution success")
		else:
			print(f"Server error: {response.status_code}")
			print(response.json())
	except requests.exceptions.RequestException as e:
		print(f"Failed to send command to server: {e}")

def main() :
	clear_terminal()
	print('''
21911722 Hyeondong Lee
Simplescalar Tester
Before run, please check docker container is running.
press enter key to continue...
''')
	input()

	if not server_check() :
		print('be sure to run docker container')
		sys.exit(1)

	while True :
		print_sim_menu()
		selection = input('Select Simulation: ')
		print_ben_menu()
		benchmarks = input('Select Benchmark: ')
		clear_terminal()
		max_inst = input('Input max instructions: ')
		cache = print_cache_menu()
		if not selection.isdigit() or not benchmarks.isdigit() :
			print('Invalid input')
			continue
		selection = int(selection)
		benchmarks = int(benchmarks)

		clear_terminal()
		print(f'''
Your selection is
Simulation: {ret_sim_order(selection)}
Benchmark: {ret_ben_order(benchmarks)}
Max Instructions: {max_inst}
Cache: {cache}
Right? (y/n)
''')
		confirm = input()
		if confirm == 'n' :
			continue
		order = get_order(selection, benchmarks, max_inst, cache)

		send_to_server(order[0])
		print(f'''
file saved in {order[1]}

continue? (y/n)
''')
		confirm = input()
		if confirm == 'n' :
			break


if __name__ == "__main__" :
	main()