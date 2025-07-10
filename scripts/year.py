import pandas as pd
import os
from datetime import datetime

def process_precipitation_data(input_file_path):
    """
    处理每日降水数据，计算并输出年平均降水数据
    
    参数:
    input_file_path: 输入CSV文件的完整路径
    """
    
    try:
        print("正在读取数据文件...")
        df = pd.read_csv(input_file_path)

        print(f"原始数据形状: {df.shape}")
        print(f"数据列名: {df.columns.tolist()}")
        print("\n前5行数据:")
        print(df.head())

        print("\n正在处理数据...")

        df['date'] = pd.to_datetime(df['date'])

        df['year'] = df['date'].dt.year

        print(f"数据年份范围: {df['year'].min()} - {df['year'].max()}")
        print(f"包含的省份数量: {df['province'].nunique()}")
        print(f"省份列表: {sorted(df['province'].unique())}")

        yearly_avg = df.groupby(['province', 'year'])['avg_precipitation'].mean().reset_index()
        yearly_avg.columns = ['province', 'year', 'annual_avg_precipitation']

        yearly_avg['annual_avg_precipitation'] = yearly_avg['annual_avg_precipitation'].round(2)

        yearly_avg = yearly_avg.sort_values(['province', 'year']).reset_index(drop=True)

        input_dir = os.path.dirname(input_file_path)
        output_file_path = os.path.join(input_dir, 'china_precipitation_province_annual_avg_2018_2024.csv')

        yearly_avg.to_csv(output_file_path, index=False, encoding='utf-8-sig')
        
        print(f"\n处理完成！")
        print(f"年平均降水数据已保存到: {output_file_path}")
        print(f"输出数据形状: {yearly_avg.shape}")

        print("\n年平均降水数据预览:")
        print(yearly_avg.head(10))

        print("\n各省份年平均降水统计:")
        summary_stats = yearly_avg.groupby('province')['annual_avg_precipitation'].agg(['mean', 'min', 'max', 'std']).round(2)
        summary_stats.columns = ['7年平均值', '最小年份', '最大年份', '标准差']
        print(summary_stats.head(10))
        
        return yearly_avg, output_file_path
        
    except FileNotFoundError:
        print(f"错误: 找不到文件 {input_file_path}")
        print("请检查文件路径是否正确")
        return None, None
        
    except Exception as e:
        print(f"处理数据时发生错误: {str(e)}")
        return None, None

def main():
    """主函数"""
    input_file = r"C:\Users\Shaira\Desktop\china_precipitation_province_daily_avg_2018_2024_simple.csv"
    
    print("=" * 60)
    print("中国省份降水数据年平均值计算程序")
    print("=" * 60)

    if not os.path.exists(input_file):
        print(f"错误: 文件不存在 - {input_file}")
        print("请确认文件路径是否正确")
        return

    result_df, output_path = process_precipitation_data(input_file)
    
    if result_df is not None:
        print("\n" + "=" * 60)
        print("程序执行成功！")
        print(f"原始数据: 每日降水数据")
        print(f"输出数据: 年平均降水数据")
        print(f"输출文件: {output_path}")
        print("=" * 60)
    else:
        print("程序执行失败，请检查错误信息")

if __name__ == "__main__":
    main()