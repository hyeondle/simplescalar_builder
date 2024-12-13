import os
import subprocess

# Define benchmark list
BENCHMARKS = [
	"applu/applu00.peak.ev6 < ./simplescalar/benchmark/applu/applu.in > applu.out 2> applu.err",
	"equake/equake00.peak.ev6 < ./simplescalar/benchmark/equake/inp.in > equake.out 2> equake.err",
	"gcc/gcc00.peak.ev6 ./simplescalar/benchmark/gcc/cp-decl.i -o cp.decl.s > gcc.out 2> gcc.err",
	"gzip/gzip00.peak.ev6 ./simplescalar/benchmark/gzip/input.combined > gzip.out 2> gzip.err",
	"mcf/mcf00.peak.ev6 ./simplescalar/benchmark/mcf/inp.in > mcf.out 2> mcf.err",
	"wupwise/wupwise.peak.ev6 > wupwise.out 2> wupwise.err"
]

# Define cache and TLB settings for 30 tests
CACHES = [
	"-cache:dl1 dl1:128:32:1:l -cache:dl2 dl2:1024:64:4:l -cache:il1 il1:128:32:1:l -cache:il2 il2:1024:64:4:l -tlb:dtlb dtlb:16:8:4:l -tlb:itlb itlb:16:8:4:l",
	"-cache:dl1 dl1:1:32:128:l -cache:dl2 dl2:1024:64:4:l -cache:il1 il1:128:32:1:l -cache:il2 il2:1024:64:4:l -tlb:dtlb dtlb:16:8:4:l -tlb:itlb itlb:16:8:4:l",
	"-cache:dl1 dl1:128:32:1:l -cache:dl2 dl2:1024:64:4:l -cache:il1 il1:128:32:4:l -cache:il2 il2:1024:64:4:l -tlb:dtlb dtlb:16:8:4:l -tlb:itlb itlb:16:8:4:l",
	"-cache:dl1 dl1:128:64:1:l -cache:dl2 dl2:1024:128:4:l -cache:il1 il1:128:32:1:l -cache:il2 il2:1024:64:4:l -tlb:dtlb dtlb:16:8:4:l -tlb:itlb itlb:16:8:4:l",
	"-cache:dl1 dl1:128:32:1:l -cache:dl2 none -cache:il1 il1:128:32:1:l -cache:il2 none -tlb:dtlb dtlb:16:8:4:l -tlb:itlb itlb:16:8:4:l",
	"-cache:dl1 dl1:128:32:1:l -cache:dl2 dl2:1024:64:4:l -cache:il1 il1:128:32:1:l -cache:il2 il2:1024:64:4:l -tlb:dtlb dtlb:16:8:4:l -tlb:itlb itlb:16:8:4:l",
	"-cache:dl1 dl1:64:32:1:l -cache:dl2 dl2:512:64:4:l -cache:il1 il1:64:32:1:l -cache:il2 il2:512:64:4:l -tlb:dtlb dtlb:16:8:4:l -tlb:itlb itlb:16:8:4:l",
	"-cache:dl1 dl1:256:32:1:l -cache:dl2 dl2:2048:64:8:l -cache:il1 il1:256:32:1:l -cache:il2 il2:2048:64:8:l -tlb:dtlb dtlb:16:8:4:l -tlb:itlb itlb:16:8:4:l",
	"-cache:dl1 dl1:256:64:4:l -cache:dl2 dl2:2048:128:8:l -cache:il1 il1:256:64:4:l -cache:il2 il2:2048:128:8:l -tlb:dtlb dtlb:32:8:4:l -tlb:itlb itlb:32:8:4:l",
	"-cache:dl1 dl1:128:32:1:r -cache:dl2 dl2:1024:64:4:l -cache:il1 il1:128:32:1:l -cache:il2 il2:1024:64:4:l -tlb:dtlb dtlb:16:8:4:l -tlb:itlb itlb:16:8:4:l",
	"-cache:dl1 dl1:128:32:1:l -cache:dl2 none -cache:il1 none -cache:il2 none -tlb:dtlb dtlb:16:8:4:l -tlb:itlb none",
	"-cache:dl1 none -cache:dl2 none -cache:il1 il1:128:32:1:l -cache:il2 none -tlb:dtlb none -tlb:itlb itlb:16:8:4:l",
	"-cache:dl1 dl1:256:64:4:l -cache:dl2 none -cache:il1 none -cache:il2 none -tlb:dtlb dtlb:16:8:4:l -tlb:itlb none",
	"-cache:dl1 none -cache:dl2 none -cache:il1 il1:256:64:4:l -cache:il2 none -tlb:dtlb none -tlb:itlb itlb:16:8:4:l",
	"-cache:dl1 dl1:128:32:1:r -cache:dl2 none -cache:il1 none -cache:il2 none -tlb:dtlb dtlb:16:8:4:l -tlb:itlb none",
	"-cache:dl1 none -cache:dl2 none -cache:il1 none -cache:il2 none -tlb:dtlb none -tlb:itlb none",
	"-cache:dl1 none -cache:dl2 dl2:1024:64:4:l -cache:il1 none -cache:il2 il2:1024:64:4:l -tlb:dtlb dtlb:16:8:4:l -tlb:itlb itlb:16:8:4:l",
	"-cache:dl1 dl1:128:32:1:l -cache:dl2 dl2:1024:64:4:l -cache:il1 il1:128:32:1:l -cache:il2 il2:1024:64:4:l -tlb:dtlb dtlb:16:8:4:l -tlb:itlb itlb:16:8:4:l",
	"-cache:dl1 dl1:128:32:1:l -cache:dl2 dl2:1024:64:4:l -cache:il1 il1:128:32:1:l -cache:il2 il2:1024:64:4:l -tlb:dtlb dtlb:16:8:4:l -tlb:itlb itlb:16:8:4:l",
	"-cache:dl1 none -cache:dl2 none -cache:il1 none -cache:il2 none -tlb:dtlb dtlb:32:8:4:l -tlb:itlb itlb:32:8:4:l",
	"-cache:dl1 dl1:128:32:1:l -cache:dl2 dl2:1024:64:4:l -cache:il1 il1:128:32:1:l -cache:il2 il2:1024:64:4:l -tlb:dtlb dtlb:16:8:4:l -tlb:itlb itlb:16:8:4:l",
	"-cache:dl1 dl1:128:32:1:l -cache:dl2 dl2:1024:64:4:l -cache:il1 il1:128:32:1:l -cache:il2 il2:1024:64:4:l -tlb:dtlb dtlb:16:8:4:l -tlb:itlb itlb:16:8:4:l",
	"-cache:dl1 dl1:128:32:1:l -cache:dl2 dl2:1024:64:4:l -cache:il1 il1:128:32:1:l -cache:il2 il2:1024:64:4:l -tlb:dtlb dtlb:16:8:4:l -tlb:itlb itlb:16:8:4:l",
	"-cache:dl1 dl1:128:32:1:l -cache:dl2 dl2:1024:64:4:l -cache:il1 il1:128:32:1:l -cache:il2 il2:1024:64:4:l -victim:victim:16:32:4:l -tlb:dtlb dtlb:16:8:4:l -tlb:itlb itlb:16:8:4:l",
	"-cache:dl1 dl1:128:32:1:l -cache:dl2 dl2:1024:64:4:l -cache:il1 il1:128:32:1:l -cache:il2 il2:1024:64:4:l -tlb:dtlb dtlb:16:8:4:l -tlb:itlb itlb:16:8:4:l",
	"-cache:dl1 dl1:128:32:1:l -cache:dl2 dl2:1024:64:4:l -cache:il1 il1:128:32:1:l -cache:il2 il2:1024:64:4:l -tlb:dtlb dtlb:16:8:4:l -tlb:itlb itlb:16:8:4:l",
	"-cache:dl1 dl1:128:32:2:l -cache:dl2 dl2:1024:64:8:l -cache:il1 il1:128:32:2:l -cache:il2 il2:1024:64:8:l -tlb:dtlb dtlb:16:8:4:l -tlb:itlb itlb:16:8:4:l",
	"-cache:dl1 dl1:128:32:1:l -cache:dl2 dl2:1024:64:4:l -cache:il1 il1:128:32:1:l -cache:il2 il2:1024:64:4:l -tlb:dtlb dtlb:16:8:4:l -tlb:itlb itlb:16:8:4:l",
	"-cache:dl1 dl1:256:64:4:l -cache:dl2 dl2:2048:128:8:l -cache:il1 il1:256:64:4:l -cache:il2 il2:2048:128:8:l -tlb:dtlb dtlb:32:8:4:l -tlb:itlb itlb:32:8:4:l",
	"-cache:dl1 dl1:128:32:1:l -cache:dl2 dl2:2048:64:8:l -cache:il1 il1:64:32:2:l -cache:il2 il2:1024:64:4:l -tlb:dtlb dtlb:16:4:4:l -tlb:itlb itlb:16:4:4:l"
]



