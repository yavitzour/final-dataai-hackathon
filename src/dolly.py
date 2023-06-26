'''
pip install accelerate
'''

from transformers import pipeline
import torch

def main():
    #instruct_pipeline = pipeline(model="databricks/dolly-v2-12b", torch_dtype=torch.bfloat16, trust_remote_code=True, device_map="auto")
    instruct_pipeline = pipeline(model="databricks/dolly-v2-3b",
                                 torch_dtype=torch.bfloat16,
                                 trust_remote_code=True,
                                 device_map="auto")
    res = instruct_pipeline("Explain to me the difference between nuclear fission and fusion.")
    print(res[0])
    pass

if __name__ == '__main__':
    main()