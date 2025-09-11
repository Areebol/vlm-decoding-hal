export CUDA_VISIBLE_DEVICES=0,1
# export HF_ENDPOINT=https://hf-mirror.com

## Generate the MLLM's responses and save them in a jsonl file:
# python chair_llava.py   --model-path "/U_20240603_ZSH_SMIL/LLM/llava-v1.5-7b" \
#                         --method typo-inject \
#                         --answers-file "./re_log/llava-1.5/typo-inject.jsonl" \
#                         --temperature 1.0
                        
## Calculate CHAIR using the generated jsonl file:
## command explanation:
# python chair.py --cap_file /path/to/jsonl --image_id_key image_id --caption_key caption --coco_path /path/to/COCO/annotations_trainval2014/annotations/ --save_path /path/to/save/jsonl
## example command:
# python chair.py --cap_file ./re_log/llava-1.5/regular.jsonl \
# python chair.py --cap_file ./re_log/llava-1.5/vcd.jsonl \
python chair.py --cap_file ./re_log/llava-1.5/typo-inject.jsonl \
                --image_id_key image_id \
                --caption_key caption \
                --coco_path /U_20240603_ZSH_SMIL/lzh/Data/coco/annotations_trainval2014/annotations/ \
                --save_path ./test/llava-1.5/typo-inject.jsonl
                # --save_path ./test/llava-1.5/regular.jsonl
                # --save_path ./test/llava-1.5/deco.jsonl
                # --save_path ./test/llava-1.5/regular.jsonl
                # --save_path ./test/llava-1.5/temp_chair.jsonl