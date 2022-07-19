# 05_StockPriceAPI\investar\MarketDB.py

class MarketDB:
    def __init__(self):
        """생성자: MariaDB 연결 및 종목코드 딕셔너리 생성"""
        self.conn = pymysql.connect(host='localhost', user='root',
            passward='*******', db='*******', charset='utf8')
        self.codes = {}
        self.get_comp_info()

    def __del__(self):
        """소멸자: MariaDB 연결 해제"""
        self.conn.close()

    def get_comp_info(self):
        """company_info 테이블에서 읽어와서 codes에 저장"""
        sql = "SELECT * FROM company_info"
        company_info = pd.read_sql(sql, self.conn)
        for idx in range(len(company_info)):
            self.codes[company_info['code'].values[idx]] = company_info['company'].values[idx]

    def get_daily_price(self, code, start_date=None, end_date=None):
        """KRX 종목별 시세를 데이터프레임 형태로 반환"""
        sql = "SELECT * FROM daily_price WHERE code = '{}' and date >= '{}' and date <= '{}'".format(code, start_date, end_date)
        df = pd.read_sql(sql, self.conn)
        df.index = df['date']
        return df
