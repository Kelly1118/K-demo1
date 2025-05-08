import torch
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer

# 自定义数据集类
class TextDataset(Dataset):
    def __init__(self, file_path, tokenizer, max_length):
        with open(file_path, 'r', encoding='utf-8') as f:
            self.texts = f.readlines()
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
    # 加载预训练的tokenizer和模型
    model_name = "deepseek-ai/deepseek-coder-7b-instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    # 创建数据集和数据加载器
    dataset = TextDataset('preprocessed_data.txt', tokenizer, max_length=512)

    # 训练参数设置
    training_args = TrainingArguments(
        output_dir='./results',
        num_train_epochs=3,
        per_device_train_batch_size=4,
        save_steps=10_000,
        save_total_limit=2,
        prediction_loss_only=True,
    )

    # 创建Trainer对象
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
    )

    # 开始训练
    trainer.train()

    # 保存训练好的模型
    trainer.save_model('./fine_tuned_model')