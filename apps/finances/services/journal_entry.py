# apps/finances/services/journal_entry.py

class JournalEntryService:
    @staticmethod
    def create_transaction_summary(journal_entry):
        """거래 요약 생성"""
        summary = []
        for detail in journal_entry.transaction_details.all():
            if detail.debit_amount > 0:
                summary.append({
                    "account_name": detail.account.account_name,
                    "account_type": detail.account.account_type,
                    "change": f"+{detail.debit_amount}"
                })
            else:
                summary.append({
                    "account_name": detail.account.account_name,
                    "account_type": detail.account.account_type,
                    "change": f"-{detail.credit_amount}"
                })
        return summary