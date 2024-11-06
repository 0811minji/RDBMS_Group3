# RDBMS_Group3

데이터 어떻게 쪼갤지

answerCode = 근데 정답 여부가 0,1로 나타난 거라서 쪼개기 어려울지도..??

앱이 어떻게 생겼을지 화면 몇개를 구상해보는 건 어떨까??(ex. 첫화면, 어떻게 연결되면 어떤 기능이 나올지)

15주차까지 4주반 남았음

10주차 그림 완성, 정답률 계산식 만들기

11주차 첫화면, 단원분석 기능 만들기

12주차 문항분석기능, 학생분석기능 만들기

13주차 여유분 한 주

14주차 피피티 만들기, 발표 준비

데이터 전처리

- 학생 정보 - 학년, 성별 쪼개기
- 7,8,9학년으로 제한

# RDBMS Project - 1106 Meeting

### Requirements

백엔드 데이터베이스 + 프론트엔드 솔루션 → 전체 어플리케이션 개발

요구사항

- 데이터베이스: table 4개 이상, table 당 row 5,000개 이상, column 2개 이상
- 프론트엔드
    1. SQL 쿼리 4개 이상 호출 → SELECT, INSERT/UPDATE/DELETE, JOIN, GROUP BY, 조합 가능
    2. standalone Python GUI, R, web-based (e.g. using Flask, React) 사용 가능
    3. 결과 반환 속도: 10-15초 미만

평가 기준

- 데이터베이스 모델링 및 설계 (데이터 전처리, ER 다이어그램 포함)
- 주제와 데이터에 적합한 어플리케이션 기능
- GUI 디자인
- SQL 쿼리 복잡성
- 어플리케이션 실행 시간 및 안정성

### DB Structure

**Raw Data**

[라벨]수학 지식체계 데이터 세트_210611

| iD | name | semester | description | chapter.name | achievement.id | achievement.name | toConceptid |
| --- | --- | --- | --- | --- | --- | --- | --- |

[원천]성취수준데이터셋_train

1_문항정오답표

| learnerID | learnerProfile | testID | assessmentItemID | answerCode | Timestamp |
| --- | --- | --- | --- | --- | --- |

2_문항IRT

| testID | assessmentItemID | difficultyLevel(난이도) | discriminationLevel(변별도) | guessLevel(추측도) | KnowledgeTag | Timestamp |
| --- | --- | --- | --- | --- | --- | --- |

난이도: 수험자가 그 문항을 정답으로 선택할 확률이 50%가 되도록 설정된 능력 → 높을수록 문항을 정답으로 맞추기 어려움

변별도: 문항이 수험자의 능력을 얼마나 잘 변별할 수 있는지 나타내는 지표 → 높을수록 능력이 높은 수험자가 정답을 맞출 확률이 높고, 능력이 낮은 수험자가 오답을 선택할 확률이 높암

추측도: 수험자가 능력 수준과 관계없이 정답을 맞출 확률

3_응시자IRT

| learnerID | learnerProfile | testID | theta (이해도) | realScore | Timestamp |
| --- | --- | --- | --- | --- | --- |

**DB Scheme**

knowledge →  수학 지식체계 데이터 세트

| iD | name | semester | description | chapter.name | achievement.id | achievement.name | toConceptid |
| --- | --- | --- | --- | --- | --- | --- | --- |

learner → 문항정오답표 or 응시자IRT

| learnerID | learnerProfile.gender | learnerProfile.schoolLevel | learnerProfile.gradeLevel |
| --- | --- | --- | --- |

test → 문항IRT

| testID | assessmentItemID | difficultyLevel | discriminationLevel | guessLevel | KnowledgeTag |
| --- | --- | --- | --- | --- | --- |

learner-answerCode → 문항정오답표

| learnerID | testID | assessmentItemID | answerCode |
| --- | --- | --- | --- |

learner-theta/realScore → 응시자IRT

| learnerID | testID | theta | realScore |
| --- | --- | --- | --- |

### Application

학생/시험/문항/응시결과 등록/삭제 → INSERT/DELETE

챕터별 학생 성취도

학생 (1명/학년별) 선택 → KnowledgeTag의 Chapter가 같은 testID끼리 grouping → theta 평균/median 계산 → JOIN, GROUP BY

부족한 개념 추출

학생 (1명) 선택 → theta 하위 n개 testID에 대한 KnowledgeTag 추출 → 해당 Concept name, toConceptid 반환 → SELECT, JOIN

문항 분석/추천

문항 선택 → 모든 학생에 대한 testID별 정답률 및 theta 평균/median/quantile 계산 → 적절한 구간에서 학생 그룹 분할 → 각 그룹 학생 정보 임시 저장 → SELECT/GROUP BY(/VIEW)

→ 각 학생 그룹 및 testID별 정답률 및 theta 평균/median 계산 → SELECT/GROUP BY/JOIN

→ 각 학생 그룹별 높은 수준의 학생들에게는 난이도와 변별력이 높은 문제를, 낮은 수준의 학생들에게는 난이도와 변별력이 낮은 문제를 추천 (이때, 정답률 → 변별력 → 난이도 순서대로 고려)

학생별 정답률

학생 선택 → 시험/문항 id를 통해서 knowledge tag 추출 → knowledge tag로 grouping하여(counting 먼저 해서 확인 → 1,2개만 있는 지식 태그는 좀… 문제가 될 수도..?) 지식태그(챕터)별로 정답률 계산

고려 사항

→ 챕터별 학생 성취도가 낮다는 것과 학생들이 해당 챕터의 개념이 부족하다는 것 사이의 연관성을 보이기 위해서 어떻게 해야 할까?

→ IRT 계산 방법 알아보기
