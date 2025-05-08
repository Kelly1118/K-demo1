from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# 加载训练好的模型和分词器
model_path = './fine_tuned_model'
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

# 准备输入文本，这里是一个 SQL 查询需求
input_text = "请写出一个查询语句，显示所有薪水超过 10000 的雇员的名字和薪水。"
input_ids = tokenizer.encode(input_text, return_tensors='pt')

# 生成文本
output = model.generate(input_ids, max_length=100, num_return_sequences=1)
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

# 打印生成的文本
print("生成的文本:")
print(generated_text)
