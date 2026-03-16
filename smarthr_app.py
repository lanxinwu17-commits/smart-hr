"""
SmartHR 智能人力资源工作台
================================
基于 Streamlit 的全栈 HR 数据分析与 AI 创意工具
技术栈：Python + Streamlit + Pandas + Plotly

功能模块：
1. 招聘漏斗自动化分析
2. 人事数据纠错与薪酬计算
3. AI 文案与海报创意工坊

作者：SmartHR Team
版本：1.0.0
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
import re
from io import BytesIO

# ============================================
# 页面配置与样式初始化
# ============================================

def init_page_config():
    """初始化页面配置，包括标题、图标和布局"""
    st.set_page_config(
        page_title="SmartHR 智能人力资源工作台",
        page_icon="🏢",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def apply_custom_css():
    """
    应用自定义 CSS 样式
    设计原则：简洁、专业、现代科技感
    """
    st.markdown("""
    <style>
    /* 全局字体设置 */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap');

    * {
        font-family: 'Noto Sans SC', sans-serif;
    }

    /* 主色调定义 */
    :root {
        --primary-color: #667eea;
        --secondary-color: #764ba2;
        --accent-color: #f093fb;
        --bg-dark: #1a1a2e;
        --bg-light: #16213e;
        --text-primary: #eaeaea;
        --text-secondary: #a0a0a0;
        --success-color: #00d9ff;
        --warning-color: #ff6b6b;
        --info-color: #4ecdc4;
    }

    /* 主容器样式 */
    .main {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        min-height: 100vh;
    }

    /* 侧边栏样式 */
    .stSidebar {
        background: linear-gradient(180deg, #1a1a2e 0%, #0f0f23 100%) !important;
        border-right: 1px solid rgba(102, 126, 234, 0.2);
    }

    .stSidebar [data-testid="stSidebarNav"] {
        background: transparent;
    }

    /* 标题样式 */
    h1 {
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700 !important;
        letter-spacing: -1px;
    }

    h2, h3 {
        color: #eaeaea !important;
        font-weight: 500 !important;
    }

    /* 卡片样式 */
    .stMetric {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 12px;
        padding: 20px;
        backdrop-filter: blur(10px);
    }

    .stMetric label {
        color: #a0a0a0 !important;
        font-size: 14px !important;
    }

    .stMetric .css-1xarl3l {
        color: #eaeaea !important;
        font-size: 32px !important;
        font-weight: 600 !important;
    }

    /* 按钮样式 */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5) !important;
    }

    /* 上传区域样式 */
    .stFileUploader {
        background: rgba(102, 126, 234, 0.05) !important;
        border: 2px dashed rgba(102, 126, 234, 0.3) !important;
        border-radius: 12px !important;
        padding: 20px !important;
    }

    .stFileUploader:hover {
        border-color: rgba(102, 126, 234, 0.6) !important;
    }

    /* 数据表格样式 */
    .stDataFrame {
        background: rgba(26, 26, 46, 0.8) !important;
        border: 1px solid rgba(102, 126, 234, 0.2) !important;
        border-radius: 12px !important;
    }

    /* 输入框样式 */
    .stTextInput > div > div {
        background: rgba(102, 126, 234, 0.1) !important;
        border: 1px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: 8px !important;
        color: #eaeaea !important;
    }

    .stTextArea > div > div {
        background: rgba(102, 126, 234, 0.1) !important;
        border: 1px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: 8px !important;
        color: #eaeaea !important;
    }

    /* 选择器样式 */
    .stSelectbox > div > div {
        background: rgba(102, 126, 234, 0.1) !important;
        border: 1px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: 8px !important;
        color: #eaeaea !important;
    }

    /* 信息框样式 */
    .stAlert {
        background: rgba(78, 205, 196, 0.1) !important;
        border: 1px solid rgba(78, 205, 196, 0.3) !important;
        border-radius: 8px !important;
    }

    /* 成功提示样式 */
    .stSuccess {
        background: rgba(0, 217, 255, 0.1) !important;
        border: 1px solid rgba(0, 217, 255, 0.3) !important;
        border-radius: 8px !important;
    }

    /* 警告提示样式 */
    .stWarning {
        background: rgba(255, 107, 107, 0.1) !important;
        border: 1px solid rgba(255, 107, 107, 0.3) !important;
        border-radius: 8px !important;
    }

    /* 扩展器样式 */
    .stExpander {
        background: rgba(102, 126, 234, 0.05) !important;
        border: 1px solid rgba(102, 126, 234, 0.2) !important;
        border-radius: 12px !important;
    }

    /* 标签页样式 */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(102, 126, 234, 0.1) !important;
        border-radius: 12px !important;
        padding: 8px !important;
    }

    .stTabs [data-baseweb="tab"] {
        color: #a0a0a0 !important;
        font-weight: 500 !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-radius: 8px !important;
    }

    /* 分隔线样式 */
    hr {
        border-color: rgba(102, 126, 234, 0.2) !important;
    }

    /* 自定义卡片 */
    .custom-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        backdrop-filter: blur(10px);
    }

    /* 渐变文字 */
    .gradient-text {
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* 科技边框 */
    .tech-border {
        position: relative;
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 12px;
        padding: 20px;
    }

    .tech-border::before {
        content: '';
        position: absolute;
        top: -1px;
        left: -1px;
        right: -1px;
        bottom: -1px;
        background: linear-gradient(45deg, #667eea, #764ba2, #f093fb, #667eea);
        border-radius: 12px;
        opacity: 0.3;
        z-index: -1;
        animation: borderGlow 3s ease infinite;
    }

    @keyframes borderGlow {
        0%, 100% { opacity: 0.3; }
        50% { opacity: 0.6; }
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================
# Mock 数据生成模块
# ============================================

def generate_mock_recruitment_data(num_candidates=100):
    """
    生成模拟招聘数据

    Args:
        num_candidates: 候选人数量，默认100

    Returns:
        DataFrame: 包含候选人信息的完整数据集
    """
    # 随机种子保证可重现性
    random.seed(42)

    # 姓氏和名字库
    surnames = ['张', '李', '王', '刘', '陈', '杨', '黄', '赵', '吴', '周', '徐', '孙', '马', '朱', '胡']
    names = ['伟', '芳', '娜', '敏', '静', '丽', '强', '磊', '洋', '艳', '杰', '涛', '明', '超', '秀英']

    # 岗位列表
    positions = ['Java开发工程师', '前端开发工程师', '产品经理', 'UI设计师', '数据分析师', 'HRBP', '销售经理']

    # 状态列表及其流转逻辑
    stages = ['投递', '初筛通过', '面试中', 'Offer发放', '已入职']

    # 生成数据
    data = []
    for i in range(num_candidates):
        # 随机生成候选人姓名
        name = random.choice(surnames) + random.choice(names) + random.choice(['', random.choice(names)])

        # 随机分配岗位
        position = random.choice(positions)

        # 随机生成投递日期（最近3个月）
        days_ago = random.randint(1, 90)
        apply_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')

        # 根据概率确定当前阶段
        rand = random.random()
        if rand < 0.4:  # 40%停留在投递
            current_stage = '投递'
            stage_num = 0
        elif rand < 0.6:  # 20%初筛通过
            current_stage = '初筛通过'
            stage_num = 1
        elif rand < 0.75:  # 15%面试中
            current_stage = '面试中'
            stage_num = 2
        elif rand < 0.85:  # 10%Offer发放
            current_stage = 'Offer发放'
            stage_num = 3
        else:  # 15%已入职
            current_stage = '已入职'
            stage_num = 4

        # 各阶段状态
        resume_screening = '通过' if stage_num >= 1 else ('未通过' if random.random() < 0.3 else '待审核')
        interview_status = '通过' if stage_num >= 2 else ('进行中' if stage_num == 1 else '未开始')
        offer_status = '已接受' if stage_num >= 4 else ('已发放' if stage_num == 3 else '未发放')
        hired = '是' if stage_num == 4 else '否'

        data.append({
            '候选人姓名': name,
            '岗位': position,
            '投递日期': apply_date,
            '简历筛选': resume_screening,
            '初筛状态': resume_screening,
            '面试状态': interview_status,
            'Offer状态': offer_status,
            '是否入职': hired
        })

    return pd.DataFrame(data)

def generate_mock_employee_data(num_employees=50):
    """
    生成模拟员工数据，包含一些错误数据用于测试纠错功能

    Args:
        num_employees: 员工数量，默认50

    Returns:
        DataFrame: 包含员工信息和薪酬数据的完整数据集
    """
    random.seed(42)

    # 姓氏库
    surnames = ['张', '李', '王', '刘', '陈', '杨', '黄', '赵', '吴', '周']
    names = ['伟', '芳', '娜', '敏', '静', '丽', '强', '磊', '洋', '艳']

    # 部门列表
    departments = ['技术部', '产品部', '设计部', '销售部', '人事部', '财务部', '市场部']

    # 岗位列表
    positions = ['高级工程师', '产品经理', '设计师', '销售代表', 'HR专员', '会计', '市场专员']

    data = []
    used_ids = set()

    for i in range(num_employees):
        # 生成唯一工号，但故意制造一些重复用于测试
        if i == 5 or i == 10:  # 故意制造重复的工号
            employee_id = list(used_ids)[0] if used_ids else f"{10001 + i}"
        elif random.random() < 0.1:  # 10%的概率生成格式错误的工号
            employee_id = f"E{random.randint(100, 999)}"
        else:
            employee_id = f"{10001 + i}"
        used_ids.add(employee_id)

        # 姓名
        name = random.choice(surnames) + random.choice(names)

        # 部门
        department = random.choice(departments)

        # 岗位
        position = random.choice(positions)

        # 入职日期（格式故意混合，用于测试日期清洗）
        days_ago = random.randint(30, 1000)
        date_formats = ['%Y-%m-%d', '%Y/%m/%d', '%d-%m-%Y', '%m/%d/%Y']
        hire_date = (datetime.now() - timedelta(days=days_ago)).strftime(random.choice(date_formats))

        # 银行卡号（故意制造一些错误）
        if random.random() < 0.15:  # 15%错误格式
            bank_card = f"{random.randint(10000000000, 99999999999)}"  # 11位，错误
        elif random.random() < 0.1:  # 10%包含字母
            bank_card = f"6225{random.randint(100000000000, 999999999999)}A"
        else:
            bank_card = f"6225{random.randint(100000000000, 999999999999)}"  # 16位

        # 时薪（元/小时）
        hourly_rate = round(random.uniform(50, 200), 2)

        # 当月加班时长（故意制造负数或过大的值）
        if random.random() < 0.05:  # 5% 负数
            overtime_hours = random.randint(-5, -1)
        elif random.random() < 0.1:  # 10% 超大值
            overtime_hours = random.randint(200, 300)
        else:
            overtime_hours = round(random.uniform(0, 50), 1)

        data.append({
            '工号': employee_id,
            '姓名': name,
            '部门': department,
            '岗位': position,
            '入职日期': hire_date,
            '银行卡号': bank_card,
            '时薪(元)': hourly_rate,
            '当月加班时长(小时)': overtime_hours
        })

    return pd.DataFrame(data)

def generate_mock_company_profile():
    """
    生成模拟公司简介数据

    Returns:
        list: 不同行业的公司简介列表
    """
    profiles = [
        {
            'name': '未来科技有限公司',
            'industry': '互联网/AI',
            'description': '''未来科技是一家专注于人工智能和大数据技术的创新型企业。
            成立于2018年，总部位于北京中关村。公司致力于为企业提供智能化解决方案，
            核心产品包括智能客服系统、数据分析平台和自动化营销工具。
            我们的使命是"用AI赋能每一家企业"，愿景是成为全球领先的AI技术提供商。
            公司文化倡导创新、协作、用户至上，拥有一支来自世界顶尖高校和技术巨头的研发团队。'''
        },
        {
            'name': '绿野生态集团',
            'industry': '环保/新能源',
            'description': '''绿野生态集团是国内领先的生态环保和新能源解决方案提供商。
            公司专注于可再生能源开发、环境治理和碳中和服务。成立于2010年，
            业务覆盖全国30个省份，拥有员工3000余人。我们的核心价值观是"绿色、可持续、共赢"，
            致力于构建人与自然和谐共生的美好未来。曾获得国家科技进步奖、绿色发展示范企业等荣誉。'''
        },
        {
            'name': '星辰金融控股',
            'industry': '金融科技',
            'description': '''星辰金融控股是一家创新型金融科技公司，专注于为年轻一代提供智能理财服务。
            通过大数据风控和AI算法，我们为超过500万用户提供个性化的投资建议和资产管理服务。
            公司成立于2015年，已完成多轮融资，估值超过10亿美元。
            我们推崇"专业、透明、可信赖"的服务理念，让每个人都能享受专业的金融服务。'''
        },
        {
            'name': '云端文创工作室',
            'industry': '文化创意',
            'description': '''云端文创是一家专注于数字内容创作和文化IP孵化的创意公司。
            我们的业务涵盖游戏美术设计、动画制作、品牌视觉设计和虚拟偶像运营。
            团队由来自全球各地的艺术家和技术专家组成，曾参与多个知名游戏和影视项目的制作。
            公司文化开放包容，鼓励创意表达，提供灵活的工作方式和良好的创作氛围。'''
        }
    ]
    return profiles

# ============================================
# 招聘漏斗分析模块
# ============================================

def analyze_recruitment_funnel(df):
    """
    分析招聘漏斗数据，计算各阶段人数和转化率

    Args:
        df: 包含招聘数据的DataFrame

    Returns:
        dict: 包含各阶段统计数据的字典
    """
    # 统计各阶段人数
    total_applied = len(df)

    # 初筛通过人数（简历筛选为"通过"或初筛状态为"通过"）
    passed_screening = len(df[df['初筛状态'].isin(['通过', '已通过'])])

    # 进入面试人数（面试状态为"通过"或"进行中"）
    in_interview = len(df[df['面试状态'].isin(['通过', '进行中', '已安排', '已完成'])])

    # Offer发放人数
    offer_sent = len(df[df['Offer状态'].isin(['已发放', '已接受', '已拒绝'])])

    # 已入职人数
    hired = len(df[df['是否入职'] == '是'])

    # 构建漏斗数据
    funnel_data = {
        'stages': ['投递', '初筛通过', '面试中', 'Offer发放', '已入职'],
        'counts': [total_applied, passed_screening, in_interview, offer_sent, hired],
        'conversion_rates': [],
        'dropoff_rates': []
    }

    # 计算转化率
    for i in range(len(funnel_data['counts'])):
        if i == 0:
            # 投递阶段的转化率为100%
            funnel_data['conversion_rates'].append(100.0)
        else:
            # 相对于上一阶段的转化率
            prev_count = funnel_data['counts'][i-1]
            curr_count = funnel_data['counts'][i]
            rate = (curr_count / prev_count * 100) if prev_count > 0 else 0
            funnel_data['conversion_rates'].append(round(rate, 2))

            # 流失率
            dropoff = 100 - rate
            funnel_data['dropoff_rates'].append(round(dropoff, 2))

    # 整体转化率（投递到入职）
    funnel_data['overall_conversion'] = round((hired / total_applied * 100), 2) if total_applied > 0 else 0

    return funnel_data

def create_funnel_chart(funnel_data):
    """
    使用 Plotly 创建动态漏斗图

    Args:
        funnel_data: 漏斗统计数据字典

    Returns:
        Figure: Plotly 图表对象
    """
    fig = go.Figure(go.Funnel(
        y=funnel_data['stages'],
        x=funnel_data['counts'],
        textposition="inside",
        textinfo="value+percent previous",
        opacity=0.85,
        marker={
            "color": ["#667eea", "#764ba2", "#f093fb", "#f5576c", "#4facfe"],
            "line": {"width": [2, 2, 2, 2, 2], "color": ["white"] * 5}
        },
        connector={"line": {"color": "royalblue", "dash": "dot", "width": 3}}
    ))

    fig.update_layout(
        title={
            'text': '招聘漏斗分析图',
            'font': {'size': 24, 'color': '#eaeaea', 'family': 'Noto Sans SC'},
            'x': 0.5,
            'xanchor': 'center'
        },
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#eaeaea', family='Noto Sans SC'),
        margin=dict(l=100, r=50, t=80, b=50),
        height=500
    )

    return fig

def generate_recruitment_insights(funnel_data):
    """
    生成智能诊断建议

    Args:
        funnel_data: 漏斗统计数据

    Returns:
        dict: 包含诊断结果和建议的字典
    """
    insights = {
        'bottleneck_stage': '',
        'bottleneck_rate': 0,
        'suggestions': [],
        'health_score': 0
    }

    # 找出流失率最高的环节
    max_dropoff = 0
    bottleneck_idx = 0

    for i in range(1, len(funnel_data['dropoff_rates'])):
        if funnel_data['dropoff_rates'][i] > max_dropoff:
            max_dropoff = funnel_data['dropoff_rates'][i]
            bottleneck_idx = i

    insights['bottleneck_stage'] = funnel_data['stages'][bottleneck_idx]
    insights['bottleneck_rate'] = max_dropoff

    # 根据瓶颈环节生成建议
    if insights['bottleneck_stage'] == '初筛通过':
        insights['suggestions'] = [
            '优化职位描述，确保与目标候选人画像匹配',
            '检查简历筛选标准是否过于严格',
            '考虑使用AI简历解析工具提高筛选效率',
            '分析未通过初筛的简历特征，优化招聘渠道'
        ]
    elif insights['bottleneck_stage'] == '面试中':
        insights['suggestions'] = [
            '优化面试流程，减少候选人流失',
            '加强面试官培训，提升面试体验',
            '缩短面试反馈周期，提高响应速度',
            '增加在线测评环节，提前筛选匹配度'
        ]
    elif insights['bottleneck_stage'] == 'Offer发放':
        insights['suggestions'] = [
            '检查薪酬竞争力，对比市场水平',
            '优化Offer沟通策略，突出职位亮点',
            '加快Offer发放速度，避免候选人流失',
            '增加签约奖金或其他福利吸引候选人'
        ]
    elif insights['bottleneck_stage'] == '已入职':
        insights['suggestions'] = [
            '优化入职流程，提前准备入职材料',
            '加强Offer到入职期间的关怀和沟通',
            '建立人才储备池，应对突发情况',
            '分析入职失败原因，改进招聘策略'
        ]

    # 计算健康分数（基于整体转化率）
    overall = funnel_data['overall_conversion']
    if overall >= 10:
        insights['health_score'] = 90
    elif overall >= 5:
        insights['health_score'] = 75
    elif overall >= 2:
        insights['health_score'] = 60
    else:
        insights['health_score'] = 40

    return insights

def render_recruitment_module():
    """
    渲染招聘漏斗分析模块的完整界面
    """
    st.header("📊 招聘漏斗自动化分析")
    st.markdown("---")

    # 创建两列布局
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("📁 数据上传")

        # 文件上传组件
        uploaded_file = st.file_uploader(
            "上传招聘数据文件（Excel/CSV）",
            type=['xlsx', 'xls', 'csv'],
            help="文件需包含：候选人姓名、岗位、投递日期、各轮面试状态、是否入职"
        )

        # 使用模拟数据按钮
        use_mock = st.checkbox("使用模拟数据预览功能", value=False)

        if use_mock:
            st.info("✅ 已加载模拟数据（100位候选人）")
            df = generate_mock_recruitment_data(100)
            st.success(f"数据加载成功！共 {len(df)} 条记录")
        elif uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                st.success(f"文件上传成功！共 {len(df)} 条记录")
            except Exception as e:
                st.error(f"文件读取失败：{str(e)}")
                return
        else:
            st.info("👆 请上传数据文件或勾选使用模拟数据")
            return

        # 显示数据预览
        with st.expander("📋 数据预览"):
            st.dataframe(df.head(10), use_container_width=True)

    with col2:
        if 'df' in locals():
            # 执行漏斗分析
            funnel_data = analyze_recruitment_funnel(df)

            # 创建指标卡片
            st.subheader("📈 关键指标")
            metric_cols = st.columns(5)

            for i, (stage, count) in enumerate(zip(funnel_data['stages'], funnel_data['counts'])):
                with metric_cols[i]:
                    st.metric(
                        label=stage,
                        value=count,
                        delta=f"{funnel_data['conversion_rates'][i]}%" if i > 0 else "基准"
                    )

            # 绘制漏斗图
            fig = create_funnel_chart(funnel_data)
            st.plotly_chart(fig, use_container_width=True)

    # 智能诊断区域
    if 'df' in locals():
        st.markdown("---")
        st.subheader("🤖 智能诊断与优化建议")

        insights = generate_recruitment_insights(funnel_data)

        diag_col1, diag_col2 = st.columns([1, 1])

        with diag_col1:
            # 健康度评分
            score = insights['health_score']
            score_color = "#00d9ff" if score >= 80 else "#ffd93d" if score >= 60 else "#ff6b6b"

            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
                        border: 1px solid rgba(102, 126, 234, 0.3);
                        border-radius: 16px; padding: 24px; text-align: center;">
                <h3 style="margin-bottom: 16px;">招聘流程健康度</h3>
                <div style="font-size: 64px; font-weight: 700; color: {score_color};">
                    {score}
                </div>
                <div style="font-size: 14px; color: #a0a0a0; margin-top: 8px;">
                    {'优秀' if score >= 80 else '良好' if score >= 60 else '需改进'}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # 瓶颈分析
            st.markdown(f"""
            <div style="margin-top: 20px; padding: 20px; background: rgba(255, 107, 107, 0.1);
                        border: 1px solid rgba(255, 107, 107, 0.3); border-radius: 12px;">
                <h4 style="color: #ff6b6b; margin: 0;">⚠️ 主要瓶颈</h4>
                <p style="margin: 10px 0 0 0; color: #eaeaea;">
                    <strong>{insights['bottleneck_stage']}</strong> 环节
                </p>
                <p style="margin: 5px 0 0 0; color: #a0a0a0; font-size: 24px;">
                    流失率：<span style="color: #ff6b6b; font-weight: 700;">{insights['bottleneck_rate']}%</span>
                </p>
            </div>
            """, unsafe_allow_html=True)

        with diag_col2:
            st.markdown("#### 💡 优化建议")
            for suggestion in insights['suggestions']:
                st.markdown(f"""
                <div style="padding: 12px 16px; margin: 8px 0;
                            background: rgba(0, 217, 255, 0.1);
                            border-left: 4px solid #00d9ff;
                            border-radius: 0 8px 8px 0;">
                    {suggestion}
                </div>
                """, unsafe_allow_html=True)

        # 详细数据表
        with st.expander("📊 详细转化数据"):
            detail_df = pd.DataFrame({
                '阶段': funnel_data['stages'],
                '人数': funnel_data['counts'],
                '阶段转化率(%)': [f"{r}%" for r in funnel_data['conversion_rates']],
                '流失率(%)': ['-'] + [f"{r}%" for r in funnel_data['dropoff_rates']]
            })
            st.dataframe(detail_df, use_container_width=True)

# ============================================
# HR 数据纠错与薪酬计算模块
# ============================================

def validate_employee_id(employee_ids):
    """
    验证工号格式

    Args:
        employee_ids: 工号列表

    Returns:
        list: 包含每个工号验证结果的字典列表
    """
    results = []
    seen_ids = {}

    for idx, emp_id in enumerate(employee_ids):
        error = None

        # 检查是否为纯数字
        if not re.match(r'^\d+$', str(emp_id)):
            error = "工号必须纯数字"
        # 检查重复
        elif str(emp_id) in seen_ids:
            error = f"工号重复（行{seen_ids[str(emp_id)] + 1}）"
        else:
            seen_ids[str(emp_id)] = idx

        results.append({
            'value': emp_id,
            'valid': error is None,
            'error': error
        })

    return results

def validate_bank_card(card_numbers):
    """
    验证银行卡号格式（通常为16-19位数字）

    Args:
        card_numbers: 银行卡号列表

    Returns:
        list: 包含每个银行卡号验证结果的字典列表
    """
    results = []

    for card in card_numbers:
        error = None
        card_str = str(card).replace(' ', '').replace('-', '')

        # 检查是否为纯数字
        if not card_str.isdigit():
            error = "卡号包含非数字字符"
        # 检查长度
        elif len(card_str) < 16 or len(card_str) > 19:
            error = f"卡号长度错误（{len(card_str)}位，应为16-19位）"

        results.append({
            'value': card,
            'valid': error is None,
            'error': error
        })

    return results

def standardize_date(date_values):
    """
    统一日期格式为 YYYY-MM-DD

    Args:
        date_values: 日期列表

    Returns:
        list: 包含标准化后日期的字典列表
    """
    results = []
    date_patterns = [
        (r'^\d{4}-\d{2}-\d{2}$', '%Y-%m-%d'),
        (r'^\d{4}/\d{2}/\d{2}$', '%Y/%m/%d'),
        (r'^\d{2}-\d{2}-\d{4}$', '%d-%m-%Y'),
        (r'^\d{2}/\d{2}/\d{4}$', '%m/%d/%Y'),
        (r'^\d{8}$', '%Y%m%d')
    ]

    for date_val in date_values:
        standardized = None
        error = None

        if pd.isna(date_val) or date_val == '':
            error = "日期为空"
        else:
            date_str = str(date_val).strip()

            for pattern, fmt in date_patterns:
                if re.match(pattern, date_str):
                    try:
                        dt = datetime.strptime(date_str, fmt)
                        standardized = dt.strftime('%Y-%m-%d')
                        break
                    except:
                        pass

            if standardized is None:
                error = "日期格式无法识别"

        results.append({
            'original': date_val,
            'standardized': standardized,
            'valid': error is None,
            'error': error
        })

    return results

def calculate_overtime_pay(overtime_hours, hourly_rate, deductible_hours=10):
    """
    计算加班费

    规则：
    1. 每月前 deductible_hours 小时不计入加班费
    2. 实付加班时长 = max(0, 总时长 - 10)
    3. 加班费 = 实付时长 × 时薪

    Args:
        overtime_hours: 加班时长
        hourly_rate: 时薪
        deductible_hours: 不计薪的小时数，默认10

    Returns:
        dict: 包含计算结果的字典
    """
    try:
        hours = float(overtime_hours)
        rate = float(hourly_rate)

        # 检查异常值
        if hours < 0:
            return {
                'valid': False,
                'error': '加班时长不能为负数',
                'payable_hours': 0,
                'overtime_pay': 0
            }

        if hours > 160:  # 一个月按4周×40小时计算
            return {
                'valid': False,
                'error': '加班时长异常（超过160小时）',
                'payable_hours': 0,
                'overtime_pay': 0
            }

        # 计算实付加班时长
        payable_hours = max(0, hours - deductible_hours)

        # 计算加班费
        overtime_pay = payable_hours * rate

        return {
            'valid': True,
            'error': None,
            'original_hours': hours,
            'deductible_hours': deductible_hours,
            'payable_hours': round(payable_hours, 2),
            'hourly_rate': rate,
            'overtime_pay': round(overtime_pay, 2)
        }

    except (ValueError, TypeError):
        return {
            'valid': False,
            'error': '数据格式错误',
            'payable_hours': 0,
            'overtime_pay': 0
        }

def audit_hr_data(df):
    """
    全面审计HR数据

    Args:
        df: 员工数据DataFrame

    Returns:
        dict: 包含审计结果的字典
    """
    audit_results = {
        'employee_id_check': validate_employee_id(df['工号'].tolist()),
        'bank_card_check': validate_bank_card(df['银行卡号'].tolist()),
        'date_check': standardize_date(df['入职日期'].tolist()),
        'overtime_calculations': [],
        'summary': {
            'total_records': len(df),
            'id_errors': 0,
            'bank_errors': 0,
            'date_errors': 0,
            'overtime_errors': 0
        }
    }

    # 统计错误数量
    for check in audit_results['employee_id_check']:
        if not check['valid']:
            audit_results['summary']['id_errors'] += 1

    for check in audit_results['bank_card_check']:
        if not check['valid']:
            audit_results['summary']['bank_errors'] += 1

    for check in audit_results['date_check']:
        if not check['valid']:
            audit_results['summary']['date_errors'] += 1

    # 计算加班费
    for idx, row in df.iterrows():
        calc_result = calculate_overtime_pay(
            row['当月加班时长(小时)'],
            row['时薪(元)']
        )
        audit_results['overtime_calculations'].append(calc_result)

        if not calc_result['valid']:
            audit_results['summary']['overtime_errors'] += 1

    return audit_results

def render_hr_auditor_module():
    """
    渲染HR数据纠错与薪酬计算模块
    """
    st.header("🔍 HR 数据纠错与薪酬计算")
    st.markdown("---")

    # 文件上传区域
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("📁 数据上传")

        uploaded_file = st.file_uploader(
            "上传员工数据文件（Excel/CSV）",
            type=['xlsx', 'xls', 'csv'],
            key="hr_uploader",
            help="文件需包含：工号、姓名、部门、入职日期、银行卡号、时薪、加班时长"
        )

        use_mock = st.checkbox("使用模拟数据预览功能", key="hr_mock")

        if use_mock:
            st.info("✅ 已加载模拟员工数据（50人，含错误数据）")
            df = generate_mock_employee_data(50)
        elif uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
            except Exception as e:
                st.error(f"文件读取失败：{str(e)}")
                return
        else:
            st.info("👆 请上传数据文件或勾选使用模拟数据")
            return

        # 显示原始数据
        with st.expander("📋 原始数据预览"):
            st.dataframe(df, use_container_width=True)

    with col2:
        if 'df' in locals():
            # 执行数据审计
            audit_results = audit_hr_data(df)

            st.subheader("📊 审计概览")

            # 错误统计卡片
            stat_cols = st.columns(4)
            stats = [
                ("总记录数", audit_results['summary']['total_records'], "#667eea"),
                ("工号错误", audit_results['summary']['id_errors'], "#ff6b6b"),
                ("银行卡错误", audit_results['summary']['bank_errors'], "#ffd93d"),
                ("日期/加班错误", audit_results['summary']['date_errors'] + audit_results['summary']['overtime_errors'], "#f093fb")
            ]

            for col, (label, value, color) in zip(stat_cols, stats):
                with col:
                    st.markdown(f"""
                    <div style="background: rgba(102, 126, 234, 0.1);
                                border: 1px solid {color};
                                border-radius: 12px; padding: 16px;
                                text-align: center;">
                        <div style="font-size: 12px; color: #a0a0a0;">{label}</div>
                        <div style="font-size: 32px; font-weight: 700; color: {color};">{value}</div>
                    </div>
                    """, unsafe_allow_html=True)

            # 详细纠错结果
            st.markdown("---")
            st.subheader("🔍 详细纠错结果")

            # 创建纠错详情表
            audit_df = df.copy()
            audit_df['工号状态'] = ['✅' if r['valid'] else f"❌ {r['error']}" for r in audit_results['employee_id_check']]
            audit_df['银行卡状态'] = ['✅' if r['valid'] else f"❌ {r['error']}" for r in audit_results['bank_card_check']]
            audit_df['日期标准化'] = [r['standardized'] if r['valid'] else f"❌ {r['error']}" for r in audit_results['date_check']]

            # 显示有错误的记录
            has_errors = (
                (audit_df['工号状态'].str.startswith('❌')) |
                (audit_df['银行卡状态'].str.startswith('❌')) |
                (audit_df['日期标准化'].str.startswith('❌'))
            )

            if has_errors.any():
                st.warning(f"发现 {has_errors.sum()} 条记录存在数据问题")
                st.dataframe(audit_df[has_errors], use_container_width=True)
            else:
                st.success("✅ 所有数据格式正确！")

    # 薪酬计算结果
    if 'df' in locals():
        st.markdown("---")
        st.subheader("💰 加班费计算结果")

        # 构建薪酬计算结果表
        payroll_data = []
        for idx, (row, calc) in enumerate(zip(df.itertuples(), audit_results['overtime_calculations'])):
            payroll_data.append({
                '工号': row.工号,
                '姓名': row.姓名,
                '部门': row.部门,
                '当月加班时长': calc.get('original_hours', 0),
                '不计薪时长': calc.get('deductible_hours', 10),
                '实付时长': calc.get('payable_hours', 0),
                '时薪': calc.get('hourly_rate', 0),
                '加班工资': calc.get('overtime_pay', 0),
                '状态': '✅ 正常' if calc['valid'] else f"❌ {calc['error']}"
            })

        payroll_df = pd.DataFrame(payroll_data)

        # 显示汇总信息
        total_payroll = payroll_df['加班工资'].sum()
        valid_records = payroll_df[payroll_df['状态'].str.startswith('✅')]

        summary_cols = st.columns(3)
        with summary_cols[0]:
            st.metric("本月加班费总额", f"¥{total_payroll:,.2f}")
        with summary_cols[1]:
            st.metric("有效计算记录", f"{len(valid_records)} 条")
        with summary_cols[2]:
            st.metric("平均加班费", f"¥{valid_records['加班工资'].mean():.2f}" if len(valid_records) > 0 else "¥0.00")

        # 显示详细计算表
        with st.expander("📋 查看详细计算表"):
            st.dataframe(payroll_df, use_container_width=True)

        # 下载处理后的文件
        st.markdown("---")
        st.subheader("💾 导出处理结果")

        # 准备导出数据
        export_df = df.copy()
        export_df['工号验证'] = [r['valid'] for r in audit_results['employee_id_check']]
        export_df['银行卡验证'] = [r['valid'] for r in audit_results['bank_card_check']]
        export_df['入职日期_标准化'] = [r['standardized'] for r in audit_results['date_check']]
        export_df['实付加班时长'] = [r['payable_hours'] for r in audit_results['overtime_calculations']]
        export_df['加班工资'] = [r['overtime_pay'] for r in audit_results['overtime_calculations']]

        # 创建下载按钮
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            export_df.to_excel(writer, sheet_name='员工数据', index=False)
            payroll_df.to_excel(writer, sheet_name='薪酬计算', index=False)

        st.download_button(
            label="📥 下载处理后的Excel文件",
            data=buffer.getvalue(),
            file_name=f"HR数据处理结果_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# ============================================
# AI 文案与海报创意工坊模块
# ============================================

def extract_keywords(company_description):
    """
    从公司描述中提取关键词（模拟企业画像提取）

    Args:
        company_description: 公司简介文本

    Returns:
        dict: 包含提取的关键词字典
    """
    # 行业关键词库
    industry_keywords = {
        '科技/互联网': ['科技', '互联网', 'AI', '人工智能', '大数据', '软件', '开发', '技术', '创新', '数字化'],
        '金融': ['金融', '银行', '投资', '理财', '支付', '保险', '风控', '证券', '基金'],
        '教育': ['教育', '培训', '学习', '课程', '知识', '学术', '教学', '学校'],
        '医疗': ['医疗', '健康', '医药', '医院', '生物', '诊断', '治疗', '护理'],
        '消费/零售': ['消费', '零售', '电商', '品牌', '购物', '商品', '销售', '市场'],
        '文化/创意': ['文化', '创意', '设计', '艺术', '内容', '媒体', '游戏', '动画'],
        '制造': ['制造', '工业', '生产', '供应链', '硬件', '设备', '工厂'],
        '新能源/环保': ['能源', '环保', '绿色', '可持续', '碳中和', '清洁', '生态']
    }

    # 企业文化关键词
    culture_keywords = ['创新', '协作', '用户至上', '开放', '包容', '高效', '专业', '诚信', '共赢', '成长']

    # 福利关键词
    benefit_keywords = ['弹性', '远程', '假期', '奖金', '股权', '培训', '晋升', '团队建设', '健康', '餐补']

    # 提取行业标签
    matched_industries = []
    for industry, keywords in industry_keywords.items():
        score = sum(1 for kw in keywords if kw in company_description)
        if score > 0:
            matched_industries.append((industry, score))

    matched_industries.sort(key=lambda x: x[1], reverse=True)
    top_industries = [ind[0] for ind in matched_industries[:2]]

    # 提取企业文化关键词
    extracted_culture = [kw for kw in culture_keywords if kw in company_description]

    # 提取可能的福利关键词
    extracted_benefits = [kw for kw in benefit_keywords if kw in company_description]

    # 提取核心技术/产品
    tech_patterns = [
        r'(\w+平台)', r'(\w+系统)', r'(\w+解决方案)', r'(智能\w+)',
        r'(\w+服务)', r'(\w+产品)', r'(\w+工具)'
    ]
    tech_products = []
    for pattern in tech_patterns:
        matches = re.findall(pattern, company_description)
        tech_products.extend(matches)
    tech_products = list(set(tech_products))[:5]  # 去重并限制数量

    return {
        'industries': top_industries if top_industries else ['互联网/科技'],
        'culture': extracted_culture if extracted_culture else ['创新', '协作'],
        'benefits': extracted_benefits if extracted_benefits else ['弹性工作', '团队氛围'],
        'tech_products': tech_products if tech_products else ['创新产品'],
        'mission': extract_mission(company_description)
    }

def extract_mission(description):
    """提取公司使命或愿景"""
    mission_patterns = [
        r'使命是["""]?([^"""\n]+)["""]?',
        r'愿景是["""]?([^"""\n]+)["""]?',
        r'致力于["""]?([^"""\n]+)["""]?',
        r'专注于["""]?([^"""\n]+)["""]?'
    ]

    for pattern in mission_patterns:
        match = re.search(pattern, description)
        if match:
            return match.group(1).strip()[:50]

    return "用创新改变世界"

def generate_job_posting(job_title, company_keywords, tone='professional'):
    """
    生成招聘文案

    Args:
        job_title: 岗位名称
        company_keywords: 公司关键词字典
        tone: 文案风格（professional/young/friendly）

    Returns:
        dict: 包含不同格式文案的字典
    """
    industries = '、'.join(company_keywords['industries'])
    culture = '、'.join(company_keywords['culture'][:3])
    benefits = '、'.join(company_keywords['benefits'][:3])
    mission = company_keywords['mission']

    templates = {
        'professional': {
            'title': f"【招聘】{job_title} | {industries}领军企业",
            'short': f"加入{industries.split('、')[0]}领先企业，担任{job_title}。我们秉承{culture}的企业文化，期待您的加入！",
            'full': f"""🏢 关于我们
我们是一家专注于{industries.split('、')[0]}的创新企业，{mission}。

🎯 岗位：{job_title}

✨ 为什么选择我们？
• 行业领先：在{industries}领域具有深厚积累和良好口碑
• 企业文化：{culture}
• 优厚福利：{benefits}等完善福利体系

💼 我们期待这样的你
• 对{industries.split('、')[0]}行业充满热情
• 具备{job_title}所需的专业技能和职业素养
• 认同我们的企业文化，渴望与优秀的团队共同成长

🚀 加入我们，共创未来！"""
        },
        'young': {
            'title': f"🚀 招{job_title}！来和我们一起搞事情！",
            'short': f"{culture}氛围，{benefits}福利～找的就是你！",
            'full': f"""Hey，年轻的创造者！👋

你是不是也在找一个能让你大展身手的舞台？
一个{culture}的团队？
一份{benefits}的工作？

那你来对地方了！✨

我们正在找一位超酷的 {job_title}
一起做出让人眼前一亮的{company_keywords['tech_products'][0] if company_keywords['tech_products'] else '产品'}！

🎮 在这里你可以：
• 和一群有趣的灵魂一起工作
• 扁平化管理，你的声音会被听见
• 不定期团建、下午茶、节日惊喜
• 拒绝996，工作生活都要精彩

别犹豫了，简历砸过来吧！📨

#招聘 #{job_title} #{industries.split('、')[0]}"""
        },
        'friendly': {
            'title': f"寻{job_title} | 寻找志同道合的你",
            'short': f"{culture}的工作氛围，等待同样热爱{industries.split('、')[0]}的你加入！",
            'full': f"""你好，未来的伙伴！🌟

我们正在寻找一位 {job_title}，
也许，你就是我们要找的那个人。

🏢 关于我们
一家{culture}的{industries.split('、')[0]}公司，
我们的使命是：{mission}

💝 我们能给你
• {benefits}——让你安心工作，快乐生活
• 平等开放的团队氛围——每个人的想法都被尊重
• 成长空间——我们希望你在这里收获的不只是一份工作

🤝 我们期待你
• 对{job_title}这份工作有热情
• 愿意学习，乐于分享
• 相信{company_keywords['culture'][0] if company_keywords['culture'] else '协作'}的力量

如果你有兴趣，欢迎联系我们聊聊～
期待与你相遇！💌"""
        }
    }

    return templates.get(tone, templates['professional'])

def generate_poster_prompt(job_title, company_keywords, style='tech'):
    """
    生成海报设计的描述词（Prompt）

    Args:
        job_title: 岗位名称
        company_keywords: 公司关键词字典
        style: 海报风格（tech/retro/future/minimal）

    Returns:
        dict: 包含中英文Prompt的字典
    """
    style_configs = {
        'tech': {
            'name': '科技风',
            'desc': '现代科技风格，使用蓝色和紫色渐变，电路板纹理背景，发光线条，数字化元素，半透明几何图形，专业大气',
            'keywords': ['technology', 'blue purple gradient', 'circuit pattern', 'glowing lines', 'digital', 'geometric', 'professional']
        },
        'retro': {
            'name': '复古风',
            'desc': '复古怀旧风格，使用暖色调（橙色、棕色），老式纸张纹理，手绘插图元素，手写字体风格，温暖亲切',
            'keywords': ['retro', 'warm tones', 'orange brown', 'vintage paper texture', 'hand drawn illustration', 'warm', 'nostalgic']
        },
        'future': {
            'name': '未来风',
            'desc': '赛博朋克未来风格，霓虹色彩（青色、洋红），城市夜景背景，全息投影效果，光线轨迹，炫酷动感',
            'keywords': ['cyberpunk', 'neon colors', 'cyan magenta', 'city nightscape', 'holographic', 'light trails', 'dynamic']
        },
        'minimal': {
            'name': '极简风',
            'desc': '极简主义风格，大面积留白，单色配色（黑白灰为主），简洁线条，无衬线字体，高级优雅',
            'keywords': ['minimalist', 'white space', 'monochrome', 'clean lines', 'sans-serif', 'elegant', 'premium']
        }
    }

    config = style_configs.get(style, style_configs['tech'])
    industries = company_keywords['industries'][0] if company_keywords['industries'] else '科技'
    culture = company_keywords['culture'][0] if company_keywords['culture'] else '创新'

    # 中文Prompt
    cn_prompt = f"""
【海报设计描述词】

风格：{config['name']}
主题：{job_title}招聘海报
行业：{industries}

画面描述：
{config['desc']}

核心元素：
• 突出岗位名称「{job_title}」
• 体现企业文化「{culture}」
• 公司Logo位置预留
• 二维码放置区域

配色方案：
{config['desc'].split('，')[1] if '，' in config['desc'] else '根据风格选择'}

输出格式：竖版海报，1080x1920px，适合社交媒体分享
"""

    # 英文Prompt（用于DALL-E/Midjourney等）
    en_prompt = f"""
A professional recruitment poster for "{job_title}" position,
{' '.join(config['keywords'])},
text "{job_title}" prominently displayed,
"{industries}" industry theme,
"{culture}" corporate culture elements,
clean layout with space for company logo and QR code,
portrait orientation 1080x1920,
high quality, 8k, professional design
"""

    return {
        'style_name': config['name'],
        'chinese_prompt': cn_prompt.strip(),
        'english_prompt': en_prompt.strip(),
        'keywords': config['keywords']
    }

def render_creative_hub_module():
    """
    渲染AI文案与海报创意工坊模块
    """
    st.header("🎨 AI 文案与海报创意工坊")
    st.markdown("---")

    # 左侧：输入区域
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("🏢 企业画像")

        # 公司描述输入
        company_input_method = st.radio(
            "输入方式",
            ["手动输入", "使用模拟公司数据"],
            horizontal=True
        )

        if company_input_method == "使用模拟公司数据":
            mock_profiles = generate_mock_company_profile()
            selected_company = st.selectbox(
                "选择模拟公司",
                options=[p['name'] for p in mock_profiles]
            )
            company_desc = [p for p in mock_profiles if p['name'] == selected_company][0]['description']
            st.text_area("公司简介", value=company_desc, height=150, disabled=True)
        else:
            company_desc = st.text_area(
                "请输入公司简介或官网描述",
                placeholder="例如：我们是一家专注于人工智能和大数据的创新企业，成立于2018年...",
                height=150
            )

        # 岗位信息输入
        st.markdown("---")
        st.subheader("💼 岗位信息")

        job_title = st.text_input(
            "岗位名称",
            placeholder="例如：高级Java开发工程师"
        )

        tone_style = st.select_slider(
            "文案风格",
            options=["专业正式", "年轻活力", "亲切友好"],
            value="专业正式"
        )

        poster_style = st.selectbox(
            "海报风格",
            options=[
                ('tech', '科技风 🔵'),
                ('retro', '复古风 🟠'),
                ('future', '未来风 🟣'),
                ('minimal', '极简风 ⚪')
            ],
            format_func=lambda x: x[1]
        )

        generate_btn = st.button("🚀 生成创意内容", use_container_width=True)

    with col2:
        if generate_btn and company_desc and job_title:
            # 提取企业画像
            keywords = extract_keywords(company_desc)

            # 显示提取的关键词
            st.subheader("🔍 企业画像提取结果")

            profile_cols = st.columns(2)
            with profile_cols[0]:
                st.markdown("**行业标签**")
                for ind in keywords['industries']:
                    st.markdown(f'<span style="background: #667eea; color: white; padding: 4px 12px; border-radius: 12px; margin: 2px; display: inline-block; font-size: 12px;">{ind}</span>', unsafe_allow_html=True)

                st.markdown("**企业文化**")
                for cul in keywords['culture'][:3]:
                    st.markdown(f'<span style="background: #764ba2; color: white; padding: 4px 12px; border-radius: 12px; margin: 2px; display: inline-block; font-size: 12px;">{cul}</span>', unsafe_allow_html=True)

            with profile_cols[1]:
                st.markdown("**核心产品/技术**")
                for tech in keywords['tech_products'][:3]:
                    st.markdown(f'<span style="background: #f093fb; color: white; padding: 4px 12px; border-radius: 12px; margin: 2px; display: inline-block; font-size: 12px;">{tech}</span>', unsafe_allow_html=True)

                st.markdown("**公司使命**")
                st.markdown(f'<div style="background: rgba(102, 126, 234, 0.2); padding: 8px 12px; border-radius: 8px; font-size: 13px; color: #eaeaea;">{keywords["mission"]}</div>', unsafe_allow_html=True)

            # 映射风格选择
            tone_map = {"专业正式": "professional", "年轻活力": "young", "亲切友好": "friendly"}

            # 生成文案
            job_posting = generate_job_posting(job_title, keywords, tone_map.get(tone_style, 'professional'))

            st.markdown("---")
            st.subheader("✍️ 生成的招聘文案")

            # 使用标签页展示不同格式
            tabs = st.tabs(["完整版", "简短版","朋友圈/小红书"])

            with tabs[0]:
                st.markdown(f"**{job_posting['title']}**")
                st.markdown(job_posting['full'])
                st.button("📋 复制完整文案", key="copy_full", use_container_width=True)

            with tabs[1]:
                st.markdown(f"**{job_posting['title']}**")
                st.markdown(job_posting['short'])
                st.button("📋 复制简短文案", key="copy_short", use_container_width=True)

            with tabs[2]:
                # 为社交媒体生成简化版本
                social_text = f"🚀 {job_title} 招聘中！\n\n{job_posting['short']}\n\n📍 地点：全国\n💰 薪资：面议\n\n#招聘 #{job_title} #{keywords['industries'][0] if keywords['industries'] else '招聘'}"
                st.text_area("社交媒体文案", value=social_text, height=150)

            # 生成海报Prompt
            st.markdown("---")
            st.subheader("🎨 海报设计描述词")

            poster_prompt = generate_poster_prompt(job_title, keywords, poster_style[0])

            st.markdown(f"**已选择风格：{poster_prompt['style_name']}**")

            with st.expander("📝 中文设计描述词（点击查看）"):
                st.code(poster_prompt['chinese_prompt'], language='text')

            with st.expander("🌍 英文 AI 绘画 Prompt（DALL-E/Midjourney）"):
                st.code(poster_prompt['english_prompt'], language='text')

            # 海报预览占位区域
            st.markdown("---")
            st.subheader("🖼️ 海报预览区域")

            # 根据风格生成对应的预览占位图样式
            style_colors = {
                'tech': ('linear-gradient(135deg, #667eea 0%, #764ba2 100%)', '#667eea'),
                'retro': ('linear-gradient(135deg, #f5af19 0%, #f12711 100%)', '#f5af19'),
                'future': ('linear-gradient(135deg, #00f260 0%, #0575e6 100%)', '#00f260'),
                'minimal': ('linear-gradient(135deg, #232526 0%, #414345 100%)', '#414345')
            }

            bg_style, accent_color = style_colors.get(poster_style[0], style_colors['tech'])

            st.markdown(f"""
            <div style="width: 100%; max-width: 400px; margin: 0 auto;
                        aspect-ratio: 9/16;
                        background: {bg_style};
                        border-radius: 16px;
                        display: flex; flex-direction: column;
                        justify-content: center; align-items: center;
                        padding: 40px 30px;
                        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                        position: relative; overflow: hidden;">

                <!-- 装饰性背景元素 -->
                <div style="position: absolute; top: -50px; right: -50px;
                            width: 200px; height: 200px;
                            background: rgba(255,255,255,0.1);
                            border-radius: 50%;"></div>
                <div style="position: absolute; bottom: -80px; left: -80px;
                            width: 250px; height: 250px;
                            background: rgba(255,255,255,0.05);
                            border-radius: 50%;"></div>

                <!-- 内容区域 -->
                <div style="text-align: center; z-index: 1; color: white;">
                    <div style="font-size: 14px; opacity: 0.8; margin-bottom: 20px;">
                        {keywords['industries'][0] if keywords['industries'] else '创新企业'}
                    </div>
                    <div style="font-size: 32px; font-weight: 700;
                                margin-bottom: 30px; line-height: 1.3;">
                        {job_title}
                    </div>
                    <div style="font-size: 18px; margin-bottom: 40px; opacity: 0.9;">
                        加入我们，共创未来
                    </div>
                    <div style="width: 120px; height: 120px;
                                background: white;
                                border-radius: 12px;
                                margin: 0 auto;
                                display: flex; align-items: center; justify-content: center;">
                        <span style="color: #333; font-size: 12px;">二维码<br/>扫码投递</span>
                    </div>
                </div>

                <!-- 底部提示 -->
                <div style="position: absolute; bottom: 20px;
                            font-size: 11px; opacity: 0.6;
                            text-align: center;">
                    {poster_prompt['style_name']} · 智能生成海报
                </div>
            </div>
            """, unsafe_allow_html=True)

            # 提示用户如何使用AI生成真实图片
            st.info("""
            💡 **如何使用AI生成真实海报图片？**

            1. **DALL-E 3 (OpenAI)**: 复制上方的英文Prompt，前往 ChatGPT Plus 的 DALL-E 3 功能
            2. **Midjourney**: 使用英文Prompt，添加参数 `--ar 9:16 --v 6`
            3. **Stable Diffusion**: 使用中文或英文描述词，选择竖版比例
            4. **即梦/可灵等国产工具**: 使用中文描述词，选择海报模板
            """)

        elif generate_btn:
            st.warning("⚠️ 请填写完整的公司描述和岗位名称后再生成")

# ============================================
# 主应用入口
# ============================================

def render_sidebar():
    """
    渲染侧边栏导航
    """
    with st.sidebar:
        # Logo 和标题
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <div style="font-size: 48px; margin-bottom: 10px;">🏢</div>
            <h1 style="margin: 0; font-size: 24px;">SmartHR</h1>
            <p style="margin: 5px 0 0 0; color: #a0a0a0; font-size: 12px;">智能人力资源工作台</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # 导航菜单
        st.markdown("### 📋 功能导航")

        # 使用 session_state 存储当前选中的模块
        if 'current_module' not in st.session_state:
            st.session_state.current_module = "招聘漏斗分析"

        # 导航按钮
        modules = [
            ("📊 招聘漏斗分析", "招聘漏斗分析"),
            ("🔍 HR数据纠错", "HR数据纠错"),
            ("🎨 AI创意工坊", "AI创意工坊")
        ]

        for icon_label, module_name in modules:
            if st.button(icon_label, use_container_width=True,
                        type="primary" if st.session_state.current_module == module_name else "secondary"):
                st.session_state.current_module = module_name
                st.rerun()

        st.markdown("---")

        # 快捷操作区
        st.markdown("### ⚡ 快捷操作")

        if st.button("📊 生成模拟招聘数据", use_container_width=True):
            df = generate_mock_recruitment_data(100)
            st.success(f"已生成 {len(df)} 条模拟招聘数据！")

        if st.button("👥 生成模拟员工数据", use_container_width=True):
            df = generate_mock_employee_data(50)
            st.success(f"已生成 {len(df)} 条模拟员工数据！")

        st.markdown("---")

        # 系统信息
        st.markdown("""
        <div style="font-size: 11px; color: #666; text-align: center;">
            <p>SmartHR v1.0.0</p>
            <p>Powered by Streamlit + Plotly + Pandas</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    """
    主应用入口函数
    """
    # 初始化页面配置
    init_page_config()

    # 应用自定义样式
    apply_custom_css()

    # 渲染侧边栏
    render_sidebar()

    # 主内容区域
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1>🏢 SmartHR 智能人力资源工作台</h1>
        <p style="color: #a0a0a0;">数据驱动决策 · AI赋能创意 · 智能优化流程</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # 根据选中的模块渲染对应内容
    current = st.session_state.get('current_module', '招聘漏斗分析')

    if current == "招聘漏斗分析":
        render_recruitment_module()
    elif current == "HR数据纠错":
        render_hr_auditor_module()
    elif current == "AI创意工坊":
        render_creative_hub_module()

if __name__ == "__main__":
    main()
