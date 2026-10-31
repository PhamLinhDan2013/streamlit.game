import streamlit as st
import time

st.set_page_config(page_title="Game Chạy Đua Tốc Độ", page_icon="🏃", layout="centered")

# Khởi tạo Session State quản lý trạng thái game
if "game_state" not in st.session_state:
    st.session_state.game_state = "menu"  # menu hoặc playing hoặc game_over
if "opponent_type" not in st.session_state:
    st.session_state.opponent_type = ""
if "player_pos" not in st.session_state:
    st.session_state.player_pos = 0.0
if "opponent_pos" not in st.session_state:
    st.session_state.opponent_pos = 0.0
if "opponent_speed" not in st.session_state:
    st.session_state.opponent_speed = 0.0
if "result_msg" not in st.session_state:
    st.session_state.result_msg = ""

TRACK_LENGTH = 100  # Độ dài đường đua

def start_game(op_type):
    st.session_state.game_state = "playing"
    st.session_state.opponent_type = op_type
    st.session_state.player_pos = 0.0
    st.session_state.opponent_pos = 0.0
    
    # Thiết lập tốc độ cho từng đối thủ
    if op_type == "leopard":
        st.session_state.opponent_speed = 0.75  # Con báo chạy rất nhanh
        st.session_state.opponent_name = "🐆 Con Báo"
    elif op_type == "npc":
        st.session_state.opponent_name = "🤖 NPC Thường"
        st.session_state.opponent_speed = 0.45  # NPC chạy tốc độ trung bình
    elif op_type == "fast_runner":
        st.session_state.opponent_name = "⚡ Vận Động Viên Siêu Tốc"
        st.session_state.opponent_speed = 0.90  # Siêu nhanh, cực kỳ khó thắng

def reset_to_menu():
    st.session_state.game_state = "menu"

# --- GIAO DIỆN 1: MÀN HÌNH CHÍNH (CHỌN ĐỐI THỦ) ---
if st.session_state.game_state == "menu":
    st.title("🏃 GAME CHẠY ĐUA TỐC ĐỘ")
    st.markdown("### Hãy chọn đối thủ bạn muốn chạy đua bên dưới:")
    st.write("💡 **Cách chơi:** Ở màn hình tiếp theo, bấm liên tục vào nút **'Bấm Dấu Cách (Space)'** để nhân vật của bạn tiến về phía trước. Bấm càng nhanh, chạy càng tốc độ!")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 1. Con Báo")
        st.write("Chạy cực kỳ nhanh, thử thách lớn cho phản xạ của bạn.")
        if st.button("🏁 Bắt đầu với Báo", use_container_width=True):
            start_game("leopard")
            st.rerun()
            
    with col2:
        st.markdown("#### 2. NPC Thường")
        st.write("Đốc thúc vừa phải, phù hợp để làm quen với nhịp game.")
        if st.button("🏁 Bắt đầu với NPC", use_container_width=True):
            start_game("npc")
            st.rerun()
            
    with col3:
        st.markdown("#### 3. Chạy Siêu Nhanh")
        st.write("Đối thủ siêu tốc độ, đòi hỏi bạn phải bấm phím liên tục không ngừng nghỉ.")
        if st.button("🏁 Bắt đầu Thách Thức", use_container_width=True):
            start_game("fast_runner")
            st.rerun()

# --- GIAO DIỆN 2: MÀN HÌNH ĐANG CHƠI ---
elif st.session_state.game_state == "playing":
    st.title("🏁 CUỘC ĐUA ĐANG DIỄN RA!")
    st.subheader(f"Đối thủ của bạn: {st.session_state.opponent_name}")
    
    # Đối thủ tự động di chuyển nhẹ theo thời gian thực dựa vào tốc độ của họ
    st.session_state.opponent_pos += st.session_state.opponent_speed
    
    # Kiểm tra điều kiện kết thúc nếu đối thủ về đích trước
    if st.session_state.opponent_pos >= TRACK_LENGTH:
        st.session_state.game_state = "game_over"
        st.session_state.result_msg = f"😢 Thua mất rồi! {st.session_state.opponent_name} đã về đích trước!"
        st.rerun()

    # Kiểm tra nếu người chơi về đích trước
    if st.session_state.player_pos >= TRACK_LENGTH:
        st.session_state.game_state = "game_over"
        st.session_state.result_msg = "🏆 Chúc mừng! Bạn đã chiến thắng cuộc đua!"
        st.rerun()

    # Vẽ đường đua mô phỏng bằng thanh tiến độ (Progress bar)
    st.write("👤 **Bạn:**")
    st.progress(min(int(st.session_state.player_pos), 100))
    
    st.write(f"{st.session_state.opponent_name}:")
    st.progress(min(int(st.session_state.opponent_pos), 100))
    
    st.markdown("---")
    st.markdown("### 👇 BẤM LIÊN TỤC VÀO NÚT BÊN DƯỚI ĐỂ CHẠY:")
    
    # Nút bấm mô phỏng thao tác "Space" (Dấu cách)
    if st.button("🏃‍♂️ BẤM ĐỂ CHẠY (SPACE) 🏃‍♂️", use_container_width=True):
        st.session_state.player_pos += 3.5  # Mỗi lần bấm tiến lên một đoạn
        st.rerun()
        
    # Nút quay lại Menu
    if st.button("🔄 Quay lại chọn đối thủ"):
        reset_to_menu()
        st.rerun()
        
    # Tạo độ trễ nhỏ để làm mượt chuyển động của đối thủ tự động
    time.sleep(0.3)
    st.rerun()

# --- GIAO DIỆN 3: KẾT THÚC GAME ---
elif st.session_state.game_state == "game_over":
    st.title("📢 KẾT QUẢ CUỘC ĐUA")
    if "Chiến thắng" in st.session_state.result_msg:
        st.success(st.session_state.result_msg)
    else:
        st.error(st.session_state.result_msg)
        
    if st.button("🔄 Chơi Lại / Chọn Lại Đối Thủ", use_container_width=True):
        reset_to_menu()
        st.rerun()
