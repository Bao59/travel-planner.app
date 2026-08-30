import streamlit as st
from datetime import date


# =========================
# 網頁基本設定
# =========================

st.set_page_config(
    page_title="Travel Planner",
    page_icon="✈️",
    layout="wide",
)


# =========================
# 初始化資料
# =========================

if "trip" not in st.session_state:
    st.session_state.trip = {
        "name": "",
        "destination": "",
        "start_date": date.today(),
        "end_date": date.today(),
    }


if "itinerary" not in st.session_state:
    st.session_state.itinerary = []


if "hotels" not in st.session_state:
    st.session_state.hotels = []


if "transportations" not in st.session_state:
    st.session_state.transportations = []


if "packing_list" not in st.session_state:
    st.session_state.packing_list = []


if "expenses" not in st.session_state:
    st.session_state.expenses = []


# =========================
# Sidebar
# =========================

st.sidebar.title("✈️ Travel Planner")

page = st.sidebar.radio(
    "選擇功能",
    [
        "🏠 旅程總覽",
        "📝 建立旅程",
        "📅 行程規劃",
        "🏨 住宿",
        "🚆 交通",
        "🧳 行李",
        "💰 支出",
    ],
)


# =========================
# 旅程總覽
# =========================

if page == "🏠 旅程總覽":

    st.title("✈️ 我的旅程")

    trip = st.session_state.trip

    if trip["name"] == "":
        st.info("目前還沒有建立旅程。請先到「建立旅程」。")

    else:

        st.subheader(trip["name"])

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "目的地",
            trip["destination"],
        )

        col2.metric(
            "出發日期",
            str(trip["start_date"]),
        )

        col3.metric(
            "回程日期",
            str(trip["end_date"]),
        )

        st.divider()

        # -------------------------
        # 行程
        # -------------------------

        st.subheader("📅 行程")

        if len(st.session_state.itinerary) == 0:
            st.write("尚未建立行程。")

        else:

            for item in st.session_state.itinerary:

                st.write(
                    f"""
                    **{item["date"]} {item["time"]}**

                    📍 {item["place"]}

                    {item["activity"]}

                    備註：{item["note"]}
                    """
                )

                st.divider()

        # -------------------------
        # 預算
        # -------------------------

        st.subheader("💰 支出")

        total = 0

        for expense in st.session_state.expenses:
            total += expense["amount"]

        st.metric(
            "目前總支出",
            f"NT$ {total:,}",
        )


# =========================
# 建立旅程
# =========================

elif page == "📝 建立旅程":

    st.title("📝 建立旅程")

    trip_name = st.text_input(
        "旅程名稱",
        value=st.session_state.trip["name"],
        placeholder="例如：東京五天四夜",
    )

    destination = st.text_input(
        "目的地",
        value=st.session_state.trip["destination"],
        placeholder="例如：東京",
    )

    col1, col2 = st.columns(2)

    start_date = col1.date_input(
        "出發日期",
        value=st.session_state.trip["start_date"],
    )

    end_date = col2.date_input(
        "回程日期",
        value=st.session_state.trip["end_date"],
    )

    if st.button("儲存旅程", type="primary"):

        st.session_state.trip = {
            "name": trip_name,
            "destination": destination,
            "start_date": start_date,
            "end_date": end_date,
        }

        st.success("旅程已儲存！")


# =========================
# 行程規劃
# =========================

elif page == "📅 行程規劃":

    st.title("📅 行程規劃")

    with st.form("itinerary_form"):

        itinerary_date = st.date_input(
            "日期",
            value=st.session_state.trip["start_date"],
        )

        itinerary_time = st.time_input(
            "時間"
        )

        place = st.text_input(
            "地點",
            placeholder="例如：淺草寺",
        )

        activity = st.text_input(
            "活動",
            placeholder="例如：參觀淺草寺",
        )

        note = st.text_area(
            "備註"
        )

        submitted = st.form_submit_button(
            "加入行程"
        )

    if submitted:

        item = {
            "date": itinerary_date,
            "time": itinerary_time,
            "place": place,
            "activity": activity,
            "note": note,
        }

        st.session_state.itinerary.append(item)

        st.success("行程已加入！")


    st.divider()

    st.subheader("目前行程")

    if len(st.session_state.itinerary) == 0:

        st.write("尚未建立行程。")

    else:

        for index, item in enumerate(st.session_state.itinerary):

            col1, col2 = st.columns([5, 1])

            with col1:

                st.write(
                    f"""
                    **{item["date"]} {item["time"]}**

                    📍 {item["place"]}

                    {item["activity"]}

                    {item["note"]}
                    """
                )

            with col2:

                if st.button(
                    "刪除",
                    key=f"delete_itinerary_{index}",
                ):

                    del st.session_state.itinerary[index]

                    st.rerun()

            st.divider()


