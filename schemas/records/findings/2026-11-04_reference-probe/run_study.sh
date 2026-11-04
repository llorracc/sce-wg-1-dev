#!/bin/bash
# The convergence study: four members at four settings, in parallel, two threads each. Logs with times stay here.
cd /home/shared/github/llorracc/sce-wg-1-dev || exit 1
S=/tmp/claude-1000/-home-shared-github-llorracc-sce-wg-1-dev/15be9292-911d-4711-9777-e339888ecb1c/scratchpad/reference
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 MKL_NUM_THREADS=2
declare -A SCN=([bst-p-zero-0.005]=natural [bst-p-zero-0.0005]=natural [bst-p-zero-0.00005]=natural [bst-restrained]=artificial)
declare -A SET=([A]="--points 1000 --top 200 --nodes 32" [B]="--points 2000 --top 400 --nodes 32" [C]="--points 2000 --top 400 --nodes 64" [D]="--points 4000 --top 1000 --nodes 64")
for mem in bst-p-zero-0.005 bst-p-zero-0.0005 bst-p-zero-0.00005 bst-restrained; do
  for s in A B C D; do
    out=$S/runs/$mem/$s; mkdir -p $out
    ( uv run --with numpy --with scipy --with jsonschema --with pyyaml --with referencing python $S/reference_probe.py \
        schemas/bst/${SCN[$mem]}/members/$mem.yaml --out $out ${SET[$s]} --tol 1e-11 --max-iter 3000 > $out/stdout.txt 2>&1;
      echo "exit $?" >> $out/stdout.txt ) &
  done
done
wait
echo "all runs finished at $(date '+%H:%M:%S %Z')"
