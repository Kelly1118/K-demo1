import torch
import os
import json
import time
from torch.utils.data import Dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer


# 自定义数据集类
class TextDataset(Dataset):
    def __init__(self, file_path, tokenizer, max_length):
        start_time = time.time()
        with open(file_path, 'r', encoding='utf-8') as f:
            self.texts = f.readlines()
        end_time = time.time()
        print(f"数据加载耗时: {end_time - start_time} 秒")
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        encoding = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        input_ids = encoding['input_ids'].flatten()
        attention_mask = encoding['attention_mask'].flatten()
        return {
            'input_ids': input_ids,
            'attention_mask': attention_mask,
            'labels': input_ids.clone()
        }


if __name__ == "__main__":
    # 本地模型路径
    local_model_path = r"D:\app\Ollama\deepseek-r1-1.5b"
    config_path = f"{local_model_path}/config.json"
    tokenizer_path = f"{local_model_path}/tokenizer.json"

    try:
        # 检查配置文件是否存在
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"未找到 {config_path} 文件，请检查模型路径是否正确。")
        # 检查配置文件内容
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            if 'model_type' not in config:
                raise ValueError(f"{config_path} 文件中缺少 'model_type' 字段，请检查文件内容。")

        # 检查分词器文件是否存在
        if not os.path.exists(tokenizer_path):
            raise FileNotFoundError(f"未找到 {tokenizer_path} 文件，请检查模型路径是否正确。")

        # 加载预训练的tokenizer和模型
        start_time = time.time()
        tokenizer = AutoTokenizer.from_pretrained(local_model_path)
        model = AutoModelForCausalLM.from_pretrained(
            local_model_path,
            torch_dtype=torch.float16,
            trust_remote_code=True  # 如果模型代码包含自定义部分，可能需要添加此参数
        )
        end_time = time.time()
        print(f"模型加载耗时: {end_time - start_time} 秒")

        # 训练参数设置
        training_args = TrainingArguments(
            output_dir='./results',
            num_train_epochs=3,
            per_device_train_batch_size=2,
            save_steps=10_000,
            save_total_limit=2,
            prediction_loss_only=True,
            gradient_accumulation_steps=2,
            logging_steps=100,  # 每 100 步记录一次日志
            warmup_steps=500,  # 热身步数
            weight_decay=0.01,  # 权重衰减
            fp16=False,  # CPU不支持混合精度训练，设置为False
            use_cpu=True  # 强制使用CPU
        )

        # 创建数据集
        dataset = TextDataset('preprocessed_data.txt', tokenizer, max_length=512)

        # 创建Trainer对象
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=dataset,
        )

        print("开始训练前的准备工作...")
        start_time = time.time()
        trainer.train()
        end_time = time.time()
        print(f"训练总耗时: {end_time - start_time} 秒")

        # 保存训练好的模型
        trainer.save_model('./fine_tuned_model')
    except (FileNotFoundError, ValueError, OSError) as e:
        print(f"加载模型时出现错误: {e}，请检查本地模型路径 {local_model_path} 是否正确。")