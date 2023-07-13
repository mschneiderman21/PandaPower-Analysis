import simbench as sb

file = f"Bench_Codes.txt"
with open(file, "w") as file:
    file.write(str(sb.collect_all_simbench_codes()))