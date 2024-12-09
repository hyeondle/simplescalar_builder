#!/bin/bash

# Simplescalar benchmark execution script

# Define benchmark list
BENCHMARKS=(
  "applu/applu00.peak.ev6 < ./simplescalar/benchmark/applu/applu.in > applu.out 2> applu.err"
  "equake/equake00.peak.ev6 < ./simplescalar/benchmark/equake/inp.in > equake.out 2> equake.err"
  "gcc/gcc00.peak.ev6 ./simplescalar/benchmark/gcc/cp-decl.i -o cp.decl.s > gcc.out 2> gcc.err"
  "gzip/gzip00.peak.ev6 ./simplescalar/benchmark/gzip/input.combined 60> gzip.out 2> gzip.err"
  "mcf/mcf00.peak.ev6 ./simplescalar/benchmark/mcf/inp.in > mcf.out 2> mcf.err"
  "wupwise/wupwise.peak.ev6 > wupwise.out 2> wupwise.err"
)

# Define cache and TLB settings for 30 tests
CACHES=(
  "-cache:dl1 dl1:128:32:1:l -cache:dl2 dl2:1024:64:4:l -cache:il1 il1:128:32:1:l -cache:il2 il2:1024:64:4:l -tlb:dtlb dtlb:16:8:4:l -tlb:itlb itlb:16:8:4:l"
  "-cache:dl1 dl1:1:32:128:l -cache:dl2 dl2:1024:64:4:l -cache:il1 il1:128:32:1:l -cache:il2 il2:1024:64:4:l -tlb:dtlb dtlb:16:8:4:l -tlb:itlb itlb:16:8:4:l"
  "-cache:dl1 dl1:128:32:1:l -cache:dl2 dl2:1024:64:4:l -cache:il1 il1:128:32:4:l -cache:il2 il2:1024:64:4:l -tlb:dtlb dtlb:16:8:4:l -tlb:itlb itlb:16:8:4:l"
  "-cache:dl1 dl1:128:64:1:l -cache:dl2 dl2:1024:128:4:l -cache:il1 il1:128:32:1:l -cache:il2 il2:1024:64:4:l -tlb:dtlb dtlb:16:8:4:l -tlb:itlb itlb:16:8:4:l"
  "-cache:dl1 dl1:128:32:1:l -cache:dl2 none -cache:il1 il1:128:32:1:l -cache:il2 none -tlb:dtlb dtlb:16:8:4:l -tlb:itlb itlb:16:8:4:l"
  "-cache:dl1 dl1:64:32:1:l -cache:dl2 dl2:512:64:4:l -cache:il1 il1:64:32:1:l -cache:il2 il2:512:64:4:l -tlb:dtlb dtlb:16:8:4:l -tlb:itlb itlb:16:8:4:l"
  "-cache:dl1 dl1:256:32:1:l -cache:dl2 dl2:2048:64:8:l -cache:il1 il1:256:32:1:l -cache:il2 il2:2048:64:8:l -tlb:dtlb dtlb:16:8:4:l -tlb:itlb itlb:16:8:4:l"
  "-cache:dl1 dl1:256:64:4:l -cache:dl2 dl2:2048:128:8:l -cache:il1 il1:256:64:4:l -cache:il2 il2:2048:128:8:l -tlb:dtlb dtlb:32:8:4:l -tlb:itlb itlb:32:8:4:l"
  "-cache:dl1 dl1:128:32:1:r -cache:dl2 dl2:1024:64:4:l -cache:il1 il1:128:32:1:l -cache:il2 il2:1024:64:4:l -tlb:dtlb dtlb:16:8:4:l -tlb:itlb itlb:16:8:4:l"
  "-cache:dl1 dl1:128:32:4:l -cache:dl2 dl2:1024:64:4:l -cache:il1 il1:128:32:4:l -cache:il2 il2:1024:64:4:l -tlb:dtlb dtlb:16:8:4:l -tlb:itlb itlb:16:8:4:l"
  "-cache:dl1 none -cache:dl2 none -cache:il1 il1:128:32:1:l -cache:il2 il2:1024:64:4:l -tlb:dtlb none -tlb:itlb itlb:16:8:4:l"
  "-cache:dl1 dl1:128:32:1:l -cache:dl2 dl2:1024:64:4:l -cache:il1 none -cache:il2 none -tlb:dtlb dtlb:16:8:4:l -tlb:itlb none"
  "-cache:dl1 dl1:128:32:4:l -cache:dl2 dl2:1024:64:8:l -cache:il1 il1:128:32:1:l -cache:il2 none -tlb:dtlb dtlb:32:8:4:l -tlb:itlb none"
  "-cache:dl1 none -cache:dl2 dl2:2048:128:8:l -cache:il1 il1:128:64:4:l -cache:il2 il2:2048:128:8:l -tlb:dtlb dtlb:16:8:4:l -tlb:itlb itlb:16:8:4:l"
  "-cache:dl1 dl1:128:64:4:l -cache:dl2 dl2:2048:128:8:l -cache:il1 none -cache:il2 il2:1024:64:4:l -tlb:dtlb none -tlb:itlb itlb:16:8:4:l"
  "-cache:dl1 dl1:128:32:1:l -cache:dl2 dl2:1024:64:4:l -cache:il1 il1:128:32:1:l -cache:il2 none -tlb:dtlb dtlb:16:8:4:l -tlb:itlb none"
  "-cache:dl1 none -cache:dl2 dl2:1024:64:4:l -cache:il1 none -cache:il2 il2:1024:64:4:l -tlb:dtlb none -tlb:itlb itlb:16:8:4:l"
  "-cache:dl1 dl1:256:64:4:l -cache:dl2 dl2:1024:128:4:l -cache:il1 il1:128:32:1:l -cache:il2 il2:512:64:4:l -tlb:dtlb dtlb:32:8:4:l -tlb:itlb itlb:16:8:4:l"
  "-cache:dl1 dl1:128:32:1:l -cache:dl2 dl2:1024:64:4:l -cache:il1 il1:128:32:1:l -cache:il2 il2:1024:64:4:l -tlb:dtlb dtlb:16:8:4:l -tlb:itlb none"
  "-cache:dl1 none -cache:dl2 none -cache:il1 il1:128:32:4:l -cache:il2 il2:1024:64:4:l -tlb:dtlb dtlb:16:8:4:l -tlb:itlb itlb:32:8:4:l"
  "-cache:dl1 dl1:128:64:1:l -cache:dl2 dl2:1024:128:4:l -cache:il1 none -cache:il2 il2:1024:128:4:l -tlb:dtlb none -tlb:itlb itlb:16:8:4:l"
  "-cache:dl1 dl1:64:32:1:l -cache:dl2 none -cache:il1 il1:64:32:1:l -cache:il2 il2:512:64:4:l -tlb:dtlb none -tlb:itlb itlb:16:8:4:l"
  "-cache:dl1 dl1:64:64:1:l -cache:dl2 none -cache:il1 il1:128:32:1:l -cache:il2 none -tlb:dtlb dtlb:16:8:4:l -tlb:itlb none"
  "-cache:dl1 dl1:128:32:4:l -cache:dl2 dl2:1024:64:8:l -cache:il1 none -cache:il2 none -tlb:dtlb dtlb:32:8:4:l -tlb:itlb none"
  "-cache:dl1 dl1:256:64:4:l -cache:dl2 dl2:2048:128:8:l -cache:il1 none -cache:il2 il2:2048:128:8:l -tlb:dtlb dtlb:32:8:4:l -tlb:itlb itlb:16:8:4:l"
  "-cache:dl1 dl1:128:32:1:l -cache:dl2 none -cache:il1 il1:128:32:1:l -cache:il2 il2:1024:64:4:l -tlb:dtlb none -tlb:itlb itlb:16:8:4:l"
  "-cache:dl1 none -cache:dl2 dl2:2048:128:8:l -cache:il1 il1:256:64:4:l -cache:il2 il2:2048:128:8:l -tlb:dtlb dtlb:16:8:4:l -tlb:itlb none"
  "-cache:dl1 dl1:128:64:4:l -cache:dl2 dl2:2048:128:8:l -cache:il1 none -cache:il2 none -tlb:dtlb dtlb:32:8:4:l -tlb:itlb itlb:32:8:4:l"
  "-cache:dl1 dl1:128:32:1:r -cache:dl2 dl2:1024:64:4:l -cache:il1 none -cache:il2 none -tlb:dtlb dtlb:16:8:4:l -tlb:itlb itlb:16:8:4:l"
)

# Loop through tests
for TEST_NUM in $(seq 1 30); do
  echo "Running Test #${TEST_NUM}..."

  # Get cache settings
  CACHE_SETTINGS=${CACHES[$((TEST_NUM - 1))]}

  # Run each benchmark for the test
  for BENCH in "${BENCHMARKS[@]}"; do
    BENCH_NAME=$(echo $BENCH | cut -d '/' -f1)
    OUTPUT_FILE="./data/test_${TEST_NUM}_${BENCH_NAME}.txt"

    # Execute the simulation
    ./simplescalar/simplesim-3.0/sim-cache \
      -redir:sim $OUTPUT_FILE \
      -max:inst 1000000000 \
      $CACHE_SETTINGS \
      ./simplescalar/benchmark/$BENCH

    echo "Test #${TEST_NUM} for ${BENCH_NAME} completed."
  done

done

echo "All tests completed."