def run_benchmark(test_num, benchmark, cache_settings):

	benchmarks = "./simplescalar/benchmark/"+benchmark
	benchmark_name = benchmark.split('/')[0]
	output_file = f"./data/test_{test_num}_{benchmark.split('/')[0]}.txt"

	# Construct the full command
	command = (
		f"./simplescalar/simplesim-3.0/sim-cache "
		f"-redir:sim {output_file} -max:inst 1000000000 {cache_settings} {benchmarks}"
	)

	print(f"Executing: {command}")

	try:
		result = subprocess.run(command, shell=True, text=True, capture_output=True)
		if result.returncode == 0:
			print(f"Test #{test_num} for {benchmark_name} completed successfully.")
		else:
			print(f"Error in Test #{test_num} for {benchmark_name}.")
			print(result.stderr)
			raise RuntimeError("Benchmark execution failed.")
	except Exception as e:
		print(f"An error occurred: {e}")
		raise

def main():
	for test_num, cache_settings in enumerate(CACHES, start=1):
		print(f"Running Test #{test_num}...")
		for benchmark in BENCHMARKS:
			try:
				run_benchmark(test_num, benchmark, cache_settings)
			except RuntimeError:
				print(f"Skipping remaining benchmarks for Test #{test_num} due to an error.")
				break

if __name__ == "__main__":
	main()