import os
from PIL import Image


def main():
    # 提示用户输入输入图像路径
    input_image_path = input("请输入输入图像的路径：")

    # 检查输入路径是否存在
    if not os.path.isfile(input_image_path):
        print("输入图像路径无效，请检查路径后重试。")
        return

    # 提示用户输入输出图像路径
    output_path = input("请输入输出图像的路径：")

    # 提示用户输入调整后的图像尺寸
    try:
        width = int(input("请输入调整大小后的图像宽度："))
        height = int(input("请输入调整大小后的图像高度："))
    except ValueError:
        print("无效的大小，请输入整数。")
        return

    try:
        # 打开输入图像
        with Image.open(input_image_path) as img:
            # 转换为灰度图像
            grayscale_img = img.convert("L")
            # 保存灰度图像
            grayscale_img.save(output_path)
            print(f"灰度图像已保存到：{output_path}")

            # 调整图像大小
            resized_img = grayscale_img.resize((width, height))
            # 保存调整大小后的图像
            resized_img.save(output_path)
            print(f"调整大小后的图像已保存到：{output_path}")

    except Exception as e:
        print(f"发生错误：{e}")


if __name__ == "__main__":
    main()