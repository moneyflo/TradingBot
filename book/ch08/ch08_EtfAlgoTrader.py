# EtfAlgoTrader
import ctypes
import win32com.client
from slacker import Slacker
from datetime import datetime
import requests
import pandas as pd

# CREON Plus 공통 Object
cpStatus = win32com.client.Dispatch('CpUtil.CpCybos') # 시스템 상태 정보
cpTradeUtil = win32com.client.Dispatch('CpTrade.CpTdUtil') # 주문 관련 도구
cpStock = win32com.client.Dispatch("DsCbo1.StockMst") # 주식 종목별 정보
cpOhlc = win32com.client.Dispatch("CpSysDib.StockChart") # OHLC 정보
cpBalance = win32com.client.Dispatch('CpTrade.CpTd6033')   # 계좌 정보
cpCodeMgr = win32com.client.Dispatch('CpUtil.CpStockCode') # 종목코드
cpCash = win32com.client.Dispatch("CpTrade.CpTdNew5331A")  # 주문 가능 금액

# CREON Plus 시스템 점검 함수
def check_creon_system():
    """크레온 플러스 시스템 연결 상태를 점검한다."""
    # 관리자 권한으로 프로세스 실행 여부
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print('check_creon_system() : admin user -> FAILED')
        return False

    # 연결 여부 체크
    if (cpStatus.IsConnect == 0):
        print('check_creon_system() : connect to server -> FAILED')
        return False

    # 주문 관련 초기화
    if (cpTradeUtil.TradeInit(0) != 0):
        print('check_creon_system() : init trade -> FAILED')
        return False

    return True

# slack 이슈 전송
my_token = 'xoxb-3791511357665-3764278580871-9NXzyhZDvEFPghWBn4xBCdN6'
def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text})

def dbgout(message):
    """인자로 받은 문자열을 파이썬 셸과 슬랙으로 동시에 출력한다."""
    print(datetime.now().strftime('[%m/%d %H:%M:%S]'), message)
    strbuf = datetime.now().strftime('[%m/%d %H:%M:%S]') + message
    post_message(my_token,"#etf-algo-trading",strbuf)


# 파이썬 셸에만 출력
def printlog(message, *args):
    """인자로 받은 문자열을 파이썬 셸에 출력한다."""
    print(datetime.now().strftime('[%m/%d %H:%M:%S]'), message, *args)


# 현재가 조회
def get_current_price(code):
    """인자로 받은 종목의 현재가, 매도호가, 매수호가를 반환한다."""
    cpStock.SetInputValue(0, code) # 종목코드에 대한 가격 정보
    cpStock.BlockRequest()

    item = {}
    item['cur_price'] = cpStock.GetHeaderValue(11) # 현재가
    item['ask'] = cpStock.GetHeaderValue(16)       # 매도호가
    item['bid'] = cpStock.GetHeaderValue(17)       # 매수호가

    return item['cur_price'], item['ask'], item['bid']


# OHLC 조회
def get_ohlc(code, qty):
    """인자로 받은 종목의 OHLC 가격 정보를 qty 개수만큼 반환한다."""
    cpOhlc.SetInputValue(0, code)            # 종목코드
    cpOhlc.SetInputValue(1, ord('2'))        # 1:기간, 2:개수
    cpOhlc.SetInputValue(4, qty)             # 요청 개수
    cpOhlc.SetInputValue(5, [0,2,3,4,5])     # 0:날짜, 2~5:OHLC
    cpOhlc.SetInputValue(6, ord('D'))        # D:일단위
    cpOhlc.SetInputValue(9, ord('1'))        # 0:무수정주가, 1:수정주가
    cpOhlc.BlockRequest()

    count = cpOhlc.GetHeaderValue(3)  # 3:수신 개수
    columns = ['open', 'high', 'low', 'close']
    index = []
    rows = []
    for i in range(count):
        index.append(cpOhlc.GetDataValue(0, i))
        rows.append([cpOhlc.GetDataValue(1, i), cpOhlc.GetDataValue(2, i),
            cpOhlc.GetDataValue(3, i), cpOhlc.GetDataValue(4, i)])

    df = pd.DataFrame(rows, columns=columns, index=index)
    return df


# 주식 잔고 조회
def get_stock_balance(code):
    """인자로 받은 종목의 종목명과 수량을 반환한다."""
    cpTradeUtil.TradeInit()
    acc = cpTradeUtil.AccountNumber[0]         # 계좌번호
    accFlag = cpTradeUtil.GoodsList(acc, 1)    # -1:전체, 1:주식, 2:선물/옵션
    cpBalance.SetInputValue(0, acc)            # 계좌번호
    cpBalance.SetInputValue(1, accFlag[0])     # 상품 구분 - 주식 상품 중 첫 번째
    cpBalance.SetInputValue(2, 50)             # 요청 건수(최대 50)
    cpBalance.BlockRequest()

    if code == 'ALL':
        dbgout('계좌명: ' + str(cpBalance.GetHeaderValue(0)))
        dbgout('결제잔고수량 : ' + str(cpBalance.GetHeaderValue(1)))
        dbgout('평가금액 ' + str(cpBalance.GetHeaderValue(3)))
        dbgout('평가손익: ' + str(cpBalance.GetHeaderValue(4)))
        dbgout('종목수: ' + str(cpBalance.GetHeaderValue(7)))

    stocks = []
    for i in range(cpBalance.GetHeaderValue(7)):
        stock_code = cpBalance.GetDataValue(12, i)  # 종목코드
        stock_name = cpBalance.GetDataValue(0, i)   # 종목명
        stock_qty = cpBalance.GetDataValue(15, i)   # 수량
        if code == 'ALL':
            dbgout(str(i+1) + ' ' + stock_code + '(' + stock_name + ')'
                + ':' + str(stock_qty))
            stocks.append({'code': stock_code, 'name': stock_name,
                'qty': stock_qty})
        if stock_code == code:
            return stock_name, stock_qty
    if code == 'ALL':
        return stocks
    else:
        stock_name = cpCodeMgr.CodeToName(code)
        return stock_name, 0


# 주문 가능 금액 조회
def get_current_cash():
    """증거금 100% 주문 가능 금액을 반환한다."""
    cpTradeUtil.TradeInit()
    acc = cpTradeUtil.AccountNumber[0]      # 계좌번호
    accFlag = cpTradeUtil.GoodsList(acc, 1) # -1:전체, 1:주식, 2:선물/옵션
    cpCash.SetInputValue(0, acc)            # 계좌번호
    cpCash.SetInputValue(1, accFlag[0])     # 상품 구분 - 주식 상품 중 첫 번째
    cpCash.BlockRequest()

    return cpCash.GetHeaderValue(9) # 증거금 100% 주문 가능 금액
