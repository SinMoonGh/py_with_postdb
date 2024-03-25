# import psycopg2

# # PostgreSQL에 연결
# conn = psycopg2.connect(
#     dbname="dvdrental",
#     user="postgres",
#     password="1234",
#     host="localhost"
# )
# cur = conn.cursor()

# # 변수를 담고 있는 데이터프레임이나 리스트 등을 SQL 쿼리 형식으로 변환
# # 예를 들어, 변수 data를 customer 테이블에 삽입
# # data = [('John', 33, 'dudu@naver.com', 100)]
# # for row in data:
# database = cur.execute("select * from address")

# # 변경 사항 저장
# print(conn.commit())

# # 연결 종료
# cur.close()
# conn.close()
# ----------------------------------

# import psycopg2

# # 연결 파라미터 설정
# conn_params = {
#     'dbname': 'testdb',
#     'user': 'postgres',
#     'password': '1234',
#     'host': 'localhost',  # 데이터베이스 서버가 로컬에 있을 경우
# }

# # 데이터베이스 연결 시도
# try:
#     conn = psycopg2.connect(**conn_params)
#     print("데이터베이스에 성공적으로 연결되었습니다.")
# except psycopg2.Error as e:
#     print("데이터베이스 연결 중 오류가 발생했습니다.")
#     print(e)

# -----------------------------------

# 커서 객체 생성
# cur = conn.cursor()

# # SQL 쿼리 실행: 테이블 생성
# create_table_query = """
# CREATE TABLE IF NOT EXISTS users (
#     id SERIAL PRIMARY KEY,
#     name VARCHAR(50),
#     age INT
# );
# """
# cur.execute(create_table_query)
# conn.commit()  # 쿼리 결과를 데이터베이스에 반영

# print("테이블이 성공적으로 생성되었습니다.")

# -----------------------------------
# # 데이터 삽입 쿼리
# insert_query = """
# INSERT INTO users (name, age) VALUES (%s, %s);
# """
# # 데이터 삽입 실행
# cur.execute(insert_query, ('Alice', 24))
# conn.commit()

# print("데이터가 성공적으로 삽입되었습니다.")

# ----------------------------------------

# # 데이터 조회 쿼리
# select_query = 'select * from users'

# # 쿼리 실행
# cur.execute(select_query)

# # 모든 결과 행 가져오기
# rows= cur.fetchall()

# for row in rows:
#     print(row)

# # 자원 정리
#     cur.close()
#     conn.close()

# ----------------------------------------
    
import psycopg2

class CountryCRUD:
    def __init__(self, dbname, user, password, host='localhost'):
        self.conn_params = {
            'dbname': dbname,
            'user': user,
            'password': password,
            'host': host,
        }
        self.conn = None
        self.connect()

    def connect(self):
        """데이터베이스에 연결합니다."""
        try:
            self.conn = psycopg2.connect(**self.conn_params)
            print("데이터베이스에 성공적으로 연결되었습니다.")
        except psycopg2.Error as e:
            print(f"데이터베이스 연결 중 오류가 발생했습니다: {e}")

    def create_country(self, country):
        """country 테이블에 새로운 나라를 추가합니다."""
        print(country)
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO country (country)
                VALUES (%s) RETURNING country_id;
            """, (country,))
            country_id = cur.fetchone()[0]
            self.conn.commit()
            print(f"국가 '{country}'이(가) country {country_id}로 추가되었습니다.")
            return country_id

    def read_country(self, country_id):
        """country_id 기반으로 국가 정보를 조회합니다."""
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM country WHERE country_id = %s;", (country_id,))
            country = cur.fetchone()
            if country:
                print(country)
                return country
            else:
                print("국가를 찾을 수 없습니다.")
                return None

    def update_country(self, country_id, country=None):
        """country 정보를 업데이트합니다."""
        with self.conn.cursor() as cur:
            cur.execute("""
                UPDATE country
                SET country = %s
                WHERE country_id = %s;
            """, (country, country_id))
            self.conn.commit()
            print(f"국가 {country_id}의 정보가 업데이트되었습니다.")

    def delete_country(self, country_id):
        """영화 정보를 삭제합니다."""
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM country WHERE country_id = %s;", (country_id,))
            self.conn.commit()
            print(f"country {country_id}의 정보가 삭제되었습니다.")

    def close(self):
        """데이터베이스 연결을 종료합니다."""
        if self.conn:
            self.conn.close()
            print("데이터베이스 연결이 종료되었습니다.")


# FilmCRUD 인스턴스 생성
country_crud = CountryCRUD(dbname="dvdrental", user="postgres", password="1234", host="localhost")
            
# 새로운 country 추가
country_id = country_crud.create_country("Like Tiger")