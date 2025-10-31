# LangGraph Agent v1.0 튜토리얼

이 저장소는 환경 설정부터 실용적인 AI 에이전트 구축까지, Langchain과 LangGraph를 학습하기 위한 포괄적인 튜토리얼 시리즈를 포함하고 있습니다.

## 📚 튜토리얼 구성

### 1. 환경 구성 (1. 환경구성.ipynb)

Langchain/LangGraph 프로젝트를 위한 개발 환경 설정 방법을 배웁니다:

- **UV 패키지 매니저**: 최신 Python 패키지 관리 도구인 UV 설치 및 사용법
  ```bash
  brew install uv
  uv --version
  uv init python_tutorial --python 3.12
  ```

- **LangGraph CLI**: 프로젝트 개발을 위한 LangGraph CLI 설치 및 초기화
  ```bash
  # langgraph-cli 설치
  uv pip install langgraph-cli
  # 또는
  brew install langgraph-cli
  
  # 새 프로젝트 시작
  langgraph new langgraph_tutorial
  cd langgraph_tutorial
  uv sync
  uv run langgraph dev
  ```

### 2. AI Agent 튜토리얼 (2. Agent 튜토리얼.ipynb)

AI 에이전트의 기본 개념과 효과적인 설계 방법을 이해합니다:

#### AI Agent란?

AI Agent는 단순한 자동화 시스템을 넘어, 환경에 반응하여 목표를 달성하기 위해 스스로 경로를 결정하는 지능형 주체입니다.

#### 주요 구성요소

1. **LLM (Large Language Model)**: 에이전트의 두뇌 역할 (GPT-4, Claude, Gemini)
2. **Tools (도구)**: 정보 조회, 계산, API 호출 등을 위한 외부 기능
3. **Memory (메모리)**: 대화 히스토리 및 작업 흐름 컨텍스트 (단기 및 장기 메모리)
4. **Planning (계획)**: 목표를 하위 작업으로 분해

#### AI Agent vs Workflow

| 구분 | AI Agent (에이전트) | Workflow (워크플로우) |
|------|---------------------|---------------------|
| **경로 결정** | 피드백에 따라 자율적으로 경로 결정 | 사전에 정의된 경로를 따름 |
| **작업 분석** | 모호하고 복잡한 문제 해결에 강점 | 의사 결정 과정을 쉽게 그릴 수 있는 경우에 적합 |
| **효율성** | 비용, 지연 시간, 오류 위험이 증가할 수 있음 | 일반적인 작업에서 더 빠르고 효율적이며 신뢰할 수 있음 |

#### 에이전트처럼 생각하기: 모범 사례

1. **명확한 역할 정의**: 구체적인 정체성과 목적을 정의
2. **도구는 역할에 맞게**: 혼란을 피하기 위해 관련 도구만 제공
3. **적을수록 좋다**: 도구는 최대 5-10개로 제한하고, 유사한 기능은 통합
4. **명확한 도구 설명**: 명시적인 이름과 상세한 문서화 사용
5. **컨텍스트 일관성 유지**: 에이전트당 하나의 도메인에 집중
6. **체크리스트**: 에이전트의 역할을 한 문장으로 설명할 수 있나요? 각 도구가 필요하고 잘 문서화되어 있나요?

### 3. Langchain & LangGraph 간단 실습 (3. Langchain Langgraph 간단실습.ipynb)

실용적인 예제와 코드 시연:

#### Langchain LLM API 호출

```python
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

model = ChatOpenAI(model="gpt-4.1-mini")
prompt = ChatPromptTemplate.from_template("{country}의 수도는 어디야?")
chain = prompt | model | StrOutputParser()
response = chain.invoke({"country": "대한민국"})
```

#### Langchain으로 간단한 Agent 만들기

```python
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[get_weather],
    system_prompt="You are a helpful assistant"
)
```

#### LangGraph Agent 구축

LangGraph로 계산기 에이전트를 구축하는 완전한 과정:

1. **도구와 모델 정의**: 도구(add, multiply, divide) 생성 및 LLM에 바인딩
2. **상태 정의**: TypedDict를 사용하여 대화 상태 관리
3. **모델 노드 정의**: LLM 의사결정 노드 생성
4. **도구 노드 및 조건부 로직 정의**: 도구 실행 및 흐름 제어 구현
5. **빌드 및 컴파일**: 그래프 조립 및 에이전트 컴파일

튜토리얼에서는 "3 곱하기 4를 하고 더하기 5 하고 나누기 2 하면 몇이야?"와 같은 복잡한 다단계 계산을 처리하는 방법을 시연합니다.

## 🚀 시작하기

1. 이 저장소를 클론합니다
2. 노트북 1의 환경 설정 지침을 따릅니다
3. 노트북 2의 에이전트 개념을 학습합니다
4. 노트북 3의 실습 예제로 연습합니다

## 📖 추가 자료

- [Python UV 사용 방법과 예제](https://www.0x00.kr/development/python/python-uv-simple-usage-and-example)
- [파이썬 개발자라면 UV를 사용합시다](https://sigridjin.medium.com/)

## 📝 라이선스

자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

