import pandas as pd
import numpy as np
from datetime import datetime
import os

station_to_province = {
    # 香港特别行政区
    "KING'S PARK": "香港",
    "HONG KONG OBSERVATORY": "香港",
    
    # 内蒙古自治区
    "HUMA": "内蒙古",
    "TULIHE": "内蒙古", 
    "HAILAR": "内蒙古",
    "ERENHOT": "内蒙古",
    "ABAG QI": "内蒙古",
    "HAILS": "内蒙古",
    "JURH": "内蒙古",
    "HALIUT": "内蒙古",
    "BAILING-MIAO": "内蒙古",
    "HUADE": "内蒙古",
    "HOHHOT": "内蒙古",
    "JARTAI": "内蒙古",
    "OTOG QI": "内蒙古",
    "XI UJIMQIN QI": "内蒙古",
    "JARUD QI": "内蒙古",
    "LINDONG": "内蒙古",
    "XILIN HOT": "内蒙古",
    "LINXI": "内蒙古",
    "TONGLIAO": "内蒙古",
    "DUOLUN": "内蒙古",
    "CHIFENG": "内蒙古",
    
    # 黑龙江省
    "NENJIANG": "黑龙江",
    "SUNWU": "黑龙江",
    "BUGT": "黑龙江",
    "KESHAN": "黑龙江",
    "QIQIHAR": "黑龙江",
    "HAILUN": "黑龙江",
    "FUJIN": "黑龙江",
    "ANDA": "黑龙江",
    "HARBIN": "黑龙江",
    "TONGHE": "黑龙江",
    "SHANGZHI": "黑龙江",
    "JIXI": "黑龙江",
    "MUDANJIANG": "黑龙江",
    "SUIFENHE": "黑龙江",
    
    # 吉林省
    "QIAN GORLOS": "吉林",
    "SIPING": "吉林",
    "CHANGCHUN": "吉林",
    "YANJI": "吉林",
    "LINJIANG": "吉林",
    
    # 辽宁省
    "ZHANGWU": "辽宁",
    "CHAOYANG": "辽宁",
    "JINZHOU": "辽宁",
    "SHENYANG": "辽宁",
    "BENXI": "辽宁",
    "YINGKOU": "辽宁",
    "DANDONG": "辽宁",
    "DALIAN": "辽宁",
    
    # 新疆维吾尔自治区
    "ULIASTAI": "新疆",
    "ALTAY": "新疆",
    "FUYUN": "新疆",
    "HOBOKSAR": "新疆",
    "KARAMAY": "新疆",
    "JINGHE": "新疆",
    "QITAI": "新疆",
    "YINING": "新疆",
    "WU LU MU QI": "新疆",
    "TURPAN": "新疆",
    "KUQA": "新疆",
    "KORLA": "新疆",
    "KASHI": "新疆",
    "BACHU": "新疆",
    "TAZHONG": "新疆",
    "TIKANLIK": "新疆",
    "RUOQIANG": "新疆",
    "SHACHE": "新疆",
    "HOTAN": "新疆",
    "QIEMO/QARQAN": "新疆",
    "HAMI": "新疆",
    
    # 甘肃省
    "EJIN QI": "甘肃",
    "MAZONG SHAN": "甘肃",
    "DUNHUANG": "甘肃",
    "YUMENZHEN": "甘肃",
    "JIUQUAN": "甘肃",
    "MINQIN": "甘肃",
    "WUSHAOLING": "甘肃",
    "LANZHOU": "甘肃",
    "YU ZHONG": "甘肃",
    "TIANSHUI": "甘肃",
    "HEZUO": "甘肃",
    "WUDU": "甘肃",
    "PINGLIANG": "甘肃",
    
    # 青海省
    "BAYAN MOD": "青海",
    "LENGHU": "青海",
    "DA-QAIDAM": "青海",
    "GANGCA": "青海",
    "GOLMUD": "青海",
    "DULAN": "青海",
    "XINING": "青海",
    "GUINAN": "青海",
    "TONGDE": "青海",
    "TUOTUOHE": "青海",
    "QUMARLEB": "青海",
    "YUSHU": "青海",
    "MADOI": "青海",
    "DARLAG": "青海",
    
    # 宁夏回族自治区
    "YINCHUAN": "宁夏",
    "YANCHI": "宁夏",
    
    # 陕西省
    "YULIN": "陕西",
    "YAN AN": "陕西",
    "BEIDAO": "陕西",
    "XIAN": "陕西",
    "HANZHONG": "陕西",
    
    # 山西省
    "DATONG": "山西",
    "YUANPING": "山西",
    "TAIYUAN": "山西",
    "JIEXIU": "山西",
    "YUNCHENG": "山西",
    
    # 河北省
    "SHIJIAZHUANG": "河北",
    "HUAILAI": "河北",
    "CHENGDE": "河北",
    "CAOHEKOU": "河北",
    "LETING": "河北",
    "CANGZHOU": "河北",
    "POTOU": "河北",
    
    # 北京市
    "BEIJING": "北京",
    
    # 天津市
    "TIANJIN": "天津",
    
    # 山东省
    "HUIMIN": "山东",
    "CHENGSHANTOU": "山东",
    "JINAN": "山东",
    "WEIFANG": "山东",
    "QINGDAO": "山东",
    "HEZE/CAOZHOU": "山东",
    "DINGTAO": "山东",
    "YANZHOU": "山东",
    
    # 河南省
    "ANYANG": "河南",
    "LUSHI": "河南",
    "ZHENGZHOU": "河南",
    "ZHUMADIAN": "河南",
    "XINYANG": "河南",
    
    # 西藏自治区
    "SHIQUANHE": "西藏",
    "BAINGOIN": "西藏",
    "NAGQU": "西藏",
    "XAINZA": "西藏",
    "XIGAZE": "西藏",
    "LHASA": "西藏",
    "SOG XIAN": "西藏",
    "DENGQEN": "西藏",
    "QAMDO": "西藏",
    
    # 四川省
    "RUO'ERGAI": "四川",
    "GARZE": "四川",
    "BARKAM": "四川",
    "SONGPAN": "四川",
    "WENJIANG": "四川",
    "LITANG": "四川",
    "CHENGDU": "四川",
    "JIULONG": "四川",
    "YIBIN": "四川",
    "XICHANG": "四川",
    "NANCHONG": "四川",
    "CHONG-QING": "四川",
    "CHONGQING": "四川",
    "WANYUAN": "四川",
    
    # 云南省
    "DEQEN": "云南",
    "HUILI": "云南",
    "TENGCHONG": "云南",
    "CHUXIONG": "云南",
    "KUNMING": "云南",
    "LINCANG": "云南",
    "LANCANG": "云南",
    "SIMAO": "云南",
    "MENGZI": "云南",
    "LIJING": "云南",
    
    # 湖北省
    "GUANGHUA": "湖北",
    "ENSHI": "湖北",
    "YICHANG": "湖北",
    "WUHAN": "湖北",
    
    # 湖南省
    "YOUYANG": "湖南",
    "CHANGDE": "湖南",
    "CHANGSHA": "湖南",
    "LINGLING": "湖南",
    "ZHIJIANG": "湖南",
    
    # 贵州省
    "BIJIE": "贵州",
    "ZUNYI": "贵州",
    "GUIYANG": "贵州",
    "XINGREN": "贵州",
    
    # 江西省
    "JIAN": "江西",
    "GANZHOU": "江西",
    "JINGDEZHEN": "江西",
    "NANCHANG": "江西",
    "NANCHENG": "江西",
    
    # 安徽省
    "BOXIAN": "安徽",
    "BENGBU": "安徽",
    "HUOSHAN": "安徽",
    "HEFEI": "安徽",
    "ANQING": "安徽",
    
    # 江苏省
    "XUZHOU": "江苏",
    "GANYU": "江苏",
    "NANJING": "江苏",
    "DONGTAI": "江苏",
    
    # 上海市
    "SHANGHAI": "上海",
    "SHANGHAI/HONGQIAO": "上海",
    
    # 浙江省
    "HANGZHOU": "浙江",
    "DINGHAI": "浙江",
    "QU XIAN": "浙江",
    "WENZHOU": "浙江",
    "DACHEN DAO": "浙江",
    "RUIAN": "浙江",
    
    # 福建省
    "NANPING": "福建",
    "FUZHOU": "福建",
    "YONGAN": "福建",
    "XIAMEN": "福建",
    
    # 广西壮族自治区
    "GUILIN": "广西",
    "HECHI": "广西",
    "BAISE": "广西",
    "GUIPING": "广西",
    "WUZHOU": "广西",
    "LONGZHOU": "广西",
    "NANNING": "广西",
    "QINZHOU": "广西",
    
    # 广东省
    "SHAOGUAN": "广东",
    "GUANGZHOU": "广东",
    "HEYUAN": "广东",
    "SHANTOU": "广东",
    "SHANWEI": "广东",
    "YANGJIANG": "广东",
    
    # 海南省
    "HAIKOU": "海南",
    "DONGFANG": "海南",
    "QIONGHAI": "海南",
    "SANYA": "海南",
    "XISHA DAO": "海南",
    
    # 台湾省（部分站点）
    "HUNG CHIA": "台湾",
    "TSINGTAO": "台湾",
    
    # 内蒙古自治区（重新分类）
    "ARXAN": "内蒙古",  # 阿尔山市，位于内蒙古
}

