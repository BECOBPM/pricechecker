import streamlit as st
import pandas as pd
from PIL import Image

# 1. 페이지 설정
st.set_page_config(
    page_title="산안비 적격성 검토 시스템",
    page_icon="🛡️",
    layout="wide"
)

# 2. 고용노동부 고시 기준 8대 항목
CATEGORIES = [
    "1. 안전관리자 등 인건비 및 각종 수당",
    "2. 안전시설비 등 (추락·낙하 방지시설 등)",
    "3. 개인보호구 및 안전장구 구입비 등",
    "4. 사업장의 안전보건진단비 등",
    "5. 안전보건교육비 및 행사비 등",
    "6. 근로자의 건강관리비 등",
    "7. 기술지도비",
    "8. 본사 전담조직 운영비"
]

# 3. 산안비 적격성 판정 엔진
def evaluate_item(item_name: str, category: str, amount: int, total_budget: int):
    name_clean = item_name.strip()
    
    # 1) 부적격 우선 판정 (시공성 자재, 타 법령 소관)
    ineligible_rules = [
        ("시스템 비계", "작업 통로 및 발판 역할을 겸하는 가설 구조물(비계)은 시공성 가설물로 직접공사비에 반영되어야 하므로 산안비 불인정 (단, 추락방지망·안전난간대 등 순수 안전장치 추가분은 인정 가능)", "공사 직접비로 이관 필요"),
        ("비계", "작업 발판 및 시공 보조용 가설비계는 공사 원가 반영 대상이므로 산안비 불인정", "공사 직접비 내역 확인"),
        ("신호수", "도로 점용 공사 및 일반 차량 유도를 위한 교통 신호수는 건설기술진흥법(건진법)상 안전관리비 소관으로 산안비 사용 불가 (단, 양중기 유도수 등 순수 작업장 안전신호수는 인정 가능)", "건진법 안전관리비 정산 전환"),
        ("일반장갑", "단순 작업 능률 향상 및 오염 방지용 일반 면장갑/코팅장갑은 산안비 불인정 (KCs 인증 안전장갑, 절단방지, 용접용 가죽장갑은 인정)", "개인보호구 KCs 인증 확인"),
        ("방진복", "단순 작업복/위생복은 작업용 피복비(직접비) 대상이므로 산안비 처리 불가 (특수 화학물질/석면 취급용 보호복은 예외 인정)", "유해물질 취급 공정 증빙 필요")
    ]
    
    for keyword, reason, guide in ineligible_rules:
        if keyword in name_clean:
            return {
                "status": "부적격",
                "badge": "🔴 불인정",
                "reason": reason,
                "guide": guide,
                "doc_check": "환수 또는 공사원가 재분류 대상"
            }

    # 2) 스마트 안전장비 한도 검토 (총액 20%)
    if any(k in name_clean for k in ["스마트", "AI CCTV", "이동형 CCTV", "웨어러블", "가스감지기"]):
        limit_val = total_budget * 0.20
        if amount > limit_val:
            return {
                "status": "한도초과",
                "badge": "🟠 한도초과(보완)",
                "reason": f"스마트 안전장비는 법정 한도(총 산안비의 20%, {limit_val:,.0f}원)를 초과할 수 없습니다. (현재 신청액: {amount:,.0f}원)",
                "guide": "한도 이내 금액 분할 인정 또는 시공사 자체 부담",
                "doc_check": "스마트 안전장비 사양서, 통신망 연동 확인서, 세금계산서"
            }
        return {
            "status": "적격",
            "badge": "🟢 적격 (스마트장비)",
            "reason": "건설업 스마트 안전장비 계상 기준에 부합하며 20% 한도 이내입니다.",
            "guide": "모니터링 관제 화면 및 설치 사진 필수",
            "doc_check": "현장 관제 사진, 납품서, 세금계산서"
        }

    # 3) 근로자 자율개선 품목 (폭염/한파 등, 총액 15%)
    if any(k in name_clean for k in ["아이스조끼", "쿨토시", "보온덧신", "휴게실", "제빙기", "포도당"]):
        limit_val = total_budget * 0.15
        if amount > limit_val:
            return {
                "status": "한도초과",
                "badge": "🟠 한도초과(보완)",
                "reason": f"근로자 건강장해 예방 및 자율개선 품목은 총 산안비의 15%({limit_val:,.0f}원) 한도 이내여야 합니다.",
                "guide": "15% 이내로 지출액 조정 필요",
                "doc_check": "위험성평가 결과표 또는 노사협의체 의결 회의록 필수"
            }
        return {
            "status": "적격",
            "badge": "🟢 적격 (자율개선)",
            "reason": "폭염·한파 대비 보건 증진 품목으로 적격합니다. (위험성평가/노사협의체 반영 필요)",
            "guide": "지급 대장 및 실물 사진 첨부",
            "doc_check": "노사협의체 회의록, 지급 확인 서명부"
        }

    # 4) 일반 적격 기본 판정
    return {
        "status": "적격",
        "badge": "🟢 적격 승인",
        "reason": f"고용노동부 고시 제7조 항목 [{category}] 기준에 부합하는 적격 안전비 지출입니다.",
        "guide": "세금계산서, 거래명세서, 전·후 사진 일치 확인",
        "doc_check": "세금계산서, 현장 설치/지급 전·후 사진, KCs 인증표(해당 시)"
    }

