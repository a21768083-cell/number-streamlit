import streamlit as st
import random

# 페이지 설정
st.set_page_config(
    page_title="숫자 맞추기 밸런스 게임",
    page_icon="🔥",
    layout="centered"
)

# 커스텀 CSS 스타일링
st.markdown("""
<style>
    .main-title {
        font-size: 28px;
        font-weight: bold;
        color: #ff4b4b;
        text-align: center;
        margin-bottom: 5px;
    }
    .sub-title {
        font-size: 16px;
        text-align: center;
        color: #555555;
        margin-bottom: 25px;
    }
    .status-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin-bottom: 20px;
        border-left: 5px solid #ff4b4b;
    }
    .hint-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #e8f4f8;
        margin-top: 15px;
        border-left: 5px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🔥 [밸런스 모드] 사칙연산 힌트 미션!</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">숫자를 맞히려면 사칙연산 미션을 성공해야 합니다!</div>', unsafe_allow_html=True)

# 1. 게임 상태 초기화 (st.session_state)
if 'secret_number' not in st.session_state:
    st.session_state.secret_number = random.randint(1, 100)
    st.session_state.max_count = 7
    st.session_state.current_attempt = 1
    st.session_state.game_over = False
    st.session_state.game_won = False
    st.session_state.stage = "guess"  # "guess" (숫자입력) -> "math" (연산미션) -> "result" (결과확인)
    st.session_state.last_guess = None
    
    # 첫 번째 연산 미션 생성
    oper = random.choice(['+', '-', '*'])
    if oper == '+':
        n1, n2 = random.randint(1, 50), random.randint(1, 50)
        correct = n1 + n2
    elif oper == '-':
        n1, n2 = random.randint(50, 100), random.randint(1, 50)
        correct = n1 - n2
    else:
        while True:
            n1 = random.randint(2, 20)
            n2 = random.randint(2, 9)
            if n1 * n2 <= 100:
                break
        correct = n1 * n2
    st.session_state.math_problem = {"n1": n1, "oper": oper, "n2": n2, "correct": correct}

# 게임 리셋 함수
def reset_game():
    st.session_state.secret_number = random.randint(1, 100)
    st.session_state.current_attempt = 1
    st.session_state.game_over = False
    st.session_state.game_won = False
    st.session_state.stage = "guess"
    st.session_state.last_guess = None
    generate_new_math()

# 새로운 연산 미션 생성 함수
def generate_new_math():
    oper = random.choice(['+', '-', '*'])
    if oper == '+':
        n1, n2 = random.randint(1, 50), random.randint(1, 50)
        correct = n1 + n2
    elif oper == '-':
        n1, n2 = random.randint(50, 100), random.randint(1, 50)
        correct = n1 - n2
    else:
        while True:
            n1 = random.randint(2, 20)
            n2 = random.randint(2, 9)
            if n1 * n2 <= 100:
                break
        correct = n1 * n2
    st.session_state.math_problem = {"n1": n1, "oper": oper, "n2": n2, "correct": correct}

# 게임 진행 상태 표시
if not st.session_state.game_over and not st.session_state.game_won:
    remaining = st.session_state.max_count - st.session_state.current_attempt + 1
    st.markdown(f"""
    <div class="status-box">
        <b>🎯 {st.session_state.current_attempt}번째 도전 중</b> (남은 기회: {remaining}번)
    </div>
    """, unsafe_allow_html=True)

# 게임 결과 메시지 출력 구역
if st.session_state.game_won:
    st.balloons()
    st.success(f"🎊 완벽합니다! {st.session_state.current_attempt}번 만에 맞혔어요! 당신은 진정한 연산 왕! 👑")
    st.info(f"정답은 [ {st.session_state.secret_number} ] 이었습니다.")
    if st.button("게임 다시 시작하기", on_click=reset_game):
        pass
elif st.session_state.game_over:
    st.error(f"😢 아쉽게도 모든 기회를 소진하셨습니다...")
    st.warning(f"정답은 바로 [ {st.session_state.secret_number} ] 이었습니다! 다음에 다시 도전하세요!")
    if st.button("게임 다시 시작하기", on_click=reset_game):
        pass

# 게임이 진행 중일 때 인터페이스
else:
    # 1단계: 숫자 입력받기
    if st.session_state.stage == "guess":
        with st.form(key='guess_form'):
            guess_input = st.number_input("정답이라고 생각하는 1~100 사이의 숫자를 입력하세요:", min_value=1, max_value=100, step=1, value=50)
            submit_guess = st.form_submit_button(label='숫자 제출 및 미션 받기')
            
            if submit_guess:
                st.session_state.last_guess = guess_input
                if guess_input == st.session_state.secret_number:
                    st.session_state.game_won = True
                    st.rerun()
                else:
                    # 마지막 기회였는데 틀린 경우 바로 게임 오버
                    if st.session_state.current_attempt >= st.session_state.max_count:
                        st.session_state.game_over = True
                        st.rerun()
                    else:
                        st.session_state.stage = "math"
                        st.rerun()

    # 2단계: 연산 미션 풀기
    elif st.session_state.stage == "math":
        prob = st.session_state.math_problem
        st.info(f"🤔 내가 입력한 숫자: {st.session_state.last_guess} | 과연 UP일까요, DOWN일까요?")
        st.markdown("📢 **힌트 미션! 아래 사칙연산 문제를 맞혀야 Up/Down 힌트가 제공됩니다!**")
        
        with st.form(key='math_form'):
            user_math = st.number_input(f"문제: {prob['n1']} {prob['oper']} {prob['n2']} = ?", step=1, value=0)
            submit_math = st.form_submit_button(label='연산 정답 제출')
            
            if submit_math:
                if user_math == prob['correct']:
                    st.session_state.math_result = "success"
                else:
                    st.session_state.math_result = "fail"
                st.session_state.stage = "result"
                st.rerun()

    # 3단계: 연산 결과에 따른 힌트 확인 및 라운드 넘기기
    elif st.session_state.stage == "result":
        prob = st.session_state.math_problem
        guess = st.session_state.last_guess
        secret = st.session_state.secret_number
        
        if st.session_state.math_result == "success":
            st.success("✅ 사칙연산 정답입니다! 힌트를 드립니다.")
            if guess < secret:
                st.markdown(f"""
                <div class="hint-box">
                    👉 <b>힌트:</b> 당신이 입력한 {guess}보다 <span style='color:red; font-weight:bold;'>[ UP ]</span> !!
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="hint-box">
                    👉 <b>힌트:</b> 당신이 입력한 {guess}보다 <span style='color:blue; font-weight:bold;'>[ DOWN ]</span> !!
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error(f"❌ 땡! 틀렸습니다. (정답은 {prob['correct']}이었습니다.)")
            st.warning("🤫 미션 실패로 인해 Up/Down 힌트가 제공되지 않습니다!")
            
        if st.button("다음 도전으로 넘어가기"):
            st.session_state.current_attempt += 1
            st.session_state.stage = "guess"
            generate_new_math()
            st.rerun()

# 개발자 정보 가볍게 노출
st.markdown("---")
st.caption("🎮 Streamlit으로 구현된 숫자 맞추기 밸런스 게임")