# =========================
# 住宿
# =========================

elif page == "🏨 住宿":

    st.title("🏨 住宿資訊")

    with st.form("hotel_form"):

        hotel_name = st.text_input(
            "住宿名稱"
        )

        hotel_address = st.text_input(
            "地址"
        )

        check_in = st.date_input(
            "入住日期"
        )

        check_out = st.date_input(
            "退房日期"
        )

        booking_number = st.text_input(
            "訂房編號"
        )

        submitted = st.form_submit_button(
            "加入住宿"
        )

    if submitted:

        hotel = {
            "name": hotel_name,
            "address": hotel_address,
            "check_in": check_in,
            "check_out": check_out,
            "booking_number": booking_number,
        }

        st.session_state.hotels.append(hotel)

        st.success("住宿已加入！")


    st.divider()

    for hotel in st.session_state.hotels:

        st.subheader(hotel["name"])

        st.write(f"📍 {hotel['address']}")

        st.write(
            f"入住：{hotel['check_in']} → 退房：{hotel['check_out']}"
        )

        st.write(
            f"訂房編號：{hotel['booking_number']}"
        )

        st.divider()


# =========================
# 交通
# =========================

elif page == "🚆 交通":

    st.title("🚆 交通資訊")

    with st.form("transport_form"):

        transport_type = st.selectbox(
            "交通方式",
            [
                "飛機",
                "火車",
                "高鐵",
                "巴士",
                "捷運",
                "計程車",
                "租車",
                "其他",
            ],
        )

        company = st.text_input(
            "公司 / 業者",
            placeholder="例如：長榮航空",
        )

        number = st.text_input(
            "班次 / 航班",
            placeholder="例如：BR198",
        )

        departure = st.text_input(
            "出發地"
        )

        arrival = st.text_input(
            "目的地"
        )

        submitted = st.form_submit_button(
            "加入交通"
        )

    if submitted:

        transportation = {
            "type": transport_type,
            "company": company,
            "number": number,
            "departure": departure,
            "arrival": arrival,
        }

        st.session_state.transportations.append(
            transportation
        )

        st.success("交通資訊已加入！")


    st.divider()

    for transport in st.session_state.transportations:

        st.write(
            f"""
            ### {transport["type"]}

            {transport["company"]}  
            班次：{transport["number"]}

            {transport["departure"]}
            ➜
            {transport["arrival"]}
            """
        )

        st.divider()


# =========================
# 行李
# =========================

elif page == "🧳 行李":

    st.title("🧳 行李清單")

    new_item = st.text_input(
        "新增物品",
        placeholder="例如：護照",
    )

    if st.button("加入行李"):

        if new_item != "":

            item = {
                "name": new_item,
                "packed": False,
            }

            st.session_state.packing_list.append(item)

            st.rerun()


    st.divider()

    for index, item in enumerate(
        st.session_state.packing_list
    ):

        checked = st.checkbox(
            item["name"],
            value=item["packed"],
            key=f"packing_{index}",
        )

        st.session_state.packing_list[index][
            "packed"
        ] = checked


# =========================
# 支出
# =========================

elif page == "💰 支出":

    st.title("💰 旅遊支出")

    with st.form("expense_form"):

        expense_name = st.text_input(
            "支出項目",
            placeholder="例如：晚餐",
        )

        amount = st.number_input(
            "金額",
            min_value=0,
            step=100,
        )

        category = st.selectbox(
            "分類",
            [
                "餐飲",
                "交通",
                "住宿",
                "購物",
                "景點",
                "其他",
            ],
        )

        submitted = st.form_submit_button(
            "新增支出"
        )

    if submitted:

        expense = {
            "name": expense_name,
            "amount": amount,
            "category": category,
        }

        st.session_state.expenses.append(expense)

        st.success("支出已新增！")


    st.divider()

    total = 0

    for expense in st.session_state.expenses:

        total += expense["amount"]

        st.write(
            f"""
            **{expense["name"]}**

            {expense["category"]}

            NT$ {expense["amount"]:,}
            """
        )

        st.divider()


    st.metric(
        "總支出",
        f"NT$ {total:,}",
    )