# 세션 상태 초기화
if "items_list" not in st.session_state:
    st.session_state.items_list = [
        {"품목명": "용접용 가죽 안전장갑", "항목": CATEGORIES[2], "신청금액": 250000, "사진수": 1, "판정": "🟢 적격 승인", "사유": "KCs 인증 안전보호구 기준 충족", "필요서류": "세금계산서, 지급대장"},
        {"품목명": "외부 작업용 시스템 비계 임대", "항목": CATEGORIES[1], "신청금액": 4500000, "사진수": 1, "판정": "🔴 불인정", "사유": "시공성 가설 구조물로 직접공사비 반영 대상 (산안비 불인정)", "필요서류": "공사 직접비로 이관 필요"}
    ]

# 4. 상단 대시보드
st.title("🛡️ 산업안전보건관리비(산안비) 적격성 자동 검토 시스템")
st.caption("고용노동부 고시 「건설업 산업안전보건관리비 계상 및 사용기준」 기반 실시간 판정 및 증빙 대조")

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    total_budget = st.number_input("현장 총 산안비 예산 (원)", min_value=1000000, value=50000000, step=1000000, format="%d")
with col2:
    st.metric("스마트 안전장비 법정 한도 (20%)", f"{total_budget * 0.2:,.0f} 원")
with col3:
    st.metric("자율개선/보건 품목 한도 (15%)", f"{total_budget * 0.15:,.0f} 원")

st.divider()

# 5. 입력 및 업로드 영역
left_col, right_col = st.columns([1, 1])

with left_col:
    st.subheader("1. 사용내역 등록")
    with st.form("item_form", clear_on_submit=True):
        item_name = st.text_input("품목명 (예: 용접장갑, 시스템 비계, 스마트 AI CCTV, 신호수)", placeholder="품목명을 입력하세요")
        category = st.selectbox("산안비 분류 항목", CATEGORIES)
        amount = st.number_input("지출 금액 (원)", min_value=0, value=150000, step=10000)
        submit_btn = st.form_submit_button("내역 검토 및 등록", use_container_width=True)

    if submit_btn:
        if not item_name.strip():
            st.warning("품목명을 입력해 주세요.")
        else:
            res = evaluate_item(item_name, category, amount, total_budget)
            new_record = {
                "품목명": item_name,
                "항목": category,
                "신청금액": amount,
                "사진수": 0,
                "판정": res["badge"],
                "사유": res["reason"],
                "필요서류": res["doc_check"]
            }
            st.session_state.items_list.append(new_record)
            st.success(f"'{item_name}' 검토 완료: {res['badge']}")

with right_col:
    st.subheader("2. 현장 증빙 사진 업로드 (선택)")
    uploaded_files = st.file_uploader("영수증, KCs 인증마크, 설치 전·후 사진 등록", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    if uploaded_files:
        st.write(f"총 {len(uploaded_files)}개의 증빙 사진이 로드되었습니다.")
        img_cols = st.columns(min(len(uploaded_files), 3))
        for idx, file in enumerate(uploaded_files[:3]):
            with img_cols[idx]:
                img = Image.open(file)
                st.image(img, caption=file.name, use_container_width=True)

st.divider()

# 6. 검토 대장 결과 테이블
st.subheader("📋 산안비 적격성 검토 대장")

if st.session_state.items_list:
    df = pd.DataFrame(st.session_state.items_list)
    
    # 통계 메트릭
    approved_sum = df[df["판정"].str.contains("적격")]["신청금액"].sum()
    rejected_sum = df[df["판정"].str.contains("불인정")]["신청금액"].sum()
    
    m1, m2, m3 = st.columns(3)
    m1.metric("총 등록 건수", f"{len(df)} 건")
    m2.metric("적격 승인 예정액", f"{approved_sum:,.0f} 원")
    m3.metric("부적격(불인정) 금액", f"{rejected_sum:,.0f} 원", delta=f"-{rejected_sum:,.0f}", delta_color="inverse")
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    c1, c2 = st.columns([1, 4])
    with c1:
        if st.button("목록 초기화"):
            st.session_state.items_list = []
            st.rerun()
    with c2:
        csv_data = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="정산 보고서(CSV) 다운로드",
            data=csv_data,
            file_name="산안비_정산검토_내역서.csv",
            mime="text/csv"
        )
else:
    st.info("등록된 산안비 내역이 없습니다. 좌측 폼에서 품목을 입력해 보세요.")