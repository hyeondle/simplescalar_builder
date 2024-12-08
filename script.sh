#!/bin/bash

input_file="$1"

if [[ -z "$input_file" ]]; then
    echo "Usage: $0 <input_file>"
    exit 1
fi

if [[ ! -f "$input_file" ]]; then
    echo "Error: File '$input_file' not found!"
    exit 1
fi

output_file="${input_file%.*}.csv"

awk '/sim: \*\* simulation statistics \*\*/ {flag=1; next} flag {
    split($0, parts, "#");
    desc = (length(parts) > 1 ? parts[2] : "");
    split(parts[1], main_parts, " ");
    name = main_parts[1];
    num = main_parts[2];
    gsub(/^ +| +$/, "", desc); # 설명의 앞뒤 공백 제거
    gsub(/,/, ".", desc);      # ','를 '.'로 대체
    print name "," num "," desc;
}' "$input_file" > "$output_file"

echo "Processed text saved to $output_file"
