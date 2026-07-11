# 실시간 시세 (웹소켓)
# 운영: wss://api.kiwoom.com:10000/api/us/websocket
# 모의투자: wss://mockapi.kiwoom.com:10000/api/us/websocket


class OverseasRealtime:
    # 웹소켓 클라이언트 구현은 아직 없음 (stub). 요청/응답 모델만 정의됨.
    # 모델 정의: _overseas_realtime_types.py
    pass


# 공통 요청 모델 (4개 TR 동일 등록/해지 프레임):
#   OverseasRealtimeRequest / OverseasRealtimeRegisterData / OverseasRealtimeRegisterItem
#
# TR	이름	메서드(예정)	values 모델 / 응답 프레임 모델
# F4	미국주식실시간주문확인	get_order_confirmation	OverseasRealtimeOrderConfirmationValues / OverseasRealtimeOrderConfirmation
# F5	미국주식실시간체결	get_execution	OverseasRealtimeExecutionValues / OverseasRealtimeExecution
# FE	미국주식실시간체결가	get_execution_price	OverseasRealtimeExecutionPriceValues / OverseasRealtimeExecutionPrice
# FT	미국주식10호가	get_ten_quotes	OverseasRealtimeTenQuotesValues / OverseasRealtimeTenQuotes
