# 조건검색 (웹소켓)
# 운영: wss://api.kiwoom.com:10000/api/us/websocket
# 모의투자: wss://mockapi.kiwoom.com:10000/api/us/websocket
#
# 웹소켓 클라이언트 구현은 아직 없음. request/response 모델은
# _overseas_condition_search_types.py 참고.


class OverseasConditionSearch:
    pass


# 미국주식 조건검색 목록조회	usa20280	get_condition_search_list
#   OverseasConditionSearchListRequest / OverseasConditionSearchListResponse
# 미국주식 조건검색 요청 일반	usa20281	request_condition_search
#   OverseasConditionSearchRequest / OverseasConditionSearchResponse
# 미국주식 조건검색 요청 실시간	usa20290	request_realtime_condition_search
#   OverseasConditionSearchRealtimeRequest / OverseasConditionSearchRealtimeResponse
# 미국주식 조건검색 실시간 해제	usa20291	cancel_realtime_condition_search
#   OverseasConditionSearchRealtimeCancelRequest / OverseasConditionSearchRealtimeCancelResponse