def process_precipitation_data(input_file, output_file=None):
    """
    处理中国降水数据，按省份计算每日平均降水量
    
    Parameters:
    input_file (str): 输入CSV文件路径
    output_file (str): 输出CSV文件路径，如果为None则自动生成
    
    Returns:
    pd.DataFrame: 处理后的省份每日平均降水数据
    """
    
    print(f"开始处理数据文件: {input_file}")

    if not os.path.exists(input_file):
        raise FileNotFoundError(f"找不到文件: {input_file}")

    try:
        print("正在读取原始数据...")
        df = pd.read_csv(input_file, encoding='utf-8')
        print(f"成功读取数据，共 {len(df)} 行记录")
    except Exception as e:
        print(f"读取文件时出错: {e}")
        try:
            df = pd.read_csv(input_file, encoding='gbk')
            print(f"使用GBK编码成功读取数据，共 {len(df)} 行记录")
        except Exception as e2:
            raise Exception(f"无法读取文件，尝试UTF-8和GBK编码都失败: {e2}")

    print(f"数据列名: {list(df.columns)}")
    print(f"数据前5行:")
    print(df.head())

    print("\n开始数据预处理...")

    initial_rows = len(df)
    df = df.dropna()
    print(f"删除缺失值后，剩余 {len(df)} 行记录 (删除了 {initial_rows - len(df)} 行)")

    try:
        df['date'] = pd.to_datetime(df['date'])
        print("日期格式转换成功")
    except Exception as e:
        print(f"日期格式转换失败: {e}")
        print("尝试常见的日期格式...")
        for date_format in ['%Y-%m-%d', '%Y/%m/%d', '%d-%m-%Y', '%d/%m/%Y']:
            try:
                df['date'] = pd.to_datetime(df['date'], format=date_format)
                print(f"使用格式 {date_format} 转换成功")
                break
            except:
                continue
        else:
            raise Exception("无法识别日期格式")

    df['precipitation'] = pd.to_numeric(df['precipitation'], errors='coerce')
    df = df.dropna(subset=['precipitation'])
    print(f"处理降水量数据后，剩余 {len(df)} 行记录")

    print("\n正在添加省份信息...")
    df['province'] = df['city'].map(station_to_province)

    unmatched_cities = df[df['province'].isna()]['city'].unique()
    if len(unmatched_cities) > 0:
        print(f"警告: 以下 {len(unmatched_cities)} 个城市未能匹配到省份:")
        for city in unmatched_cities[:10]:  # 只显示前10个
            print(f"  - {city}")
        if len(unmatched_cities) > 10:
            print(f"  ... 还有 {len(unmatched_cities) - 10} 个城市未显示")

    matched_rows = len(df[df['province'].notna()])
    df = df.dropna(subset=['province'])
    print(f"成功匹配 {matched_rows} 行记录到省份")

    print("\n正在计算各省份每日平均降水量...")
    province_daily_avg = df.groupby(['date', 'province'])['precipitation'].agg([
        'mean',
        'count',
        'std',
        'min',
        'max'
    ]).round(4)

    province_daily_avg = province_daily_avg.reset_index()
    province_daily_avg.columns = ['date', 'province', 'avg_precipitation', 
                                 'station_count', 'std_precipitation', 
                                 'min_precipitation', 'max_precipitation']

    province_daily_avg = province_daily_avg.sort_values(['date', 'province'])
    
    print(f"计算完成，共生成 {len(province_daily_avg)} 条省份日均降水记录")

    print(f"\n数据统计:")
    print(f"时间范围: {province_daily_avg['date'].min()} 到 {province_daily_avg['date'].max()}")
    print(f"涵盖省份: {province_daily_avg['province'].nunique()} 个")
    province_counts = province_daily_avg.groupby('province').size().sort_values(ascending=False)
    print("各省份记录数量:")
    for province, count in province_counts.head(10).items():
        print(f"  {province}: {count} 天")

    if output_file is None:
        input_dir = os.path.dirname(input_file)
        output_file = os.path.join(input_dir, "china_precipitation_province_daily_avg_2018_2024.csv")

    try:
        province_daily_avg.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"\n结果已保存到: {output_file}")
    except Exception as e:
        try:
            province_daily_avg.to_csv(output_file, index=False, encoding='gbk')
            print(f"\n结果已保存到: {output_file} (使用GBK编码)")
        except Exception as e2:
            raise Exception(f"保存文件失败: {e2}")

    simple_output = province_daily_avg[['date', 'province', 'avg_precipitation']].copy()
    simple_output_file = output_file.replace('.csv', '_simple.csv')
    
    try:
        simple_output.to_csv(simple_output_file, index=False, encoding='utf-8-sig')
        print(f"简化版本已保存到: {simple_output_file}")
    except:
        simple_output.to_csv(simple_output_file, index=False, encoding='gbk')
        print(f"简化版本已保存到: {simple_output_file} (使用GBK编码)")
    
    return province_daily_avg

def main():
    """主函数"""
    input_file = r"C:\Users\Shaira\Desktop\china_precipitation_2018_2024.csv"
    
    try:
        result_df = process_precipitation_data(input_file)
        
        print("\n处理完成！")
        print(f"生成的数据包含以下列:")
        for col in result_df.columns:
            print(f"  - {col}")
        
        print(f"\n数据样例:")
        print(result_df.head(10))
        
    except Exception as e:
        print(f"处理过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()