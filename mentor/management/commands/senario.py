from django.core.management.base import BaseCommand
from mentor.models import Question, Answer
from accounts.models import UserProfile
from django.utils import timezone

class Command(BaseCommand):
    help = "연애선배 카테고리에 질문과 답변을 자동 삽입합니다."

    def handle(self, *args, **kwargs):
        try:
            author = UserProfile.objects.get(id=1)
        except UserProfile.DoesNotExist:
            self.stderr.write(self.style.ERROR("id=1인 UserProfile이 존재하지 않습니다."))
            return

        data = [
            {
                "title": "연애 경험이 없는 20대 초반",
                "question": "지금까지 연애 경험이 한 번도 없어요. 주변 사람들은 다들 연애하는데 저는 어떻게 시작해야 할지도 모르겠고, 저 같은 사람은 연애 못 할까봐 걱정돼요.",
                "answer": """연애는 누구나 자연스럽게 겪는 일이기도 하지만, 절대 ‘빨리 해야 할 일’은 아닙니다. 중요한 건, 스스로를 이해하고 좋아하는 것부터 시작하는 거예요. 저도 24살까지 연애 경험이 없었는데, 그 시기에 제 외모나 성격을 바꾸려 하기보단 취미와 인간관계를 넓히는 데 집중했어요. 그러다 보니 사람들과 자연스럽게 어울리는 기회가 생겼고, 그 안에서 관계가 생기더라고요. 연애는 준비된 사람에게 기회가 오는 게 아니라, ‘자기 삶을 잘 살아가는 사람’에게 다가옵니다. 나를 먼저 사랑하세요."""
            },
            {
                "title": "연인과의 다툼이 잦아진 1년 차 커플",
                "question": "사귄 지 1년 정도 됐는데, 요즘 사소한 걸로 자주 싸워요. 서로 맞지 않는다는 생각도 드는데 계속 만나야 할지 고민돼요.",
                "answer": """1년쯤 되는 시기는 관계가 익숙해지면서 ‘성장통’을 겪는 시기입니다. 다툼의 이유를 곰곰이 살펴보세요. 반복되는 패턴이 있나요? 저도 예전에 비슷한 상황에서 ‘서운함을 참다가 폭발하는’ 식으로 싸움이 커졌어요. 그때 바꾼 건, 감정이 커지기 전에 ‘나는 이런 상황이 반복되면 힘들어’라고 말하는 연습이었습니다. 대화는 타이밍과 방식이 전부예요. 싸움을 덜 하려고 하지 말고, ‘잘 싸우는 법’을 연습해보세요. 그래도 해결되지 않는다면, 이 관계가 서로를 지치게 하는 건 아닌지 차분히 돌아봐야 해요."""
            }
        ]

        for entry in data:
            q = Question.objects.create(
                author=author,
                category='love',
                title=entry["title"],
                content=entry["question"],
                is_anonymous=True,
                created_at=timezone.now()
            )
            Answer.objects.create(
                question=q,
                author=author,
                content=entry["answer"],
                created_at=timezone.now()
            )

        self.stdout.write(self.style.SUCCESS("연애선배 질문과 답변이 성공적으로 삽입되었습니다."))
