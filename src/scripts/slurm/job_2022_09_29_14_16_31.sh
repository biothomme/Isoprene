#!/bin/bash
#SBATCH -A snic2022-22-608
#SBATCH -M rackham
#SBATCH -p core
#SBATCH -n 2
#SBATCH -t 1-00:00:00
#SBATCH --mail-user thomasmarkus.huber.3696@student.uu.se
#SBATCH --mail-type=FAIL
#SBATCH -J job_2022_09_29_14_16_31
#SBATCH -o /crex/proj/snic2022-23-321/private/thomas/cache/00_slurmlog/slurm-%A.out
#SBATCH -e /crex/proj/snic2022-23-321/private/thomas/cache/00_slurmlog/slurm-%A.err
# modules


# commands
python /crex/proj/snic2022-23-321/private/thomas/src/scripts/python/01_get_era5.py