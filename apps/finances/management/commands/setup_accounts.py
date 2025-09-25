# management/commands/setup_accounts.py

from django.core.management.base import BaseCommand
from apps.finances.models import Account

class Command(BaseCommand):
    help = '기본 계정과목 템플릿 생성'

    def handle(self, *args, **options):
        # 개인장부 템플릿
        personal_accounts = [
            # 자산 계정
            ("1100", "현금", "asset"),
            ("1110", "은행예금", "asset"),
            ("1120", "체크카드", "asset"),
            ("1130", "신용카드", "asset"),
            ("1200", "투자자산", "asset"),
            ("1300", "기타자산", "asset"),

            # 부채 계정
            ("2100", "신용카드미결제", "liability"),
            ("2200", "개인대출", "liability"),
            ("2300", "학자금대출", "liability"),
            ("2900", "기타부채", "liability"),

            # 개인수입 계정
            ("3100", "급여소득", "revenue"),
            ("3200", "용돈/기타수입", "revenue"),
            ("3300", "투자수익", "revenue"),
            ("3400", "부업소득", "revenue"),
            ("3500", "배당수입", "revenue"),
            ("3600", "이자수입", "revenue"),
            ("3900", "기타수입", "revenue"),

            # 개인지출 계정
            ("4100", "식비", "expense"),
            ("4200", "교통비", "expense"),
            ("4300", "생필품/쇼핑", "expense"),
            ("4400", "의료비", "expense"),
            ("4500", "교육비", "expense"),
            ("4600", "여가/오락", "expense"),
            ("4700", "통신비", "expense"),
            ("4800", "보험료", "expense"),
            ("4850", "구독료", "expense"),
            ("4900", "미용/이발", "expense"),
            ("4950", "저축/투자", "expense"),
            ("4960", "대출상환", "expense"),
            ("4970", "세금/과태료", "expense"),
            ("4980", "경조사비", "expense"),
            ("4990", "기타개인지출", "expense"),
        ]

        # 사업장부 템플릿
        business_accounts = [
            # 사업자산 계정
            ("1100", "사업용현금", "asset"),
            ("1110", "사업용예금", "asset"),
            ("1200", "사업용자산", "asset"),
            ("1300", "매출채권", "asset"),
            ("1400", "재고자산", "asset"),
            ("1500", "선급비용", "asset"),
            ("1600", "유형자산", "asset"),
            ("1900", "기타자산", "asset"),

            # 사업부채 계정
            ("2100", "매입채무", "liability"),
            ("2200", "사업대출", "liability"),
            ("2300", "미지급금", "liability"),
            ("2400", "예수금", "liability"),
            ("2500", "부가세예수금", "liability"),
            ("2900", "기타부채", "liability"),

            # 자본 계정
            ("3000", "자본금", "equity"),
            ("3100", "이익잉여금", "equity"),

            # 사업수입 계정
            ("4100", "매출", "revenue"),
            ("4200", "용역수입", "revenue"),
            ("4300", "수수료수입", "revenue"),
            ("4400", "이자수입", "revenue"),
            ("4900", "기타사업수입", "revenue"),

            # 사업비용 계정
            ("5100", "재료비/매입비", "expense"),
            ("5200", "인건비/외주비", "expense"),
            ("5300", "임대료", "expense"),
            ("5400", "공과금", "expense"),
            ("5500", "광고비", "expense"),
            ("5600", "교통비/여비", "expense"),
            ("5700", "접대비", "expense"),
            ("5800", "소모품비", "expense"),
            ("5900", "통신비", "expense"),
            ("6000", "수수료", "expense"),
            ("6100", "세금공과", "expense"),
            ("6200", "감가상각비", "expense"),
            ("6300", "대출이자", "expense"),
            ("6400", "보험료", "expense"),
            ("6500", "교육비", "expense"),
            ("6600", "차량비", "expense"),
            ("6700", "도서인쇄비", "expense"),
            ("6800", "회의비", "expense"),
            ("6900", "기타사업비용", "expense"),
        ]

        # 개인장부 계정 생성
        for code, name, acc_type in personal_accounts:
            Account.objects.get_or_create(
                user_id=0,
                account_code=code,
                account_name=name,
                account_type=acc_type,
                book_type="personal"
            )

        # 사업장부 계정 생성
        for code, name, acc_type in business_accounts:
            Account.objects.get_or_create(
                user_id=0,
                account_code=code,
                account_name=name,
                account_type=acc_type,
                book_type="business"
            )

        self.stdout.write(
            self.style.SUCCESS('계정과목 템플릿이 성공적으로 생성되었습니다.')
        )